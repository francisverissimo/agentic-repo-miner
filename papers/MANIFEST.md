# Manifest de Artigos (papers)

## Política

**PDFs NÃO são versionados no git.** Eles ficam em `papers/` — pasta ignorada
por `.gitignore` — apenas para leitura local. Este manifest (versionado)
registra metadados, links e a contribuição de cada artigo para a pesquisa, para
que qualquer agente/humano reproduza e entenda o contexto.

Regra ao adicionar um novo artigo:

1. Salvar o PDF em `papers/`;
2. Adicionar entrada abaixo neste manifest;
3. Registar entrada datada em `CHANGELOG.md` (origem: `novo paper`);
4. Se o paper mudar a abordagem, criar/atualizar registro em `DECISIONS.md`.

---

## 2026-09-23 — Heurísticas de detecção (indicado pelo orientador)

| Campo | Valor |
|---|---|
| **Arquivo (local)** | `papers/Promises, Perils, and (Timely) Heuristics for Mining Coding Agent Activity.pdf` |
| **Título** | Promises, Perils, and (Timely) Heuristics for Mining Coding Agent Activity |
| **Autores** | Romain Robbes, Théo Matricon, Thomas Degueule, Andre Hora, Stefano Zacchiroli |
| **Ano** | 2026 (MSR '26, Rio de Janeiro) |
| **arXiv** | arXiv:2601.18345v1 \[cs.SE\] |
| **Fonte** | https://doi.org/10.1145/nnnnnnn.nnnnnnn (proc. MSR'26) |
| **Contribuição** | Catálogo de heurísticas para detectar traços de coding agents em 5 categorias de artefatos (files, commits, branches, PRs, issues/users), com counts do GitHub (Tabela 1). Promises/Perils que moldam a metodologia: **Peril 1** (observabilidade parcial — >40% dos adotantes não têm marcador de commit; ~20% excluem arquivos de guidance via `.gitignore`), **Peril 4** (velocity — heurísticas mudam rápido, mitigação = repositório comunitário), **Promise 5** (taxonomia dos arquivos de guidance: regras, conhecimento do repo, planos de tarefa, táticas). Base da decisão **D6** (detecção multi-sinal via `heuristics.json`) e do roadmap de análise de conteúdo. |

---

## 2026-09-19 — Paper de base

| Campo | Valor |
|---|---|
| **Arquivo (local)** | `papers/Investigating Autonomous Agent Contributions in the Wild: Activity Patterns and Code Change over Time.pdf` |
| **Título** | Investigating Autonomous Agent Contributions in the Wild: Activity Patterns and Code Change over Time |
| **Autores** | Razvan Mihai Popescu, David Gros, Andrei Botocan, Rahul Pandita, Prem Devanbu, Maliheh Izadi |
| **Ano** | 2026 |
| **arXiv** | arXiv:2604.00917v1 \[cs.SE\] |
| **Dataset** | https://huggingface.co/datasets/AISE-TUDelft/MOSAIC-agentic-3m |
| **Contribuição** | Paper de base. Constrói dataset de ~110k PRs de coding agents (OpenAI Codex, Claude Code, GitHub Copilot, Google Jules, Devin) + humanos com commits/comentários/reviews/issues/files e metadados dos repos. Define *search signals* para atribuir PRs a agentes (branch prefix ex. `codex/`, author bots, watermarks no body como "Co-Authored-By: Claude"). Base da decisão D1 (dataset) e da pergunta de pesquisa deste projeto. |