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

## 2026-10-05 — Papers de referência para o protocolo + contexto de conteúdo

| Campo | Valor |
|---|---|
| **Arquivo (local)** | `papers/Are We All Using Agents the Same Way? An Empirical Study of Core and Peripheral Developers’ Use of Coding Agents.pdf` |
| **Título** | Are We All Using Agents the Same Way? An Empirical Study of Core and Peripheral Developers’ Use of Coding Agents |
| **Autores** | Shamse Tasnim Cynthia, Joy Krishan Das, Banani Roy (University of Saskatchewan) |
| **Ano** | 2026 (MSR '26, Rio de Janeiro) |
| **arXiv** | arXiv:2601.20106v1 \[cs.SE\], 27 Jan 2026 |
| **Fonte** | https://doi.org/10.1145/3793302.3793377 |
| **Contribuição** | **Paper de protocolo de exemplo** (indicado pelo orientador: "veja introdução e metodologia"). Estudo empírico de 9.427 agentic PRs (Claude, Cursor, Copilot, Codex) comparando core vs peripheral developers. Metodologia-modelo: coleta via GitHub search API (branch prefix `head:codex/`, `Co-Authored-By: Claude`), filtros explícitos (≥100 stars; janela até 08/2025; exclusões de devs), classificação por experiência (80º percentil), **1 seção de método por RQ**, rotulagem GPT-4 + validação humana (amostra 95%/±5%, Cohen's Kappa 80–85%), replication package. Template para estruturar o nosso protocolo. |

| Campo | Valor |
|---|---|
| **Arquivo (local)** | `papers/Agent READMEs: An Empirical Study of Context Files for AgenticCoding.pdf` |
| **Título** | Agent READMEs: An Empirical Study of Context Files for Agentic Coding |
| **Autores** | Worawalan Chatlatanagulchai, Hao Li, Yutaro Kashiwa, Brittany Reid, Kundjanasith Thonglek, Pattara Leelaprute, Arnon Rungsawang, Bundit Manaskasemsak, Bram Adams, Ahmed E. Hassan, Hajimu Iida |
| **Ano** | 2026 (ACM TOSEM) |
| **Fonte** | https://doi.org/10.1145/3840295 |
| **Contribuição** | Estudo de **2.303 agent context files** (AGENTS.md, CLAUDE.md...) de 1.925 repos — a "estratégia para pegar os `.md`" citada pelo orientador (dataset AIDev → filtro ≥5 stars → varredura da raiz por nomes conhecidos; base da nossa detecção por arquivo). RQ1 características (arquivos longos/difíceis, hierarquia H2/H3), **RQ2 manutenção** (evoluem em **rajadas curtas com adições incrementais** — relaciona-se à dívida de intenção / MD desatualizado), **RQ3 conteúdo** (taxonomia de **16 tipos de instrução**, rotulagem LLM + validação manual). Achado-chave: **requisitos não-funcionais raramente especificados** (security 14,8%, performance 14,5%) → candidato a indicador de dívida de intenção (restrições pouco comunicadas). |

| Campo | Valor |
|---|---|
| **Arquivo (local)** | `papers/Supporting governance of mobile application developers from mining and analyzing technical questions in stack overflow.pdf` |
| **Título** | Supporting governance of mobile application developers from mining and analyzing technical questions in stack overflow |
| **Autores** | Awdren Fontão, Bruno Ábia, Igor Wiese, Bernardo Estácio, Marcelo Quinta, Rodrigo Pereira dos Santos, Arilo Claudio Dias-Neto |
| **Ano** | 2018 (Journal of Software Engineering Research and Development 6:8) |
| **Fonte** | https://doi.org/10.1186/s40411-018-0052-6 |
| **Contribuição** | **Paper do orientador** (doutorado) — referência de estilo/protocolo de estudo empírico de mineração (citado em reuniões anteriores). Estrutura: 1 RQ abrangente ("O que pode ser entendido dos três MSECOs a partir de questões técnicas no Stack Overflow?"), mineração de **1.568.377 questões**, análises comparativas (intensidade de atividade, hot-topics via LDA, questões "What/How to", unanswered, eventos), **validação com praticantes via survey** e 4 key insights + 10 estratégias de developer governance derivadas de systematic mapping (65 estudos). Espelha o desenho que o orientador espera: RQ → mineração → métricas → validação → contribuições práticas. |

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