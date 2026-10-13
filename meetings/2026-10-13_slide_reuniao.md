# Slide da reunião semanal — versão elaborada

> **Data:** 2026-10-13 (semana da reunião)
> **Formato:** 12 slides em Markdown, separados por `---`. Cada bloco = 1 slide
> do Google Slides. Nota de locutor + tempo estimado ao final de cada slide.
> **Duração sugerida:** ~10 minutos de fala.
> **Fontes dos números:** `data/manifest.csv` (amostra 500/seed 42, v0.2) ·
> `CHANGELOG.md` · `PROTOCOLO.md`.

---

## 0 · Capa

**Dívida de intenção em repositórios que trabalham com agentes de IA**

*Caracterizando indicadores e manifestações a partir dos arquivos de contexto (`.md`)*

Aluno: Francis de Souza Verissimo Ferreira
Orientador: Prof. Dr. Awdren de Lima Fontão (UFMS)
Reunião semanal · out/2026

**Nota de locutor (30 s):** *"Na última reunião o mestrado foi redirecionado
para caracterizar dívida de intenção. Hoje trago três coisas: onde o objetivo
agora está registrado (PROTOCOLO.md), os números da coleta que já rodou, e umas
decisões que preciso validar com você."*

---

## 1 · Motivação — a vitória e a preocupação

| A vitória (o que os agentes trazem) | A preocupação (o que pode custar) |
|---|---|
| ~50% menos tempo em tarefas como migrações | Aceleração ≠ compreensão |
| ~70% das alterações de código feitas por IA | Dívida de integração rápida → **dívida cognitiva**: a equipe deixa de entender o que está no código |

*(números como discutidos na reunião de 16/09, ex. experiência relatada do paper do Google)*

**Ponte para o estudo:** os arquivos de contexto (AGENTS.md, CLAUDE.md...) são a
**memória escrita da intenção** de um projeto. Se eles desatualizam enquanto o
código acelera, a intenção se perde — é isso que queremos medir.

**Nota de locutor (1 min):** devolver o raciocínio do orientador com as palavras
dele mostra escuta e ancora toda a motivação do texto.

---

## 2 · Construto — intenção (teoria, não inventei)

> **Intenção = objetivos + restrições (constraints) + razões (rationales)**

- Teoria consolidada (não é construto novo — o orientador indicou a base);
- **Dívida de intenção** (definição de trabalho a validar): *a lacuna entre a
  intenção necessária para o projeto e a intenção que os artefatos comunicam*.

**Hipóteses de manifestação (a testar):**

| # | Hipótese | Evidência externa inicial |
|---|---|---|
| H1 | Restrições não-funcionais **raramente especificadas** | Agent READMEs: security 14,8% · performance 14,5% |
| H2 | **Racional (rationale)** é raro (ADR é a exceção) | — (a medir) |
| H3 | Contexto **fica desatualizado** vs. código acelerado | Agent READMEs: evolução em rajadas curtas |

**Nota de locutor (1 min):** "essa definição de trabalho faz sentido como ponto
de partida? Onde você ajustaria?"

---

## 3 · Questões de pesquisa — registradas no `PROTOCOLO.md`

**RQ abrangente:** quais **indicadores e manifestações de dívida de intenção**
podem ser caracterizados em repositórios que trabalham com agentes, a partir dos
arquivos `.md`?

| RQ | Pergunta | Onde está no pipeline |
|---|---|---|
| **RQ1 · Adoção** | Quais repos do universo trabalham com agentes e quais sinais caracterizam isso? | ✅ basicamente respondida (amostra: 390/500) |
| **RQ2 · Conteúdo** | O que os `.md` comunicam em termos de objetivos, restrições e razões? | ▶ próxima fase |
| **RQ3 · Evolução** | Como o contexto evolui vs. a atividade de código? | ⏳ fase futura |

**Nota de locutor (30 s):** responder ao "não achei onde você registrou o
objetivo" — *"criei o PROTOCOLO.md, versionado, com objetivo, construto, RQs e
método"*.

---

## 4 · Método — pipeline completo (estado de cada etapa)

```
1. UNIVERSO ──► 2. FILTRO DE ADOÇÃO ──► 3. CORPUS DE CONTEÚDO ──► 4. ANÁLISE
dataset          heurísticas (Robbes      adotantes com arquivo      RQ2 conteúdo
MOSAIC-3m        et al.) heuristics.json   de instrução explícito    (LLM + humano)
30.744 repos     v1.0.0 · sem API ·       = 111 na amostra          RQ3 evolução
    ✓              partial clone ✓            ✓ (D7, a validar)        ▶
```

- **Sem token/API** (partial clone via git) — decisão D2;
- **Replicável:** `--seed`/`--limit` registrados, parquet cacheados,
  heuristics.json versionado (v1.0.0).

**Nota de locutor (1 min):** mostrar que a fundação é replicável — é o estilo
que o orientador valoriza (trabalho do Arthur/Stack Overflow dele).

---

## 5 · Universo — 30.744 vs. a estimativa "~860"

**Expectativa da reunião 16/09:** *"dos 860 repositórios, a gente vai usar ~300"*

**O que o dataset real contém:** **30.744 repositórios únicos**

| Agente | Repos (únicos) |
|---|---|
| Claude | 6.836 |
| Codex | 8.752 |
| Copilot | 8.173 |
| Devin | 2.652 |
| Jules | 4.916 |

**Na amostra (500):** 390 adotantes (~78%) — proporção alta porque o dataset já
vem filtrado para repos onde agentes abriram PRs (viés de seleção do dataset).

**Pergunta ao orientador:** *qual recorte você tinha em mente quando falou
"~860"? Consideramos o universo inteiro?*

**Nota de locutor (1 min):** alinhar expectativa com cuidado — "número não é
erro meu nem seu; é um recorte diferente que preciso entender".

---

## 6 · Resultados da amostra (500 · seed 42)

| Resultado | Qtd | % |
|---|---|---|
| **Adotantes** (todos os `.md` baixados) | 390 | 78% |
| Erros (privados/removidos) | 78 | 16% |
| Sem sinais de adoção | 32 | 6% |
| **Total** | 500 | 100% |

- **14.633 arquivos `.md`** baixados · ~188 MB
- Por repo: **média 37,5** · **mediana 4** · máx 2.141 (1 repo com 3.372 pulado
  por limite — registrado como erro)
- Cada `.md` é uma **fonte em potencial de intenção** para a análise

**Nota de locutor (30 s):** números por que importam — "é o insumo da análise de
conteúdo, não um fim em si".

---

## 7 · Sinais de adoção — como detectamos (sobrepostos)

| Sinal | Adotantes | |
|---|---|---|
| Co-author/author em **commits** | 287 | |
| Prefixo de **branch** (`codex/`, `copilot/`, `devin/`...) | 250 | |
| **Arquivo** de instrução na raiz | 107 | |
| **Dir** de convenção na raiz (`.claude/`...) | 50 | |
| Subpasta conhecida (`.github/instructions/`) | 7 | |
| **Multi-sinal** (≥2 sinais) | 269 (69%) | ✔ robustez |

**Adotantes por agente (repos podem estar em >1 tabela):**
Copilot 114 · Codex 114 · Claude 90 · Jules 45 · Devin 37

**Insight:** arquivo de instrução **nunca aparece sozinho** — sempre acompanha
commit/branch → context file é o "final" da adoção madura.

**Nota de locutor (1 min):** afirmar o insight como observação, não como
conclusão definitiva (validação manual vem depois).

---

## 8 · Corpus de conteúdo (decisão de desenho — a validar, candidata a D7)

```
390 adotantes (amostra)
  └── 111 com arquivo de instrução explícito  ← corpus da análise de conteúdo
        ├── 104 na raiz  (AGENTS.md, CLAUDE.md, GEMINI.md, ...)
        └──   7 em .github/instructions/
```

**Por que 111 e não 390?** Adotantes detectados *só* por commit/branch **não têm
arquivo de contexto** → não há "intenção escrita" para analisar.

**Pergunta ao orientador:** *faz sentido fixar o corpus de conteúdo nos 111
repos com arquivo de instrução?* *(Ou usar subamostra/estratificação?)*

**Nota de locutor (1 min):** decisão minha de desenho, aberta a revisão —
pedir que ele aponte os problemas antes de eu investir na rodada completa.

---

## 9 · Próximos passos (nas próximas semanas)

| # | Atividade | Status |
|---|---|---|
| 1 | Validar protocolo + decisões com o orientador | **hoje** |
| 2 | Rodada completa (`--limit 0` · 30.744 repos · `--resume`) | a executar |
| 3 | Validação de precisão das heurísticas (~30 repos/sinal, manual) | a executar |
| 4 | **Piloto de análise de conteúdo** (10–15 arquivos de instrução) | a executar |
| 5 | Rotulagem LLM em escala + validação humana (Cohen's Kappa) | fase RQ2 |

**Dúvida de priorização:** rodar a validação de precisão *antes* da rodada
completa (mais seguro) ou começar o piloto de conteúdo em paralelo?

**Nota de locutor (1 min):** pedir opinião de priorização — mostra autonomia com
checagem de rota.

---

## 10 · Perguntas ao orientador

1. **Universo:** "~860" era qual recorte? Universo inteiro (30.744) faz sentido?
2. **RQs:** RQ1/RQ2/RQ3 (PROTOCOLO.md) espelham "caracterizar indicadores e
   manifestações"? O que corrigir?
3. **Operacionalização:** pode nos passar as **perguntas das dimensões**
   (objetivos / restrições / razões) para calibrar a rotulagem?
4. **Corpus D7:** conteúdo só nos 111 repos com arquivo de instrução — ok?
5. **Priorização:** validação de heurísticas antes ou piloto de conteúdo em
   paralelo?

**Nota de locutor:** ouvir mais do que falar — esta reunião é de calibração, não
de apresentação de resultado.

---

## 11 · Visão de semestre (macro — para onde caminhamos)

| Fase | Conteúdo | Período |
|---|---|---|
| **1 · Dados** | universo, miner v0.2, .md baixados | ✅ concluída |
| **2 · Validação + escala** | precisão, `--limit 0`, corpus final | em andamento |
| **3 · Conteúdo (RQ2)** | taxonomia + construto + LLM + validação | semestre em curso |
| **4 · Evolução (RQ3) + escrita** | contexto vs código; texto do mestrado | próximo semestre |

**Nota de locutor (30 s):** "o mestrado não é o script — o script foi a fase 1;
o entendimento vem nas fases 3 e 4."

---

*Fonte dos números: `data/manifest.csv` (amostra 500 · seed 42 · v0.2) · `CHANGELOG.md` (2026-09-23 e 2026-10-08) · `PROTOCOLO.md` v0.1.*