# Changelog

Todas as mudanças relevantes do projeto são registradas aqui, em entradas
**datadas** (formato no espírito de
[Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/)). Idioma: PT-BR
(termos técnicos em inglês).

Estrutura de cada entrada: **Contexto** (origem: agente, orientador, novo
paper, mudança de dataset...) · **Adicionado / Alterado / Removido** ·
**Decisão** (referência D# em `DECISIONS.md`, quando aplicável) ·
**Execuções** (comandos, seeds, resultados) · **Em aberto**.

---

## [2026-09-20] — Documentação do projeto + organização de papers

**Contexto:** necessidade de garantir **continuidade** quando o projeto for
manipulado por outros agentes (Claude Code, Kiro, etc.); definição de política
para versionamento de artigos PDF.

**Adicionado:**
- `AGENTS.md` — contrato central para agentes: estado atual, regras
  obrigatórias, decisões vigentes, papers e roadmap.
- `CHANGELOG.md` — este log datado.
- `DECISIONS.md` — registros ADR (D1–D5).
- `papers/MANIFEST.md` — metadados/links dos artigos (versionado).

**Alterado:**
- PDF do paper-base movido da raiz para `papers/` (pasta ignorada no git).
- `.gitignore` agora inclui `papers/`.
- `README.md` documenta a política de artigos.

**Decisão:** D5 — artigos: PDFs **fora** do git; manifest versionado.

**Em aberto:** nenhum.

---

## [2026-09-19] — Implementação inicial do miner (v0.1)

**Contexto:** início do projeto de pesquisa de mineração de repositórios
(*MSR*). Paper de base e dataset escolhidos (D1). Orientação: script simples
que baixa `.md` de repositórios com `AGENTS.md` e variações por agente.

**Adicionado:**
- `miner_agents.py` — pipeline: parquet (HF) → dedupe → amostra → *partial
  clone* via git → detecção de instruções na raiz → download de todos os `.md`.
- `README.md`, `requirements.txt`, `.gitignore`.

**Decisões:** D2 (sem token → partial clone), D3 (todos os `.md`; detecção na
raiz), D4 (primeira rodada em amostra).

**Execuções:**
- Teste `--limit 20 --seed 42 --workers 4`: 5 repos com instrução
  (`AGENTS.md` 4, `CLAUDE.md` 2), 295 `.md` baixados, 0 erros.
- Rodada `--limit 500 --seed 42 --workers 5`: 106 repos com instrução
  (`CLAUDE.md` 71, `AGENTS.md` 55, `GEMINI.md` 4); 6.781 `.md` baixados
  (96 MB); 77 erros = repos hoje privados/removidos (não quebram a execução).

**Em aberto:** rodada completa (`--limit 0`), análise de conteúdo dos
arquivos de instrução, detecção em subpastas.