# miner_agents — Mineração de repositórios que trabalham com agentes de IA

Script simples para achar e baixar arquivos `.md` de repositórios que **de fato
trabalham com agentes de IA**, ou seja, que adotaram arquivos de instrução como
`AGENTS.md` (e variações por agente: `CLAUDE.md`, `COPILOT_INSTRUCTIONS.md`,
`GEMINI.md`, `OPENHANDS.md`, ...).

## Contexto (por que este script existe)

O paper *"Investigating Autonomous Agent Contributions in the Wild: Activity
Patterns and Code Change over Time"* (Popescu et al., 2026) disponibilizou um
dataset público no Hugging Face:

- **Dataset:** [`AISE-TUDelft/MOSAIC-agentic-3m`](https://huggingface.co/datasets/AISE-TUDelft/MOSAIC-agentic-3m)
- **Conteúdo:** PRs feitos por agentes (OpenAI Codex, Claude Code, GitHub
  Copilot, Google Jules, Devin) + humanos, com commits, reviews, comentários,
  issues e metadados dos repositórios.

Este script usa as tabelas `Repositories_{Agente}` para obter a **lista de
repositórios onde agentes abriram PRs**, e então verifica quais desses repos
adotaram a convenção `AGENTS.md`. Para cada repo adotante, baixa **todos os
arquivos `.md`**.

## Como funciona (tecnicamente)

Para não depender da API do GitHub (rate limit de 60 req/h sem token), o script
usa **clone parcial do git**:

1. `git clone --depth 1 --filter=blob:none --no-checkout --sparse` — baixa só a
   *árvore de nomes de arquivos* (dezenas de KB), sem conteúdo.
2. `git ls-tree -r --name-only HEAD` — lista todos os arquivos do repo
   localmente.
3. Detecta `AGENTS.md` e variantes na raiz + enumera todos os `.md`.
4. Se houver instrução de agente: `git sparse-checkout set --no-cone <...>` +
   `git checkout` materializa **somente** os `.md`.
5. Copia os arquivos para `data/downloads/{owner}__{repo}/` preservando o
   caminho relativo.

Resultado por repositório em `data/manifest.csv`.

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

## Lista de arquivos de instrução detectados

A detecção é case-insensitive e feita na **raiz** do repositório:

`AGENTS.md`, `CLAUDE.md`, `COPILOT_INSTRUCTIONS.md`, `GEMINI.md`, `OPENHANDS.md`,
`CURSOR.md`, `WINDY.md`, `Q.md`, `AMAZON_Q.md`, `DEVIN.md`, `ROO.md`, `TRAE.md`,
`CODEWISDOM.md`, `JULES.md`

> A lista vive na constante `INSTRUCTION_NAMES` no topo do script — fácil de
> estender.

## Limitações

- O dataset do paper é um snapshot (jun–ago/2025); o script inspeciona o estado
  **atual** dos repositórios.
- Detecta apenas arquivos de instrução na **raiz** (v2 pode incluir
  `agents/`, `.github/instructions/`, `.claude/`, etc.).
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