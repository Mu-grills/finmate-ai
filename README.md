# FinMate AI 💳🤖
Experiência digital de relacionamento financeiro (educativa) guiada por IA generativa (Gemini) + boas práticas de UX.

> ⚠️ Aviso: conteúdo educativo. Não substitui aconselhamento financeiro profissional.

---

## ✨ O que é
O **FinMate AI** é um assistente conversacional que:
- entende perguntas em linguagem natural
- responde com base em uma **base de conhecimento** (Markdown)
- realiza **simulações demonstrativas** (Python)
- mantém **contexto** da conversa (Streamlit)
- entrega orientação com **dica de decisão** + **próximo passo**

---

## 🧠 Arquitetura (visão rápida)
- `app.py`: UI + memória + orquestração
- `src/retrieval.py`: busca simples (keyword scoring)
- `src/tooling.py`: detecção de intenção
- `src/calculos.py`: cálculos testáveis
- `src/agent.py`: prompt + Gemini

---

## 🛠️ Stack
- Python
- Streamlit
- Gemini (Google GenAI)
- Markdown KB

---

## ▶️ Como rodar localmente

![FAQ demo](assets/demo_faq.jpeg)

### 1) Instale dependências
```bash
python -m venv .venv
# Windows (PowerShell):
.venv\Scripts\Activate.ps1
pip install -r requirements.txt

```md
---

## Demo

<p align="center">
  <img src="assets/demo_faq.jpeg" alt="FAQ demo" width="48%"/>
</p>

<p align="center">
  <em>FAQ com base de conhecimento (esq.) e simulação financeira (dir.).</em>
</p>