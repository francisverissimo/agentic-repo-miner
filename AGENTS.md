# AGENTS.md — Diretrizes para agentes de IA neste projeto

> **Leia este arquivo antes de qualquer alteração.** Ele centraliza o estado
> atual, as regras obrigatórias e as decisões vigentes do projeto. Todos os
> agentes que manipularem este repositório (Claude Code, Kiro, OpenCode, etc.)
> devem segui-lo. Histórico completo: `CHANGELOG.md` · Rationale das decisões:
> `DECISIONS.md`.

## Objetivo do projeto

Pesquisa de *Mining Software Repositories* (MSR): identificar repositórios
GitHub que **realmente trabalham com agentes de IA** — aqueles que adotaram
arquivos de instrução (`AGENTS.md` e variações como `CLAUDE.md`,
`COPILOT_INSTRUCTIONS.md`, `GEMINI.md`, ...) — e baixar seus arquivos `.md`
para análise.

Base: paper *"Investigating Autonomous Agent Contributions in the Wild:
Activity Patterns and Code Change over Time"* (Popescu et al., 2026) e seu
dataset público `AISE-TUDelft/MOSAIC-agentic-3m` (Hugging Face).

## Estado atual (atualizar sempre que algo mudar)

- **Script:** `miner_agents.py` v0.1 — lê `Repositories_{Agente}` do dataset,
  deduplica por `name_with_owner`, amostra, faz *partial clone* via git
  (`--filter=blob:none`), detecta instruções na **raiz** e baixa **todos** os
  `.md` dos repos adotantes.
- **Última execução (2026-09-19):** `--limit 500 --seed 42 --workers 5` →
  106 repos com arquivo de instrução (`CLAUDE.md` 71 · `AGENTS.md` 55 ·
  `GEMINI.md` 4) · 6.781 `.md` baixados (96 MB) · 77 "erros" = repos hoje
  privados/removidos.
- **Dados:** `data/` (gitignored) — `data/manifest.csv` (1 linha por repo),
  `data/downloads/`, `data/parquet/`.
- **Decisões vigentes:** D1–D5 (`DECISIONS.md`).

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

## Como rodar

```bash
python3 -m venv .venv                      # 1ª vez
.venv/bin/pip install -r requirements.txt  # 1ª vez

.venv/bin/python miner_agents.py --limit 500 --seed 42   # amostra
.venv/bin/python miner_agents.py --merged-only           # só repos com PR de agente mergeado
.venv/bin/python miner_agents.py --limit 0               # dataset inteiro (pode levar horas)
.venv/bin/python miner_agents.py --resume                # continua de onde parou
```

## Decisões vigentes (resumo)

| ID | Decisão | Status |
|----|---------|--------|
| D1 | Dataset fonte = `AISE-TUDelft/MOSAIC-agentic-3m` (`Repositories_{Claude,Codex,Copilot,Devin,Jules}`, sem `Human`) | vigente |
| D2 | Abordagem **sem token**: partial clone via git em vez de GitHub API | vigente |
| D3 | Escopo de download: **todos** os `.md`; detecção de instrução só na **raiz** | vigente |
| D4 | Primeira rodada em **amostra** (`--limit 500`, `seed 42`) antes de escala total | concluída |
| D5 | Artigos: PDFs **fora** do git (`papers/`); manifest versionado (`papers/MANIFEST.md`) | vigente |

Rationale completo e alternativas consideradas: `DECISIONS.md`.

## Papers e contexto

- PDFs: `papers/` (gitignored). Manifest versionado: `papers/MANIFEST.md`.
- Paper de base: Popescu et al. (2026) — dataset MOSAIC-agentic-3m; *search
  signals* para atribuir PRs a agentes (branch prefix, author bots, watermarks).

## Roadmap

- [ ] Rodada completa do dataset (`--limit 0`)
- [ ] Análise de conteúdo dos arquivos de instrução (temas, comandos, regras)
- [ ] v2: detecção em subpastas (`agents/`, `.github/instructions/`, `.claude/`)
- [ ] Cruzamento com outros datasets (ex.: `disler/agent-contexts`) p/ estimar cobertura