# AGENTS.md — Diretrizes para agentes de IA neste projeto

> **Leia este arquivo antes de qualquer alteração.** Ele centraliza o estado
> atual, as regras obrigatórias e as decisões vigentes do projeto. Todos os
> agentes que manipularem este repositório (Claude Code, Kiro, OpenCode, etc.)
> devem segui-lo. Histórico completo: `CHANGELOG.md` · Rationale das decisões:
> `DECISIONS.md`.

## Objetivo do projeto

Pesquisa de *Mining Software Repositories* (MSR): identificar repositórios
GitHub que **realmente trabalham com agentes de IA** — detectados por múltiplos
sinais (arquivos de instrução como `AGENTS.md` e variações, diretórios de
convenção como `.claude/`, co-author em commits, prefixos de branch) — e
baixar seus arquivos `.md` para análise.

Base: paper *"Investigating Autonomous Agent Contributions in the Wild:
Activity Patterns and Code Change over Time"* (Popescu et al., 2026) e seu
dataset público `AISE-TUDelft/MOSAIC-agentic-3m` (Hugging Face); catálogo de
heurísticas de *"Promises, Perils, and (Timely) Heuristics for Mining Coding
Agent Activity"* (Robbes et al., MSR'26).

## Estado atual (atualizar sempre que algo mudar)

- **Script:** `miner_agents.py` v0.2 — lê `Repositories_{Agente}` do dataset,
  deduplica por `name_with_owner`, amostra, faz *partial clone* via git
  (`--filter=blob:none`) e classifica cada repo como **adotante** se qualquer
  sinal do catálogo `heuristics.json` bater (arquivo de instrução na raiz,
  diretório de convenção, subpasta conhecida, co-author em commits, prefixo de
  branch). Adotantes têm **todos** os `.md` baixados.
- **Última execução v0.1 (2026-09-19):** `--limit 500 --seed 42 --workers 5` →
  106 repos adotantes por arquivo na raiz (`CLAUDE.md` 71 · `AGENTS.md` 55 ·
  `GEMINI.md` 4) · 6.781 `.md` baixados (96 MB) · 77 "erros" = repos hoje
  privados/removidos. (Backup: `data/manifest_v0.1.csv`.)
- **Rodada v0.2 (2026-09-23):** mesma amostra, multi-sinal → **390 repos
  adotantes** (vs 106 v0.1; +285 via novos sinais) · 14.633 `.md` baixados
  (~188 MB) · 78 erros. Sinais: commit 287 · branch 250 · arquivo raiz 107 ·
  dir raiz 50 · subpasta 7. Resultados e análise: `CHANGELOG.md` (2026-09-23).
- **Dados:** `data/` (gitignored) — `data/manifest.csv` (1 linha por repo,
  colunas `signals` + `heuristics_version`), `data/downloads/`, `data/parquet/`.
- **Protocolo:** `PROTOCOLO.md` v0.1 (rascunho) — objetivo + RQs do mestrado
  (dívida de intenção); validar com o orientador. Reuniões: `meetings/`
  (transcrições + resumos executivos anotados).
- **Decisões vigentes:** D1–D6 (`DECISIONS.md`) + candidata **D7** (corpus de
  conteúdo = adotantes com arquivo de instrução explícito) em `PROTOCOLO.md`.

## Convenções e regras obrigatórias

1. **Nunca commitar** `data/`, `.venv/` nem `papers/` (ver `.gitignore`).
2. **Toda alteração** neste repositório gera uma entrada **datada** em
   `CHANGELOG.md` (o que mudou + por que + origem: agente, orientador, novo
   paper, mudança de dataset...).
3. **Toda decisão nova/revertida** ganha registro em `DECISIONS.md` (formato
   ADR) e é resumida na tabela abaixo.
4. Rodar sempre com `.venv/bin/python`; instalar deps com
   `.venv/bin/pip install -r requirements.txt`.
5. **Reprodutibilidade:** registrar sempre `--seed`, `--limit` e parâmetros
   nas entradas do CHANGELOG; parquet ficam cacheados em `data/parquet/`.
6. **Idioma:** textos em PT-BR; termos técnicos/nomes de convenções em inglês
   (AGENTS.md, DECISIONS.md, partial clone, sparse-checkout, parquet...).
7. **Artigos (PDFs):** não versionar PDFs no git. Guardar em `papers/`
   (gitignored) e registrar metadados/links em `papers/MANIFEST.md`.
8. **Orientações do orientador:** registrar como entrada de CHANGELOG
   (origem = orientador); se mudarem abordagem, atualizar `DECISIONS.md`.
9. **`heuristics.json`:** catálogo data-driven de sinais. Toda alteração nele
   exige novo número de `version`, entrada de CHANGELOG e (se mudar critério)
   atualização em `DECISIONS.md` — combate o Peril 4 do paper (heurísticas
   mudam rápido).
10. **Protocolo e reuniões:** o objetivo + RQs do mestrado ficam em
    `PROTOCOLO.md` (documento vivo; toda mudança gera CHANGELOG). Transcrições
    de reuniões e resumos executivos anotados ficam em `meetings/` (versionados).

## Como rodar

```bash
python3 -m venv .venv                      # 1ª vez
.venv/bin/pip install -r requirements.txt  # 1ª vez

.venv/bin/python miner_agents.py --limit 500 --seed 42   # amostra
.venv/bin/python miner_agents.py --merged-only           # só repos com PR de agente mergeado
.venv/bin/python miner_agents.py --limit 0               # dataset inteiro (pode levar horas)
.venv/bin/python miner_agents.py --resume                # continua de onde parou
.venv/bin/python miner_agents.py --no-commit-signals     # desliga varredura de commits
.venv/bin/python miner_agents.py --no-branch-signals     # desliga ls-remote de branches
.venv/bin/python miner_agents.py --heuristics outros.json# catálogo alternativo
```

## Decisões vigentes (resumo)

| ID | Decisão | Status |
|----|---------|--------|
| D1 | Dataset fonte = `AISE-TUDelft/MOSAIC-agentic-3m` (`Repositories_{Claude,Codex,Copilot,Devin,Jules}`, sem `Human`) | vigente |
| D2 | Abordagem **sem token**: partial clone via git em vez de GitHub API | vigente |
| D3 | Escopo de download: **todos** os `.md` dos adotantes (detecção ampliada por D6) | vigente |
| D4 | Primeira rodada em **amostra** (`--limit 500`, `seed 42`) antes de escala total | concluída |
| D5 | Artigos: PDFs **fora** do git (`papers/`); manifest versionado (`papers/MANIFEST.md`) | vigente |
| D6 | Detecção **multi-sinal** via `heuristics.json` (Robbes et al.): arquivos/dirs na raiz, subpastas conhecidas, co-author em commits, prefixos de branch | vigente |

Rationale completo e alternativas consideradas: `DECISIONS.md`.

## Papers e contexto

- PDFs: `papers/` (gitignored). Manifest versionado: `papers/MANIFEST.md`.
- Paper de base: Popescu et al. (2026) — dataset MOSAIC-agentic-3m; *search
  signals* para atribuir PRs a agentes (branch prefix, author bots, watermarks).
- Heurísticas (D6): Robbes et al. (MSR'26) — catálogo de heurísticas para
  detectar coding agents (files, commits, branches, PRs); Peril 1
  (observabilidade parcial), Peril 4 (velocity), Promise 5 (taxonomia dos
  arquivos de guidance).
- Protocolo de exemplo (orientador — "veja introdução e metodologia"): Cynthia,
  Das, Roy (MSR'26) — *Are We All Using Agents the Same Way?* — template de
  estudo empírico (coleta, RQ por seção, validação com LLM + humanos + Kappa).
- Conteúdo dos context files: Chatlatanagulchai et al. (TOSEM'26) — *Agent
  READMEs* — estratégia de coleta (varredura da raiz por nomes conhecidos) +
  taxonomia de 16 tipos de instrução + manutenção (rajadas curtas).
- Estilo de protocolo do orientador: Fontão et al. (2018, JSERD) — mineração +
  métricas + validação com praticantes (survey).

## Roadmap

- [ ] Validar `PROTOCOLO.md` com o orientador (RQs + corpus de conteúdo — D7)
- [ ] Rodada completa do dataset (`--limit 0`)
- [ ] Validação manual de precisão das heurísticas (Peril 1)
- [ ] Análise de conteúdo dos arquivos de instrução (RQ2): taxonomia de 16 tipos
      (Agent READMEs) + construto do orientador (objetivos/restrições/razões);
      rotulagem LLM + validação humana com Cohen's Kappa
- [ ] Análise de evolução temporal dos context files vs. atividade de código
      (RQ3 — hipótese de dívida de intenção)
- [x] ~~v2: detecção multi-sinal~~ (concluído em 2026-09-23 — D6)
- [ ] Cruzamento com outros datasets (ex.: `disler/agent-contexts`) p/ estimar
      cobertura
- [ ] Expansão de universo via lista de ~10k repos adotantes do paper de
      heurísticas (Section 6)