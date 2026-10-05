# PROTOCOLO DE PESQUISA — Dívida de Intenção em Repositórios que Trabalham com Agentes de IA

> **Status:** rascunho **v0.1** (2026-10-05) — documento vivo, para **validação com o
> orientador** antes da próxima reunião.
> Este é o registro formal do **objetivo e das questões de pesquisa** do mestrado
> (resposta direta ao "não achei onde você registrou o objetivo"). Mudanças aqui
> geram entrada datada no `CHANGELOG.md`.

## 1. Objetivo

**Objetivo geral**

Caracterizar **indicadores e manifestações de dívida de intenção** em
repositórios que trabalham com agentes de IA, a partir da análise dos arquivos
de contexto (`.md`) que guiam esses agentes.

**Objetivos específicos**

- **OE1 — Corpus:** estabelecer o conjunto de repositórios que *realmente*
  trabalham com agentes dentro do universo do dataset (detecção multi-sinal).
- **OE2 — Conteúdo:** extrair e categorizar o conteúdo dos arquivos de contexto
  segundo o construto de intenção (objetivos, restrições, razões).
- **OE3 — Evolução:** analisar como esses arquivos evoluem ao longo do tempo em
  relação à atividade de código do repositório (fonte da dívida).

## 2. Contexto e justificativa

- **A vitória (segundo o aluno):** agentes aceleram a produção de código — ex.:
  paper do Google reporta ~50% menos tempo em migrações, com ~70% das alterações
  feitas por IA.
- **A preocupação (em aberto na pesquisa):** a aceleração acumula **dívida de
  integração → dívida cognitiva → dívida de intenção e de abstração** das
  equipes (compreensão).
- **A lacuna:** os arquivos de contexto (`AGENTS.md`, `CLAUDE.md`, ...) são o
  "contrato" entre o projeto e o agente — definem objetivos, restrições e razões
  em linguagem natural. Sabe-se pouco sobre o que eles de fato comunicam e se
  acompanham o código. Evidências iniciais ("Agent READMEs", 2026): evoluem em
  **rajadas curtas** (muitas adições pequenas) e **raramente especificam
  requisitos não-funcionais** (security 14,8%; performance 14,5%) — ou seja,
  comunicam pouco das *restrições* (uma das dimensões da intenção).

## 3. Construto teórico (não inventar — embasar)

- **Intenção** = **objetivos + restrições (constraints) + razões (rationales)**
  — construto consolidado em outras ciências, adotado pelo orientador como base
  teórica do estudo (reunião 2026-09-16).
- **Arquivos de contexto** = "READMEs para agentes": especificam conhecimento do
  projeto, arquitetura, comandos de build/teste, convenções e regras; são
  carregados no início da sessão do agente (Claude Code, Codex, Copilot...).
- **Dívida de intenção** (definição de trabalho a validar): a lacuna entre a
  intenção necessária para o projeto e a intenção que os artefatos comunicam ou
  capturam — ex.: arquivo de contexto desatualizado; restrições não especificadas;
  racionais (rationales) perdidos.
- **Hipóteses de manifestação (a teste):**
  - H1: a maioria dos arquivos de contexto **não especifica restrições**
    não-funcionais (segurança, performance, usabilidade);
  - H2: a **explicitação de razões/rationales** é rara (ADRs são a exceção);
  - H3: arquivos de contexto **ficam desatualizados** em relação à atividade de
    código (o código muda mais rápido que o contexto).

## 4. Questões de pesquisa (RQs — rascunho a validar)

**RQ-abrangente:** *Quais indicadores e manifestações de dívida de intenção podem
ser caracterizados em repositórios que trabalham com agentes de IA, a partir da
análise dos arquivos de contexto (`.md`)?*

| RQ | Pergunta | Motivação | Método (resumo) | Resultado esperado |
|---|---|---|---|---|
| **RQ1** | Em que medida os repositórios do universo do dataset trabalham com agentes, e quais **sinais** caracterizam essa adoção? | Definir o corpus com critério (evitar pressupor adoção onde não há) | Miner v0.2 + heurísticas (Robbes et al.), análise descritiva dos sinais, validação manual de precisão | Corpus de adotantes descrito por tipo de sinal (arquivo, dir, subpasta, commit, branch) |
| **RQ2** | O que os arquivos de contexto **comunicam** em termos de objetivos, restrições e razões? | Operacionalizar o construto de intenção no conteúdo real | Rotulagem LLM + validação humana (taxonomia 16 tipos do "Agent READMEs" + construto do orientador); Cohen's Kappa | Perfil de conteúdo: quais dimensões da intenção são comunicadas e quais são omitidas |
| **RQ3** | Como os arquivos de contexto **evoluem** ao longo do tempo em relação à atividade de código? | Testar a hipótese de dívida (contexto desatualizado vs código acelerado) | Histórico git dos arquivos de contexto (rajadas, gaps) vs. ritmo de commits/PRs do repo | Evidência de defasagem (lag) e de "mudança de intenção" entre versões |

## 5. Universo, corpus e amostra

- **Universo (D1):** dataset `AISE-TUDelft/MOSAIC-agentic-3m`, tabelas
  `Repositories_{Claude,Codex,Copilot,Devin,Jules}` (sem `Human`).
  Conferido em 2026-10-05: **30.744 repositórios únicos** (universo real — o
  orientador estimava "~860"; a esclarecer).
- **Filtro de adoção (D6):** heurísticas de Robbes et al. via `heuristics.json`
  v1.0.0 (arquivo na raiz, diretório de convenção, subpasta conhecida,
  co-author/author em commits, prefixo de branch).
- **Amostra de validação (D4):** `--limit 500 --seed 42 --workers 5`
  → 390 adotantes, 14.633 `.md` (~188 MB). Rodada completa (`--limit 0`)
  programada antes da análise de conteúdo.
- **Corpus da análise de conteúdo (proposta → candidata a D7):** repos adotantes
  com **arquivo de instrução explícito** na raiz/subpasta conhecida (guia direto
  de intenção). Na amostra: 126 repos. Deixar de fora adotantes detectados *só*
  por commit/branch evita analisar conteúdo onde não há arquivo de contexto.
  *(Validar com o orientador.)*

## 6. Coleta e preparação de dados

- **Pipeline:** `miner_agents.py` v0.2 — partial clone via git, **sem API, sem
  token (D2)**; download de **todos** os `.md` dos adotantes (D3), preservando o
  caminho relativo.
- **Manifest:** `data/manifest.csv` — 1 linha por repo, colunas `signals` e
  `heuristics_version` (versão do catálogo por execução).
- **Rastreabilidade:** parquet cacheados em `data/parquet/`; backups de manifest
  por versão (`data/manifest_v0.1.csv`).

## 7. Análise

- **RQ1 (descritiva):** distribuição de sinais por categoria; sobreposições
  (multi-sinal); sanidade vs. rodada anterior; **validação manual de precisão**
  (amostra ~30 repos por sinal → estimar falsos positivos; o paper de Robbes faz
  o mesmo — Peril 1).
- **RQ2 (conteúdo):** amostragem estratificada dos `.md` (95% confiança / ±5%
  erro, precedente do paper de exemplo); rotulagem com LLM + revisão por 2
  codificadores; **Cohen's Kappa ≥ ~0,80**; análise de presença/ausência por
  dimensão (objetivos/restrições/razões) e por tipo de instrução (16 tipos do
  "Agent READMEs").
- **RQ3 (evolução):** histórico git por arquivo de contexto (datas, rajadas,
  adições/deleções); métricas de "idade" do contexto (ex.: tempo desde a última
  alteração) vs. ritmo de commits/PRs; análise de mudança de conteúdo entre
  versões (transição de intenção).

## 8. Validação e limitações previstas

- **Heurísticas ruidosas** (Peril 1 do paper de Robbes): sensíveis a falso
  positivo (ex.: humanos chamados "Claude"; prefixo `codex/` por conveniência
  humana) → validação manual antes de escalar.
- **Observabilidade parcial:** sinais de commit varrem apenas o branch padrão;
  arquivos `.gitignore`-ados não aparecem (Peril 1: ~20% excluem guidance).
- **Snapshot vs. estado atual:** dataset é um corte de jun–ago/2025; o miner
  inspeciona o estado *atual* (78 erros = privados/removidos na amostra).
- **Viés de rotulagem LLM:** mitigado por validação humana e métricas de
  concordância (Kappa).
- **Amostra vs. universo:** números descritivos da amostra (seed 42) não devem
  ser apresentados como universo sem a rodada completa.

## 9. Replicabilidade

- Comandos, `--seed`/`--limit`/`--workers` sempre registrados no `CHANGELOG.md`.
- `heuristics.json` versionado (mudança exige novo `version`).
- Parquet cacheados; manifest versionados por rodada.
- Dados brutos (`.md`) em `data/downloads/` (gitignored) — corpus da análise.

## 10. Pendências do orientador / do aluno

- [ ] **Orientador:** validar/corrigir RQs do protocolo.
- [ ] **Orientador:** enviar as **perguntas de operacionalização** das dimensões
      (objetivos, restrições, razões).
- [ ] **Orientador:** esclarecer o "~860 repositórios" x universo real (30.744).
- [ ] **Orientador:** validar o corpus de conteúdo (candidata a D7).
- [ ] **Aluno:** rodada completa (`--limit 0`) para o corpus final de conteúdo.
- [ ] **Aluno:** validação manual de precisão das heurísticas.

## 11. Referências

1. Popescu et al. (2026) — *Investigating Autonomous Agent Contributions in the
   Wild* — dataset MOSAIC-agentic-3m. `papers/MANIFEST.md`.
2. Robbes et al. (MSR'26) — *Promises, Perils, and (Timely) Heuristics for Mining
   Coding Agent Activity* — catálogo de heurísticas (D6). `papers/MANIFEST.md`.
3. Cynthia, Das, Roy (MSR'26) — *Are We All Using Agents the Same Way?* — paper
   de protocolo de exemplo (introdução e metodologia). `papers/MANIFEST.md`.
4. Chatlatanagulchai et al. (2026, TOSEM) — *Agent READMEs* — estratégia de
   coleta de context files + taxonomia de conteúdo + manutenção.
   `papers/MANIFEST.md`.
5. Fontão et al. (2018, JSERD) — *Supporting governance of mobile application
   developers...* — paper do orientador, estilo de protocolo de mineração.
   `papers/MANIFEST.md`.
6. Reunião 2026-09-16 (transcrição + resumo executivo anotado): `meetings/`.