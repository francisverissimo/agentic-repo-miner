# miner_agents — Mineração de repositórios que trabalham com agentes de IA

Script para achar e baixar arquivos `.md` de repositórios que **de fato
trabalham com agentes de IA** — detectados por múltiplos sinais (arquivos de
instrução como `AGENTS.md` e variações por agente, diretórios de convenção como
`.claude/`, co-author em commits, prefixos de branch). O catálogo de sinais é
data-driven, versionado em `heuristics.json` (base: Robbes et al., MSR'26).

## Contexto (por que este script existe)

O paper *"Investigating Autonomous Agent Contributions in the Wild: Activity
Patterns and Code Change over Time"* (Popescu et al., 2026) disponibilizou um
dataset público no Hugging Face:

- **Dataset:** [`AISE-TUDelft/MOSAIC-agentic-3m`](https://huggingface.co/datasets/AISE-TUDelft/MOSAIC-agentic-3m)
- **Conteúdo:** PRs feitos por agentes (OpenAI Codex, Claude Code, GitHub
  Copilot, Google Jules, Devin) + humanos, com commits, reviews, comentários,
  issues e metadados dos repositórios.

Este script usa as tabelas `Repositories_{Agente}` para obter a **lista de
repositórios onde agentes abriram PRs** (o *universo* da pesquisa), e então
classifica cada repo como **adotante de agentes** usando o catálogo de
heurísticas de Robbes et al. (MSR'26): arquivo de instrução na raiz, diretório
de convenção (`.claude/`, `.codex/`, ...), subpastas conhecidas
(`.github/instructions/`, `copilot-instructions/`, ...), co-author/author em
commits e prefixos de branch. Para cada repo adotante, baixa **todos os
arquivos `.md`**.

## Como funciona (tecnicamente)

Para não depender da API do GitHub (rate limit de 60 req/h sem token), o script
usa **clone parcial do git** + chamadas leves:

1. `git clone --depth 1 --filter=blob:none --no-checkout --sparse --single-branch` —
   baixa só a *árvore de nomes de arquivos* (dezenas de KB), sem conteúdo.
2. `git ls-tree -r --name-only HEAD` lista todos os **arquivos**; uma segunda
   chamada com `-d` lista os **diretórios** (para detectar `.claude/`, etc.).
3. Sinais de commit: o commit `HEAD` é verificado de graça
   (`git log -1`); se não bater, o histórico inteiro é varrido após
   `git fetch --filter=blob:none --unshallow --no-tags` (só objetos de
   commit/tree, sem blobs) — nenhum arquivo de conteúdo é baixado.
4. Sinais de branch: `git ls-remote --heads <url> 'refs/heads/claude/*' ...` —
   uma chamada leve, sem clone.
5. Adotante (qualquer sinal): `git sparse-checkout set --no-cone <...>` +
   `git checkout` materializa **somente** os `.md`.
6. Copia os arquivos para `data/downloads/{owner}__{repo}/` preservando o
   caminho relativo.

Resultado por repositório em `data/manifest.csv` (inclui `signals` e
`heuristics_version`).

## Como rodar

```bash
# 1. Dependências (uma vez)
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt

# 2. Rodar (amostra de 500 repos — padrão)
.venv/bin/python miner_agents.py

# Outros exemplos
.venv/bin/python miner_agents.py --limit 1000 --seed 7 --workers 6
.venv/bin/python miner_agents.py --limit 0              # processa TUDO (pode levar horas)
.venv/bin/python miner_agents.py --merged-only          # só repos com PR de agente mergeado
.venv/bin/python miner_agents.py --resume               # continua de onde parou
.venv/bin/python miner_agents.py --no-commit-signals    # desliga varredura de commits
.venv/bin/python miner_agents.py --no-branch-signals    # desliga ls-remote de branches
.venv/bin/python miner_agents.py --heuristics outro.json # catálogo alternativo
```

## Estrutura de saída

```
data/
├── parquet/                    # parquet baixados do HuggingFace (cache)
├── clones/                     # clones temporários (limpados ao final)
├── downloads/
│   └── owner__repo/            # .md baixados (caminho relativo preservado)
│       ├── AGENTS.md
│       ├── README.md
│       └── docs/...
└── manifest.csv                # um registro por repo processado
```

## Opções principais

| Flag | Padrão | Descrição |
|---|---|---|
| `--agents` | `Claude,Codex,Copilot,Devin,Jules` | Agentes a considerar |
| `--limit` | `500` | Amostra aleatória (`0` = tudo) |
| `--seed` | `42` | Seed da amostra (reproduzível) |
| `--workers` | `5` | Clones em paralelo |
| `--merged-only` | off | Restringe a repos com PR de agente **mergeado** |
| `--delay` | `0.25` | Pausa (s) após cada clone (educação com o GitHub) |
| `--resume` | off | Pula repos já presentes no `manifest.csv` |
| `--heuristics` | `heuristics.json` | Catálogo de sinais (versionado no repo) |
| `--no-commit-signals` | off | Desliga a varredura de autor/co-author em commits |
| `--no-branch-signals` | off | Desliga o `ls-remote` de prefixos de branch |

## Catálogo de heurísticas (`heuristics.json`)

A detecção é **case-insensitive** e dirigida por dados — o script lê o
catálogo `heuristics.json` (versionado no git), cuja **fonte é a Tabela 1** de
Robbes et al. (MSR'26), ampliada com convenções observadas na rodada v0.1:

- `instruction_files_root` — arquivos de instrução **na raiz** (`AGENTS.md`,
  `AGENT.md`, `CLAUDE.md`, `GEMINI.md`, `COPILOT_INSTRUCTIONS.md`,
  `COPILOT-INSTRUCTIONS.md`, `OPENHANDS.md`, `CURSOR.md`, ...);
- `instruction_dirs_root` — diretórios de convenção **na raiz** (`.claude/`,
  `.codex/`, `.cursor/`, `.windsurf/`, `.copilot/`, `.gemini/`, `.cline/`,
  `.kiro/`, `.opencode/`, `memory-bank/`, ...);
- `instruction_paths_anywhere` — caminhos conhecidos **em qualquer nível**
  (`.github/instructions/`, `copilot-instructions/`,
  `.github/workflows/claude|copilot`, `.specify/memory/constitution.md`);
- `commit_signals` — autor/co-author conhecidos (`Co-authored-by: Claude`,
  `noreply@anthropic.com`, `codex@openai.com`, `Copilot`,
  `devin-ai-integration`, `google-labs-jules`, ...);
- `branch_prefixes` — prefixos de branch remoto (`claude/`, `codex/`,
  `copilot/`, `cursor/`, `devin/`, `jules/`, `sweep/`, ...).

> Toda alteração em `heuristics.json` exige novo `version` + entrada no
> `CHANGELOG.md` — heurísticas mudam rápido (Peril 4 do paper).

## Limitações

- O dataset do paper é um snapshot (jun–ago/2025); o script inspeciona o estado
  **atual** dos repositórios.
- Heurísticas são ruidosas por natureza (o paper alerta): ex., um humano
  chamado *Claude* pode assinar commits; `copilot-instructions/` pode conter
  conteúdo para humanos. Por isso o catálogo prioriza padrões específicos
  (emails/repos de convenção conhecidos).
- Sinais de commit varrem o branch padrão (PRs não-mergeados em branches
  próprias não aparecem no histórico).
- Repos deletados/renomeados/privados são registrados como `erro` no manifesto e
  não quebram a execução.

## Documentação do projeto

Para garantir **continuidade** quando o projeto for manipulado por outros
agentes (Claude Code, Kiro, OpenCode, ...), o repositório mantém:

- `AGENTS.md` — contrato central para agentes: estado atual, regras
  obrigatórias e decisões vigentes.
- `CHANGELOG.md` — log datado de todos os passos/incrementos dos experimentos.
- `DECISIONS.md` — registro ADR das decisões (com contexto, alternativas e
  consequências).

Qualquer alteração no projeto exige entrada datada no `CHANGELOG.md` — ver
regras detalhadas no `AGENTS.md`.

## Artigos (papers)

PDFs de artigos **não são versionados** no git — ficam em `papers/` (pasta
ignorada por `.gitignore`), apenas para leitura local. O registro versionado é
o `papers/MANIFEST.md`, com metadados, links e a contribuição de cada artigo
à pesquisa. O paper de base já está lá.