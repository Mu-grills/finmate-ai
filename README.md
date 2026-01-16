# FinMate AI 💳🤖
Experiência digital de relacionamento financeiro (educativa) guiada por IA generativa (Gemini) + boas práticas de UX.

> ⚠️ Aviso: conteúdo educativo. Não substitui aconselhamento financeiro profissional.

---

## ✨ O que é
O **FinMate AI** é um assistente conversacional que:
- entende perguntas em linguagem natural
- responde com base em uma **base de conhecimento** (Markdown)
- realiza **simulações demonstrativas** (Python) para apoiar entendimento
- mantém **contexto** da conversa (memória de sessão no Streamlit)
- sempre entrega orientação prática com **dica de decisão** + **próximo passo**

---

## 🧩 Funcionalidades
- Chat com memória (Streamlit `session_state`)
- FAQ inteligente por base de conhecimento (`knowledge_base/*.md`)
- Simulações demonstrativas:
  - Juros compostos
  - Reserva de emergência
- Resposta estruturada:
  1) Resumo
  2) Objetivo entendido
  3) Opções com prós/contras
  4) Dica de tomada de decisão (critério simples)
  5) Próximo passo (ação curta)
- Modo debug:
  - mostrar trechos usados da base
  - mostrar resultado do cálculo

---

## 🧠 Arquitetura (visão rápida)
- `app.py`: UI + memória + orquestração
- `src/retrieval.py`: busca simples (keyword scoring) na base
- `src/tooling.py`: detecta intenção e extrai números (heurístico)
- `src/calculos.py`: funções puras (testáveis)
- `src/agent.py`: prompt + chamada ao Gemini

---

## 🛠️ Stack
- Python
- Streamlit
- Google GenAI SDK (Gemini)
- Markdown KB

---

## ▶️ Como rodar localmente
### 1) Instale dependências
```bash
python -m venv .venv
# Windows (PowerShell):
.venv\Scripts\Activate.ps1
pip install -r requirements.txt

## Demo
![FAQ demo](assets/demo_faq.png)
![Simulação demo](assets/demo_simulacao.png)
