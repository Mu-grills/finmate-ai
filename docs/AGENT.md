# FinMate AI — Documentação do Agente

## Visão geral
O FinMate AI é um assistente conversacional de relacionamento financeiro (educativo), guiado por IA generativa (Gemini) e boas práticas de UX.  
Ele combina:
- Conversa em linguagem natural
- Base de conhecimento (Markdown) com busca simples
- Simulações financeiras demonstrativas (Python)
- Memória de contexto na sessão do usuário (Streamlit session_state)

> Aviso: o conteúdo é educativo e não substitui aconselhamento financeiro profissional.

---

## Objetivos do agente
1. Ajudar o usuário a entender conceitos e produtos financeiros de forma simples.
2. Sugerir caminhos de decisão com base em critérios práticos (prazo, objetivo, risco).
3. Oferecer simulações demonstrativas para apoiar entendimento (ex.: juros compostos, reserva de emergência).
4. Manter a conversa contextualizada com histórico recente.

---

## Entradas e saídas
### Entrada
- Texto do usuário via `st.chat_input`

### Saída
- Resposta em 5 blocos:
  1) Resumo (1–2 linhas)  
  2) O que entendi do objetivo do usuário  
  3) Opções (2–4) com prós e contras  
  4) Dica de tomada de decisão (critério simples)  
  5) Próximo passo (uma ação curta)

---

## Componentes do sistema
### 1) UI (Streamlit)
- `app.py`: chat UI, memória de sessão e controles (debug).

### 2) Memória de conversa
- `st.session_state.messages`: armazena turnos de usuário/assistente.
- Para evitar “prompt gigante”, apenas os últimos turnos relevantes são enviados ao modelo.

### 3) Base de conhecimento
- Pasta `knowledge_base/` com arquivos `.md`.
- `src/retrieval.py`: busca trechos relevantes (keyword scoring) e fornece contexto ao agente.

### 4) Ferramentas de cálculo (simulações)
- `src/calculos.py`: funções puras e testáveis:
  - `juros_compostos(aporte_inicial, taxa_mensal, meses)`
  - `reserva_emergencia(gasto_mensal, valor_reserva)`

- `src/tooling.py`: detecta intenção de simulação e extrai valores de forma simples.

### 5) Agente (prompt + geração)
- `src/agent.py`:
  - Define persona e regras
  - Monta prompt com: estilo + contexto da base + histórico + resultado de cálculos
  - Chama Gemini via `google-genai`

---

## Regras de segurança e UX
- Não solicita dados sensíveis (senha, cartão, agência/conta).
- Sempre inclui aviso de caráter educativo.
- Se faltar dado para simulação, faz pergunta curta e dá exemplo de como informar.

---

## Limitações conhecidas
- Retrieval por palavras-chave (não usa embeddings).
- Extração de números é heurística; entradas muito complexas podem falhar.
- O projeto prioriza clareza e estrutura (iniciante) em vez de máxima precisão.
