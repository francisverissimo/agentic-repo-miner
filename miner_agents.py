#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
miner_agents.py — Mineração de repositórios que trabalham com agentes de IA
============================================================================

Objetivo
--------
A partir do dataset público "MOSAIC-agentic-3m" (paper "Investigating Autonomous
Agent Contributions in the Wild" — Popescu et al., 2026), este script:

  1. Carrega os repositórios onde agentes de IA (Claude, Codex, Copilot, Devin,
     Jules) abriram Pull Requests;
  2. Detecta quais desses repositórios adotaram arquivos de instrução para
     agentes (AGENTS.md e variações como CLAUDE.md, COPILOT_INSTRUCTIONS.md,
     GEMINI.md, OPENHANDS.md, ...);
  3. Para cada repositório com instrução, baixa TODOS os arquivos .md
     (preservando o caminho relativo).

Fonte de dados
--------------
https://huggingface.co/datasets/AISE-TUDelft/MOSAIC-agentic-3m
Tabelas usadas (uma por agente): data/{AGENTE}/Repositories/*.parquet
Nota: o campo de branch padrão veio com typo no dataset ("default_brach").

Como funciona (e por que não usa a API do GitHub)
--------------------------------------------------
  Em vez de chamar a API (que tem rate limit de 60 requisições/hora sem token),
  usamos *clone parcial* do git:

    git clone --depth 1 --filter=blob:none --no-checkout --sparse URL repo

  Isso baixa apenas a "árvore" de nomes de arquivos (~dezenas de KB), sem
  nenhum conteúdo. Daí:

    git ls-tree -r --name-only HEAD   -> lista TODOS os arquivos do repo

  Com essa lista detectamos AGENTS.md/variantes e enumeramos todos os .md.
  Se há instrução de agente, materializamos só os .md:

    git sparse-checkout set --no-cone <caminhos-dos-md...>
    git checkout

  ...e copiamos os arquivos para data/downloads/{owner}__{repo}/.

Uso
---
  python3 miner_agents.py                       # amostra de 500 repos
  python3 miner_agents.py --limit 500 --seed 42 --workers 4
  python3 miner_agents.py --limit 0             # processa todos
  python3 miner_agents.py --merged-only         # só repos com PR de agente merged
  python3 miner_agents.py --resume              # continua de onde parou

Dependências
------------
  pip install pandas pyarrow
  (git é usado via subprocess; precisa estar instalado no sistema)
"""

import argparse
import csv
import os
import shutil
import subprocess
import threading
import time
import urllib.request
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed

import pandas as pd

# ---------------------------------------------------------------------------
# Configurações
# ---------------------------------------------------------------------------

HF_DATASET = "AISE-TUDelft/MOSAIC-agentic-3m"
PARQUET_URL_TEMPLATE = (
    "https://huggingface.co/datasets/"
    + HF_DATASET
    + "/resolve/main/data/{agent}/{table}/train-00000-of-00001.parquet"
)

# Agentes incluídos no dataset do paper (a parte "Human" fica de fora,
# pois o objetivo são repositórios que trabalham COM agentes).
DEFAULT_AGENTS = ["Claude", "Codex", "Copilot", "Devin", "Jules"]

# Nomes de arquivos de instrução de agente detectados na RAIZ do repositório.
# A comparação é case-insensitive (AGENTS.md, agents.md, Agents.md ...).
# Estenda esta lista conforme novas convenções/agentes aparecerem.
INSTRUCTION_NAMES = {
    "agents.md",
    "claude.md",
    "copilot_instructions.md",
    "gemini.md",
    "openhands.md",
    "cursor.md",
    "windy.md",
    "q.md",
    "amazon_q.md",
    "devin.md",
    "roo.md",
    "trae.md",
    "codewisdom.md",
    "jules.md",
}

# Extensões de arquivos considerados "markdown"
MD_EXTENSIONS = (".md", ".markdown", ".mdown")

MANIFEST_FIELDS = [
    "name_with_owner",
    "default_branch",
    "stars",
    "agents",
    "instruction_files",
    "total_md_in_tree",
    "md_downloaded",
    "status",
    "error",
]

_print_lock = threading.Lock()


# ---------------------------------------------------------------------------
# Utilitários
# ---------------------------------------------------------------------------

def log(msg: str) -> None:
    with _print_lock:
        print(msg, flush=True)


def download_parquet(agent: str, table: str, parquet_dir: str) -> str:
    """Baixa (e cacheia) um parquet do HuggingFace."""
    dest = os.path.join(parquet_dir, f"{agent}_{table}.parquet")
    if os.path.exists(dest) and os.path.getsize(dest) > 0:
        return dest
    os.makedirs(parquet_dir, exist_ok=True)
    url = PARQUET_URL_TEMPLATE.format(agent=agent, table=table)
    req = urllib.request.Request(url, headers={"User-Agent": "miner_agents"})
    log(f"  baixando parquet: {url}")
    with urllib.request.urlopen(req, timeout=300) as resp, open(dest, "wb") as fh:
        shutil.copyfileobj(resp, fh)
    return dest


# ---------------------------------------------------------------------------
# Leitura e preparação da lista de repositórios
# ---------------------------------------------------------------------------

def load_repos(agents: list[str], parquet_dir: str, merged_only: bool) -> pd.DataFrame:
    """Junta as tabelas Repositories_{agente}, deduplica e agrega metadados."""
    frames = []
    for agent in agents:
        repos_path = download_parquet(agent, "Repositories", parquet_dir)
        repo_df = pd.read_parquet(repos_path)
        repo_df["agent"] = agent

        if merged_only:
            # Restringe aos repos cujo PR do agente foi de fato mergeado
            # (sinal mais forte de que o repo "trabalha" com o agente).
            pr_path = download_parquet(agent, "PullRequests", parquet_dir)
            pr_df = pd.read_parquet(pr_path)
            pr_df["_state"] = pr_df["state"].astype(str).str.upper()
            merged_ids = set(pr_df.loc[pr_df["_state"] == "MERGED", "id"])
            repo_df = repo_df[repo_df["pr_id"].isin(merged_ids)]

        frames.append(repo_df)

    df = pd.concat(frames, ignore_index=True)

    # Remove linhas sem nome de repo
    df = df[df["name_with_owner"].notna() & (df["name_with_owner"].astype(str).str.strip() != "")]
    df["name_with_owner"] = df["name_with_owner"].astype(str)

    # Quais agentes aparecem em cada repo
    agents_by_repo = (
        df.groupby("name_with_owner")["agent"]
        .apply(lambda s: ",".join(sorted(set(map(str, s)))))
    )

    df = df.drop_duplicates(subset=["name_with_owner"]).set_index("name_with_owner")
    df["agents"] = agents_by_repo

    # Branch padrão — atenção ao typo "default_brach" presente no dataset
    if "default_brach" in df.columns:
        df["default_branch"] = df["default_brach"]
    elif "default_branch" not in df.columns:
        df["default_branch"] = None

    # Estrelas
    if "stargazer_count" not in df.columns:
        df["stargazer_count"] = -1
    df["stars"] = df["stargazer_count"].fillna(-1).astype(int)

    return df.reset_index()


def sample_repos(df: pd.DataFrame, limit: int, seed: int) -> pd.DataFrame:
    """Amostra aleatória (limit=0 => todos)."""
    if limit and limit > 0 and len(df) > limit:
        return df.sample(n=limit, random_state=seed).reset_index(drop=True)
    return df


# ---------------------------------------------------------------------------
# Operações com git (clone parcial + materialização dos .md)
# ---------------------------------------------------------------------------

class CloneError(RuntimeError):
    pass


def _run(cmd: list[str], cwd: str | None, timeout: int, env: dict | None = None) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, env=env, cwd=cwd)


def git_clone(owner_repo: str, branch: str | None, clone_dir: str, timeout: int) -> None:
    """Clone 'parcial': só a árvore de nomes, sem conteúdo."""
    env = dict(os.environ, GIT_TERMINAL_PROMPT="0")
    base = [
        "git", "clone", "--depth", "1", "--filter=blob:none",
        "--no-checkout", "--sparse", "--single-branch",
        f"https://github.com/{owner_repo}.git", clone_dir,
    ]
    if branch:
        cmd = base[:10] + ["--branch", branch] + base[10:]
        r = _run(cmd, cwd=None, timeout=timeout, env=env)
        if r.returncode == 0:
            return
    # Fallback: branch informada pode estar desatualizada (dataset antigo) —
    # clona sem --branch, usando o branch padrão atual do GitHub.
    r = _run(base, cwd=None, timeout=timeout, env=env)
    if r.returncode != 0:
        err = " | ".join(line.strip() for line in r.stderr.splitlines() if line.strip())
        raise CloneError(err[:400] or f"git clone falhou (rc={r.returncode})")


def clone_with_retry(owner_repo: str, branch: str | None, clone_dir: str,
                     timeout: int = 300, retries: int = 2, delay: float = 1.0) -> None:
    last_err = None
    for attempt in range(retries + 1):
        if attempt:
            time.sleep(delay * (2 ** (attempt - 1)))
        try:
            git_clone(owner_repo, branch, clone_dir, timeout=timeout)
            return
        except subprocess.TimeoutExpired as exc:
            last_err = f"timeout durante clone: {exc}"
        except CloneError as exc:
            last_err = str(exc)
        shutil.rmtree(clone_dir, ignore_errors=True)
    raise CloneError(f"{owner_repo}: {last_err}")


def git_ls_tree(clone_dir: str) -> list[str]:
    r = _run(["git", "-C", clone_dir, "ls-tree", "-r", "--name-only", "HEAD"], cwd=None, timeout=120)
    if r.returncode != 0:
        raise CloneError("git ls-tree falhou: " + (r.stderr.strip()[:200] or "?"))
    return [line for line in r.stdout.splitlines() if line]


def materialize_md(clone_dir: str, md_paths: list[str]) -> None:
    """Materializa na working tree APENAS os arquivos .md (sparse-checkout)."""
    # 1) Caminho primário: sparse-checkout com os caminhos exatos (batch fetch)
    if md_paths and len(md_paths) <= 3000:
        r = _run(["git", "-C", clone_dir, "sparse-checkout", "set", "--no-cone", *md_paths],
                 cwd=None, timeout=180)
        if r.returncode == 0:
            r = _run(["git", "-C", clone_dir, "checkout"], cwd=None, timeout=600)
            if r.returncode == 0:
                return
    # 2) Fallback: git checkout HEAD -- <paths> (busca blob a blob)
    if not md_paths:
        return
    if len(md_paths) > 3000:
        raise CloneError(f"repo com muitos .md ({len(md_paths)}) — pulando")
    r = _run(["git", "-C", clone_dir, "checkout", "HEAD", "--", *md_paths], cwd=None, timeout=600)
    if r.returncode != 0:
        raise CloneError("materialização dos .md falhou: " + (r.stderr.strip()[:200] or "?"))


def copy_md_files(clone_dir: str, dest_dir: str, md_paths: list[str]) -> int:
    """Copia os .md materializados preservando o caminho relativo."""
    copied = 0
    for p in md_paths:
        src = os.path.join(clone_dir, p)
        if os.path.isfile(src):
            dst = os.path.join(dest_dir, p)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copy2(src, dst)
            copied += 1
    return copied


# ---------------------------------------------------------------------------
# Processamento de um repositório
# ---------------------------------------------------------------------------

def process_repo(row: pd.Series, clones_dir: str, downloads_dir: str,
                 verbose: bool, delay: float) -> dict:
    owner_repo = row["name_with_owner"]
    branch = row.get("default_branch")
    if branch is not None and isinstance(branch, float) and pd.isna(branch):
        branch = None
    if branch is None and isinstance(branch, str) and branch.strip() in ("", "nan", "None"):
        branch = None

    clone_dir = os.path.join(clones_dir, owner_repo.replace("/", "__"))

    base = {
        "name_with_owner": owner_repo,
        "default_branch": "" if branch is None else str(branch),
        "stars": int(row.get("stars", -1)),
        "agents": str(row.get("agents", "")),
        "instruction_files": "",
        "total_md_in_tree": 0,
        "md_downloaded": 0,
        "status": "",
        "error": "",
    }

    try:
        clone_with_retry(owner_repo, branch, clone_dir)
        if delay:
            time.sleep(delay)  # gentileza com o GitHub durante clones em massa

        tree = git_ls_tree(clone_dir)
        instr = sorted(
            p for p in tree
            if "/" not in p and os.path.basename(p).lower() in INSTRUCTION_NAMES
        )
        md_paths = [p for p in tree if p.lower().endswith(MD_EXTENSIONS)]
        base["total_md_in_tree"] = len(md_paths)

        if not instr:
            base["status"] = "sem_instrucao"
            return base

        materialize_md(clone_dir, md_paths)
        dest_dir = os.path.join(downloads_dir, owner_repo.replace("/", "__"))
        copied = copy_md_files(clone_dir, dest_dir, md_paths)

        base["instruction_files"] = ",".join(instr)
        base["md_downloaded"] = copied
        base["status"] = "baixado"
        return base

    except Exception as exc:  # noqa: BLE001 — erro de um repo não derruba o script
        msg = str(exc)[:400]
        # Git pede credenciais quando o repo é inexistente/privado e prompts
        # estão desabilitados — é o caso mais comum de "erro" neste script.
        if "could not read Username" in msg or "not found" in msg.lower():
            msg = "repositorio privado, inexistente ou deletado"
        base["status"] = "erro"
        base["error"] = msg
        return base

    finally:
        shutil.rmtree(clone_dir, ignore_errors=True)


# ---------------------------------------------------------------------------
# Resumo
# ---------------------------------------------------------------------------

def print_summary(results: list[dict], downloads_dir: str, manifest_path: str) -> None:
    n = len(results)
    ok = [r for r in results if r["status"] != "erro"]
    downloaded = [r for r in results if r["status"] == "baixado"]
    no_instr = [r for r in results if r["status"] == "sem_instrucao"]
    errors = [r for r in results if r["status"] == "erro"]

    print("\n" + "=" * 60)
    print("RESUMO")
    print("=" * 60)
    print(f"Repositórios processados : {n}")
    print(f"  com instrução de agente: {len(downloaded)}")
    print(f"  sem instrução         : {len(no_instr)}")
    print(f"  com erro               : {len(errors)}")
    if errors:
        for r in errors[:10]:
            print(f"    - {r['name_with_owner']}: {r['error']}")

    print("\nArquivos de instrução encontrados (raiz dos repos):")
    counter: Counter = Counter()
    for r in downloaded:
        for f in r["instruction_files"].split(","):
            if f:
                counter[f.upper()] += 1
    if counter:
        for name, count in counter.most_common():
            print(f"  {name:28s} em {count} repos")
    else:
        print("  (nenhum)")

    total_md = sum(r["md_downloaded"] for r in downloaded)
    total_tree = sum(r["total_md_in_tree"] for r in ok)
    print(f"\nArquivos .md baixados     : {total_md}")
    print(f"Arquivos .md no total     : {total_tree} (inclui repos sem instrução)")
    print(f"\nSaída em: {downloads_dir}/")
    print(f"Manifesto: {manifest_path}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Minerador de repositórios com AGENTS.md (dataset MOSAIC-agentic-3m)."
    )
    parser.add_argument("--agents", default=",".join(DEFAULT_AGENTS),
                        help=f"Agentes a considerar (padrão: {','.join(DEFAULT_AGENTS)})")
    parser.add_argument("--limit", type=int, default=500,
                        help="Tamanho da amostra aleatória de repos (0 = todos)")
    parser.add_argument("--seed", type=int, default=42, help="Seed da amostra")
    parser.add_argument("--workers", type=int, default=5, help="Clones em paralelo")
    parser.add_argument("--merged-only", action="store_true",
                        help="Só repos onde o PR do agente foi MERGED")
    parser.add_argument("--data-dir", default="data", help="Diretório de saída")
    parser.add_argument("--resume", action="store_true",
                        help="Não reprocessa repos já presentes no manifest.csv")
    parser.add_argument("--delay", type=float, default=0.25,
                        help="Pausa (s) após cada clone, para não sobrecarregar o GitHub")
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    agents = [a.strip() for a in args.agents.split(",") if a.strip()]

    data_dir = args.data_dir
    parquet_dir = os.path.join(data_dir, "parquet")
    clones_dir = os.path.join(data_dir, "clones")
    downloads_dir = os.path.join(data_dir, "downloads")
    manifest_path = os.path.join(data_dir, "manifest.csv")
    os.makedirs(clones_dir, exist_ok=True)
    os.makedirs(downloads_dir, exist_ok=True)

    print(f"==> Baixando/parseando parquet ({','.join(agents)})...")
    df = load_repos(agents, parquet_dir, args.merged_only)
    df = sample_repos(df, args.limit, args.seed)
    print(f"==> {len(df)} repositórios únicos na amostra")

    # Resume: carrega manifest existente
    done: dict[str, dict] = {}
    if args.resume and os.path.exists(manifest_path):
        with open(manifest_path, newline="", encoding="utf-8") as fh:
            for row in csv.DictReader(fh):
                done[row["name_with_owner"]] = row
        print(f"==> Resume: {len(done)} repos já processados serão pulados")

    results: list[dict] = list(done.values())
    pending = df[~df["name_with_owner"].isin(done)].to_dict("records")

    if not pending:
        print("==> Nada a processar (tudo já em manifest.csv). Use --limit 0 se quiser o restante.")
    else:
        print(f"==> Processando {len(pending)} repos com {args.workers} workers...")
        counter = 0
        with ThreadPoolExecutor(max_workers=args.workers) as ex:
            futures = {
                ex.submit(process_repo, row, clones_dir, downloads_dir, args.verbose, args.delay): row["name_with_owner"]
                for row in pending
            }
            for fut in as_completed(futures):
                counter += 1
                owner_repo = futures[fut]
                try:
                    res = fut.result()
                except Exception as exc:  # defesa extra
                    res = {
                        "name_with_owner": owner_repo,
                        "default_branch": "", "stars": -1, "agents": "",
                        "instruction_files": "", "total_md_in_tree": 0,
                        "md_downloaded": 0, "status": "erro", "error": str(exc)[:400],
                    }
                results.append(res)
                if args.verbose or counter % 25 == 0:
                    log(f"[{counter}/{len(pending)}] {owner_repo} -> {res['status']}")

    # Grava manifest (ordena por nome para facilitar diff)
    results.sort(key=lambda r: r["name_with_owner"])
    with open(manifest_path, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=MANIFEST_FIELDS, extrasaction="ignore")
        writer.writeheader()
        for row in results:
            writer.writerow(row)

    print_summary(results, downloads_dir, manifest_path)


if __name__ == "__main__":
    main()