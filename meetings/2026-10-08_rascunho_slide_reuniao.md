# Rascunho de slide — Reunião semanal com o orientador

> **Data:** semana de 2026-10-08 (rascunho)
> **Formato:** 7 "slides" em Markdown, separados por `---`. Basta copiar cada
> bloco para o Google Slides (ou apagar os `---` e usar como documento).
> **Nota do locutor (o que falar)**: frases curtas, números visíveis — o
> orientador pediu evolução mensurável, não script.
> Arquivo vivo: mudanças geram entrada no `CHANGELOG.md`.

---

## 0 · Capa

**Caracterizando dívida de intenção em repositórios que trabalham com agentes de IA**

Aluno: Francis de Souza Verissimo Ferreira
Orientador: Prof. Dr. Awdren de Lima Fontão (UFMS)

*(1 linha de contexto: "continuando o desenho do estudo — hoje trago o objetivo
registrado no PROTOCOLO.md, os números da mineração e as perguntas para validar".)*

---

## 1 · Objetivo (agora registrado)

> **Caracterizar indicadores e manifestações de dívida de intenção** em
> repositórios que trabalham com agentes, a partir dos arquivos `.md` que guiam
> esses agentes.

**Construto (teoria, não inventei):**
intenção = **objetivos + restrições (constraints) + razões (rationales)**

**Dívida de intenção (definição de trabalho):** a lacuna entre a intenção
*necessária* para o projeto e a intenção que os artefatos *comunicam* —
ex.: MD de contexto desatualizado, restrições que não são especificadas,
rationales perdidos.

**RQs (rascunho):** RQ1 adoção · RQ2 conteúdo · RQ3 evolução — detalhes no
`PROTOCOLO.md`

**Nota do locutor:** responder ao "não achei onde você registrou o objetivo" —
o `PROTOCOLO.md` foi criado e está versionado.

---

## 2 · Pipeline de pesquisa (onde estamos)

```
dataset (30.744 repos únicos)
      │  sinais: heurísticas (Robbes et al.) via heuristics.json v1.0.0
      ▼
adotantes (390 na amostra) ──► baixar TODOS os .md (14.633 · 188 MB)
      │
      ▼
análise de conteúdo .md (RQ2: objetivos/restrições/razões)   ← PRÓXIMO passo
      │
      ▼
evolução temporal (RQ3: contexto desatualiza vs. código)     ← fase futura
```

**Nota do locutor:** o script é só o meio — a parte científica (entendimento)
começa agora, na análise de conteúdo.

---

## 3 · Números da amostra (500 · seed 42)

| Resultado | Qtd | % |
|---|---|---|
| **Adotantes** (todos os `.md` baixados) | 390 | 78% |
| Erros (privados/removidos) | 78 | 16% |
| Sem sinais de adoção | 32 | 6% |
| **Total amostrado** | 500 | 100% |

- **14.633 arquivos `.md` baixados (~188 MB)** · média 37,5 e mediana 4 por repo
- **Corpus da análise de conteúdo (candidata D7):** 111 adotantes com **arquivo
  de instrução explícito** (104 na raiz · 7 em `.github/instructions`)

**Nota do locutor:** "dos ~860 repos que comentamos, o universo real do dataset
é 30.744; na amostra, 78% saíram adotantes — proporção alta porque o dataset já
vem filtrado para repos onde agentes abriram PRs."

---

## 4 · Como detectamos adoção (sinais, sobrepostos)

| Sinal | Adotantes |
|---|---|
| Co-author/author em **commits** | 287 |
| Prefixo de **branch** (`codex/`, `copilot/`, `devin/`...) | 250 |
| **Arquivo** de instrução na raiz (`AGENTS.md`, `CLAUDE.md`...) | 107 |
| **Dir** de convenção na raiz (`.claude/`, `.codex/`...) | 50 |
| Subpasta conhecida (`.github/instructions/`) | 7 |
| **Multi-sinal** (≥2 sinais) | 269 (69%) |

**Adotantes por agente (obs.: repos podem estar em >1 tabela do dataset):**
Copilot 114 · Codex 114 · Claude 90 · Jules 45 · Devin 37

**Nota do locutor:** sinal de arquivo nunca apareceu sozinho — sempre vem com
commit/branch. Commit e branch são, de longe, os mais frequentes.

---

## 5 · Próximos passos (o que vou fazer até a próxima reunião)

1. **Rodada completa** do dataset (`--limit 0`, 30.744 repos, com `--resume`)
   → corpus final de conteúdo
2. **Validação de precisão** das heurísticas (amostra manual ~30 repos/sinal —
   Peril 1 do paper de Robbes)
3. **Análise de conteúdo (RQ2):** taxonomia de 16 tipos de instrução (Agent
   READMEs) + construto do orientador; rotulagem LLM + validação humana com
   Cohen's Kappa (como no paper de exemplo)

**Nota do locutor:** perguntar se ele prefere que eu valide as heurísticas antes
ou siga direto para a análise de conteúdo.

---

## 6 · Perguntas para validar com o orientador

1. **Universo:** o "~860 repos" que você comentou — qual recorte era? O dataset
   real tem 30.744 repos únicos. Consideramos o universo inteiro?
2. **RQs (`PROTOCOLO.md`):** RQ1 adoção · RQ2 conteúdo · RQ3 evolução — fazem
   sentido para "caracterizar indicadores e manifestações de dívida de
   intenção"? O que corrigir?
3. **Operacionalização:** pode enviar as perguntas das dimensões (objetivos /
   restrições / razões) para começar a rotulagem do conteúdo?
4. **Corpus (candidata D7):** análise de conteúdo só nos adotantes com arquivo
   de instrução explícito (111), e não nos 390 — ok?

**Nota do locutor:** deixar o orientador falar mais — o objetivo é calibrar o
protocolo, não apresentar resultados.