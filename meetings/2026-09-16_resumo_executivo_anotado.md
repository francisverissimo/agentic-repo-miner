# Reunião 2026-09-16 — Resumo Executivo Anotado

| Campo | Valor |
|---|---|
| **Participantes** | Awdren de Lima Fontão (orientador) · Francis de Souza Verissimo Ferreira |
| **Duração** | 31 min 44 s |
| **Transcrição original** | `meetings/2026_09_16 16_06 GMT-04_00 - Transcript.md` |
| **Resumo gerado** | 2026-10-05 (agente OpenCode), com comentários do aluno |

> O orientador pediu que o aluno lesse a transcrição e **adicionasse comentários**
> nela. Este documento é a versão "anotada": resumo executivo + comentários do
> aluno + perguntas em aberto para a próxima reunião.

---

## 1. Resumo executivo (o que foi decidido)

1. **Redirecionamento do mestrado:** objetivo passa a ser **caracterizar
   indicadores e manifestações de dívida de intenção** em repositórios que
   trabalham com agentes, a partir dos arquivos `.md` de instrução/contexto.
2. **Construto teórico:** intenção = **objetivos + restrições + razões**
   (teoria consolidada; o orientador mandará as **perguntas de operacionalização**
   dessas dimensões).
3. **Pipeline acordado:** dataset do paper → filtrar repositórios com atividade
   de agentes (heurísticas) → recuperar os `.md` → categorizar o conteúdo →
   *(fase futura)* extração LLM do construto → *(fase futura)* evolução temporal
   da intenção.
4. **Tarefa urgente da semana (C1):** pegar o paper/dataset, replicar a
   sistemática e rodar um script que **recupera só os `.md`** — "só isso que me
   importa".
5. **Expectativa:** *"dos 860 repositórios a gente vai usar só 300"* (número a
   recalibrar — ver comentários).
6. **Processo:** comentar a transcrição até sexta; chegar na reunião semanal com
   um "slidezinho" de evolução (dataset → MDs → heurísticas → resultado);
   autonomia mensurável; **mestrado é sobre entendimento, não sobre o script**.

---

## 2. Checklist de tarefas (estado atual)

- [x] Obter o dataset do paper-base (MOSAIC-agentic-3m) — **30.744 repos únicos**
- [x] Implementar o miner (v0.1: só raiz → v0.2: multi-sinal via heurísticas)
- [x] Rodar amostra de validação (500, seed 42) → **390 adotantes** · 14.633 `.md`
- [x] Recuperar os `.md` dos adotantes (dado pronto para a análise de conteúdo)
- [x] Registrar objetivo/RQs no `PROTOCOLO.md` *(este documento)*
- [ ] **Validar RQs com o orientador** (próxima reunião)
- [ ] Receber perguntas de operacionalização (objetivos/restrições/razões)
- [ ] Rodada completa (`--limit 0`)
- [ ] Validação manual de precisão das heurísticas (antes de escalar)
- [ ] Análise de conteúdo dos `.md` (taxonomia) + extração LLM (fase seguinte)
- [ ] Análise de evolução temporal (dívida de intenção)

---

## 3. Anotações e comentários do aluno sobre a transcrição

### 3.1 Vitória e preocupação (início da reunião)
- **Transcrição:** aceleração ~50% do tempo em migração; ~70% das alterações por
  IA; contraparte: dívida de integração rápida → dívida cognitiva/de abstração.
- **Comentário:** a reunião reformulou a motivação: a preocupação não é a
  velocidade, e sim a **compreensão** (as equipes perdem o entendimento do que
  está no código). Foi esse o gancho que o orientador usou para conectar com
  dívida de intenção. Vou guardar isso para a introdução do texto.

### 3.2 Construto de intenção
- **Transcrição:** "intenção é teoricamente composta por objetivos, restrições
  (constraints) e razões (rationales)"; exemplo do orientador: objetivo "ir para
  a Europa" + restrição "orçamento" + razão "aprender idioma/visitar
  universidade".
- **Comentário:** importante **não inventar o construto** — a definição vem da
  teoria. No `PROTOCOLO.md`, deixei uma "definição de trabalho" de **dívida de
  intenção** (lacuna entre a intenção necessária e a comunicada/capturada pelos
  artefatos) e 3 hipóteses de manifestação (H1: restrições raramente
  especificadas; H2: rationales raros; H3: contexto desatualizado vs código).
  *Pergunta para o orientador:* essa definição de trabalho faz sentido como
  ponto de partida?

### 3.3 Pipeline e escopo
- **Transcrição:** o orientador pediu para **filtrar** os repos do paper que
  tenham atividade de agentes (heurísticas) e **recuperar só os `.md`**, depois
  categorizar ("esse aqui é mais objetivo/plano, esse é constraints/ADR, esse é
  rationale/hardness").
- **Comentário:** isso é exatamente o que o projeto já fez **e o que vem pela
  frente**: a etapa de recuperação está concluída (v0.1/v0.2); a **categorização
  de conteúdo** é a próxima (taxonomia de conteúdo + o construto dele). Decisão
  minha de desenho (a validar): analisar conteúdo apenas nos adotantes com
  **arquivo de instrução explícito** (111 dos 390 adotantes na amostra), não nos
  390 — candidata a
  D7.

### 3.4 Números: "860 → 300"
- **Transcrição:** "acho que são 860 repositórios pra esse outro paper... dos 860
  a gente vai usar só 300".
- **Comentário:** conferi o dataset real: são **30.744 repositórios únicos** nos
  5 agentes. O "860" deve ser de outro recorte (talvez do paper que ele
  procurava, ou de uma contagem antiga). **Preciso esclarecer com o orientador**
  qual universo ele tinha em mente. Na nossa amostra de 500, os adotantes foram
  390 (proporcionalmente ~78%) — proporção alta porque o universo já é composto
  por repos onde agentes abriram PRs (viés de seleção do dataset).

### 3.5 "O mestrado não é o script"
- **Transcrição:** "seu mestrado não é implementação, é o que a gente vai usar...
  não é para ficar duas semanas implementando o script".
- **Comentário:** o script cumpre o papel de meio. Para a reunião: mostrar
  **resultados de uso** (amostra, sinais, `.md` baixados), não gastar tempo em
  engenharia de script. Isso respalda o meu plano de **pivotar para análise de
  conteúdo** agora.

### 3.6 Replicabilidade (exemplos citados)
- **Transcrição:** o orientador citou os trabalhos do Arthur (mineração,
  passos replicáveis) e o próprio estudo dele de Stack Overflow como exemplos de
  sequência bem documentada ("pega o repositório, roda tal ferramenta... isso é
  replicável").
- **Comentário:** nosso repo já institucionalizou isso (AGENTS.md, CHANGELOG,
  seeds, heuristics versionado, README/`PROTOCOLO.md`). É um **ponto de venda**
  na próxima reunião.

### 3.7 Próximas fases que o orientador antecipou
- **Transcrição:** análise das **mudanças nos MDs** ("como a intenção foi
  mudando"), correlação com produção de código, e a hipótese de os MDs de
  contexto **ficarem desatualizados** enquanto o código acelera.
- **Comentário:** no "Agent READMEs" (paper que ele citou como fonte da
  estratégia de pegar `.md`), a RQ2 deles já mostra que context files evoluem em
  **rajadas curtas com adições incrementais** — motivação empírica direta para a
  nossa RQ3. Vou usar isso na justificativa.

---

## 4. Perguntas em aberto para a próxima reunião

1. O universo a considerar é o MOSAIC-agentic-3m inteiro (30.744 repos) ou um
   recorte específico (ex.: "~860")? Qual critério?
2. As RQs do `PROTOCOLO.md` (RQ1 adoção, RQ2 conteúdo, RQ3 evolução) estão
   adequadas? O que corrigir para espelhar o "caracterizar indicadores e
   manifestações"?
3. As **perguntas de operacionalização** das dimensões (objetivos/restrições/
   razões) — pode compartilhar na reunião?
4. D7 (corpus de conteúdo = adotantes com arquivo de instrução explícito): ok?
5. Validação de precisão das heurísticas: o orientador prefere que eu documente
   primeiro (amostra manual) ou seguimos para a análise de conteúdo e deixo a
   validação como trabalho futuro?

---

## 5. Referências citadas na dedução deste resumo

- Transcrição original: `meetings/2026_09_16 16_06 GMT-04_00 - Transcript.md`
- Protocolo: `PROTOCOLO.md` (rascunho v0.1, 2026-10-05)
- Papers de contexto: `papers/MANIFEST.md` (entrada 2026-10-05)