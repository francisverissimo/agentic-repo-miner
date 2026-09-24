# Decisões (Architecture Decision Records)

Registro das decisões relevantes do projeto. Formato por decisão:
**ID** · **Data** · **Status** (proposta | vigente | substituído) ·
**Contexto** · **Alternativas consideradas** · **Decisão** · **Consequências**.

> Regra: ao alterar/reverter uma decisão, atualize o status do registro e
> acrescente entrada datada no `CHANGELOG.md`. Decisões novas: novo registro
> aqui + resumo na tabela "Decisões vigentes" do `AGENTS.md`.

---

## D1 — Dataset fonte

- **Data:** 2026-09-19 · **Status:** vigente
- **Contexto:** o projeto precisava de um dataset público de repositórios com
  atividade de coding agents para minerar.
- **Alternativas consideradas:**
  - GitHub Code Search global (`filename:AGENTS.md`) — cobertura ampla, porém
    exige autenticação e tem resultados limitados/instáveis;
  - `disler/agent-contexts` (Hugging Face) — já contém AGENTS.md de milhares de
    repos, mas é *gated* e não carrega o contexto de pesquisa do paper;
  - Dataset do paper (escolhido).
- **Decisão:** usar `AISE-TUDelft/MOSAIC-agentic-3m` (Popescu et al., 2026),
  tabelas `Repositories_{Claude,Codex,Copilot,Devin,Jules}` (exclui o grupo
  `Human`, pois o objetivo são repos que trabalham COM agentes).
- **Consequências:** universo = repos da janela jun–ago/2025 do dataset; o
  estado dos repos inspecionado é o atual (hiato entre snapshot e hoje);
  cobertura limitada a quem apareceu no dataset.

---

## D2 — Abordagem sem token: partial clone via git

- **Data:** 2026-09-19 · **Status:** vigente
- **Contexto:** verificar existência de `AGENTS.md`/variantes e listar todos os
  `.md` de milhares de repos. A API do GitHub sem token permite ~60 req/h — inviável.
- **Alternativas consideradas:**
  - GitHub REST API (`/contents`, `/git/trees?recursive=1`) — 1 chamada/repo,
    porém ~60 req/h sem token e 5.000/h com token;
  - *Partial clone* via git (escolhido).
- **Decisão:** para cada repo, `git clone --depth 1 --filter=blob:none
  --no-checkout --sparse` baixa apenas a árvore de nomes (~KB); `git ls-tree -r`
  lista tudo localmente; `git sparse-checkout set --no-cone` + `git checkout`
  materializa somente os `.md`. Zero chamadas de API → sem rate limit, sem token.
- **Consequências:** ~1 s por repo (medido); necessita `git` no sistema;
  repos privados/removidos aparecem como erro (GitHub pede credenciais).

---

## D3 — Escopo de download: todos os `.md`; detecção inicialmente só na raiz

- **Data:** 2026-09-19 · **Status:** vigente, com a parte de *detecção* **substituída por D6** (2026-09-23); escopo de *download* mantido
- **Contexto:** usuário pediu "todos os arquivos .md dos repos que realmente
  trabalham com agentes (que possuem AGENTS.md e variações por agente)".
- **Alternativas consideradas:**
  - Baixar apenas os arquivos de instrução (AGENTS.md, CLAUDE.md, ...);
  - Baixar todos os `.md` do repo adotante (escolhido);
  - Instruções + README.
- **Decisão (vigente):** repo adotante = repo com sinal de agente (ver D6);
  para adotantes, baixar **todos** os arquivos com extensão `.md`/`.markdown`/`.mdown`
  do repo, preservando o caminho relativo.
- **Consequências:** volume maior de dados (96 MB na amostra de 500 da v0.1);
  subpastas conhecidas passam a qualificar a partir da v0.2 (D6).

---

## D4 — Escala da primeira rodada: amostra antes de escala total

- **Data:** 2026-09-19 · **Status:** concluída
- **Contexto:** o dataset tem dezenas de milhares de repos únicos; rodar tudo
  de primeira arriscaria horas de execução e rate limiting do GitHub.
- **Alternativas consideradas:** dataset inteiro já; só repos com PR mergeado;
  amostra aleatória pequena (escolhida).
- **Decisão:** primeira rodada com `--limit 500 --seed 42` (amostra aleatória
  reproduzível) para validar o pipeline antes de escalar.
- **Consequências:** pipeline validado com 0 erros de script; decisão de
  rodada completa (`--limit 0`) fica no roadmap.

---

## D5 — Artigos: PDFs fora do git, manifest versionado

- **Data:** 2026-09-20 · **Status:** vigente
- **Contexto:** artigos PDF são binários, não diffáveis e incham o repositório
  conforme a coleção cresce.
- **Alternativas consideradas:**
  - Versionar PDFs no git — rejeitada (bloat, diff inútil);
  - Apenas links/citações, sem cópia local — perde leitura offline;
  - PDFs em pasta ignorada + manifest versionado (escolhido).
- **Decisão:** PDFs ficam em `papers/` (ignorado por `.gitignore`); o versionado
  é `papers/MANIFEST.md`, com metadados (título, autores, ano, arXiv/DOI,
  dataset) e a contribuição de cada artigo à pesquisa.
- **Consequências:** repo leve e reproduzível (artigos re-downloadable via
  links); leitura offline preservada; gestão de contexto centralizada.

---

## D6 — Detecção multi-sinal com heurísticas de Robbes et al. (SIGNATURA v0.2)

- **Data:** 2026-09-23 · **Status:** vigente
- **Contexto:** o paper indicado pelo orientador (Robbes et al., MSR'26)
  documenta heurísticas para detectar atividade de coding agents em arquivos,
  commits, branches e PRs — e mostra que detecção só por arquivo de instrução
  na raiz **subestima** adoção (Peril 1: >40% dos adotantes não têm marcador em
  commits; ~20% excluem os arquivos de guidance via `.gitignore`).
- **Alternativas consideradas:**
  - Manter detecção v0.1 (raiz-only) e só ampliar a lista de nomes;
  - Adotar catálogo completo multi-sinal (escolhido);
  - Incluir labels de PR (rejeitado: exige GitHub API, contraria D2).
- **Decisão:** o repo é **adotante** se qualquer um destes sinais bater
  (catálogo data-driven em `heuristics.json`, versionado):
  - arquivo de instrução na raiz (lista ampliada: `AGENTS.md`, `AGENT.md`,
    `CLAUDE.md`, `copilot-instructions.md`, ...);
  - diretório de convenção na raiz (`.claude/`, `.codex/`, `.cursor/`, ...);
  - caminhos conhecidos em qualquer nível (`.github/instructions/`,
    `copilot-instructions/`, `.github/workflows/claude|copilot`, ...);
  - autor/co-author conhecido em commits (`Co-authored-by: Claude`,
    `noreply@anthropic.com`, `codex@openai.com`, ...) — HEAD grátis; histórico
    só se o HEAD não bater, via fetch sem blobs;
  - prefixos de branch remoto (`claude/`, `codex/`, `copilot/`, ...) via
    `git ls-remote` (1 chamada, sem clone).
  O escopo de download (todos os `.md` dos adotantes — D3) é mantido.
- **Consequências:** mais repos classificados como adotantes dentro do mesmo
  universo (dataset MOSAIC-agentic-3m); manifest ganha colunas `signals` e
  `heuristics_version`, permitindo quantificar o Peril 1 na nossa coleta;
  heurísticas atualizáveis sem tocar no código (mudança de `heuristics.json`
  gera entrada de CHANGELOG — Peril 4). Custos adicionais por repo: 1 chamada
  `ls-remote` + fetch profundo sem blobs quando o HEAD não tem sinal.