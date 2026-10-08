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

## [2026-10-08] — Rascunho de slide da reunião + reconciliação de números (corpus D7)

**Contexto:** montar o "slidezinho" semanal pedido pelo orientador (evolução
mensurável: dataset → MDs → heurísticas → resultado). Origem: aluno + agente.

**Adicionado:**
- `meetings/2026-10-08_rascunho_slide_reuniao.md` — 7 slides em Markdown
  (capa · objetivo registrado no PROTOCOLO · pipeline · números da amostra ·
  sinais de adoção · próximos passos · perguntas ao orientador), prontos para
  copiar para o Google Slides, com notas de locutor.

**Alterado / corrigido:**
- Corpus da análise de conteúdo (candidata a D7): corrigido de **126 → 111**
  adotantes com arquivo de instrução explícito (104 na raiz · 7 em
  `.github/instructions`) — conferido contra `data/manifest.csv`
  (instrução_files não nulo entre os 390 baixados). Atualizado em
  `PROTOCOLO.md` §5 e no resumo executivo.

**Conferido (validação de números, v0.2, amostra 500/seed 42):**
- 390 adotantes (78%) · 78 erros (77 privados/removidos + 1 repo com 3.372 .md
  pulado) · 32 sem sinais; 14.633 `.md` no disco (188 MB).
- Sinais entre adotantes: commit 287 · branch 250 · arquivo raiz 107 · dir raiz
  50 · subpasta 7; multi-sinal 269 (69%).
- Adotantes por agente (repos podem estar em >1 tabela): Copilot 114 · Codex 114
  · Claude 90 · Jules 45 · Devin 37.
- Obs.: `data/manifest.csv` superconta +6 `md_downloaded` (14.639) vs. 14.633 no
  disco — slide usa o valor do disco (verificável).

**Em aberto:** validar RQs/universo/operacionalização/D7 com o orientador;
rodada completa (`--limit 0`); validação de precisão das heurísticas.

---

## [2026-10-05] — Protocolo de pesquisa + papers de referência + organização de reuniões

**Contexto:** conversa com o orientador na sexta (2026-10-02) — ele pediu para
começar a escrever o **protocolo** ("com as questões de pesquisa e etc."),
indicou o paper de exemplo *"Are We All Using Agents the Same Way?"* ("veja
introdução e metodologia") e observou que **não achou onde o objetivo estava
registrado**. Origem: orientador (paper + protocolo) e aluno (recuperação do
paper do orientador e do "Agent READMEs").

**Adicionado:**
- `PROTOCOLO.md` v0.1 — registro formal do objetivo + RQs (RQ1 adoção, RQ2
  conteúdo, RQ3 evolução) + construto teórico (intenção = objetivos + restrições
  + razões) + método, validação, limitações e replicabilidade. Rascunho para
  validação do orientador.
- `meetings/` — transcrição da reunião 2026-09-16 movida da raiz +
  `meetings/2026-09-16_resumo_executivo_anotado.md` (resumo executivo anotado,
  checklist de tarefas e perguntas em aberto — o orientador pediu comentários na
  transcrição).
- `papers/MANIFEST.md` — 3 papers novos: o de exemplo de protocolo (Cynthia,
  Das, Roy, MSR'26), o "Agent READMEs" (Chatlatanagulchai et al., TOSEM'26;
  estratégia de coleta de context files + taxonomia de conteúdo) e o paper do
  orientador (Fontão et al., 2018; estilo de protocolo de mineração).

**Alterado:**
- `AGENTS.md` — regra nova sobre `meetings/` e `PROTOCOLO.md`; estado atual e
  roadmap atualizados.

**Decisão:** nenhuma D nova; candidata **D7** (corpus de conteúdo = adotantes
com arquivo de instrução explícito) proposta em aberto no protocolo.

**Em aberto:** validar RQs + receber perguntas de operacionalização do
orientador; esclarecer universo "~860" x 30.744 repos; rodada completa
(`--limit 0`); validação manual de precisão das heurísticas; análise de conteúdo.

---

## [2026-09-23] — v0.2: detecção multi-sinal (heurísticas de Robbes et al.)

**Contexto:** paper indicado pelo orientador — *"Promises, Perils, and (Timely)
Heuristics for Mining Coding Agent Activity"* (Robbes et al., MSR'26), adicionado
em `papers/`. Decisão de usar as heurísticas dele para **melhorar a detecção**
do script atual, mantendo o mesmo dataset/universo (D1).

**Adicionado:**
- `heuristics.json` **v1.0.0** — catálogo data-driven de sinais (arquivos/dirs
  na raiz, subpastas conhecidas, co-author em commits, prefixos de branch),
  fonte = Tabela 1 do paper + convenções da v0.1. Regra de manutenção: toda
  mudança exige novo `version` + CHANGELOG.
- `miner_agents.py` v0.2: leitura do catálogo; detecção de **diretórios** na
  raiz (`.claude/`, `.codex/`, ...) via `ls-tree -r -d`; subpastas conhecidas;
  varredura de commits (HEAD grátis + `fetch --filter=blob:none --unshallow`
  quando necessário); prefixos de branch via `git ls-remote` (sem clone, sem
  API — D2 preservada); colunas novas `signals` e `heuristics_version` no
  manifest; flags `--heuristics`, `--no-commit-signals`, `--no-branch-signals`.
- Ajuste técnico: `ls-tree -r --name-only` **não lista diretórios** (validado
  empiricamente) — por isso a varredura de pastas usa `-d` em comando separado.

**Decisões:** D6 (detecção multi-sinal, vigente); D3 atualizada (escopo de
download mantido; detecção ampliada por D6).

**Papers:** entrada de Robbes et al. no `papers/MANIFEST.md`.

**Execuções:**
- Protótipo em `/tmp/opencode`: validação de mecânica (`ls-tree -d`, `ls-remote`
  multi-pattern, `--unshallow --filter=blob:none`: 4,6 s no apache/datafusion,
  14.964 commits).
- Smoke test `--limit 5 --seed 42`: 5/5 adotantes via sinais novos
  (`.kiro/`, `codex/` branch, commit `noreply@anthropic.com`, `.github/instructions/`).
- Rodada de comparação `--limit 500 --seed 42 --workers 5` (2026-09-23):
  390 repos **adotantes** (vs 106 da v0.1 → **+285**; 105 mantidos, 1 perdido
  por repo ter ficado privado) · 78 erros (repos privados/removidos) ·
  14.633 `.md` baixados (~188 MB; vs 6.781/96 MB na v0.1).
  - Sinais por categoria: arquivo raiz 107 · dir raiz 50 · subpasta 7 ·
    commit 287 · branch 250.
  - Cruzamentos: com + commit + branch 57 · sem (só commit e/ou branch) 264 ·
    **0 repos com sinal de arquivo isolado** (todo adotante por arquivo também
    tem commit ou branch — dado interessante para o orientador, dialoga com o
    Peril 1 do paper: detecção só por arquivo subestima).
  - Sanidade: contagem de arquivos na raiz (107) ≈ v0.1 (106) + nomes novos
    (`AGENT.md` 3, `CRUSH.md` 1), confirmando que a lista antiga continuaria
    com o mesmo resultado e o ganho vem dos novos sinais.

**Em aberto:** rodada completa (`--limit 0`), análise de conteúdo (taxonomia do
Promise 5), cruzamento com outros datasets, expansão de universo.

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