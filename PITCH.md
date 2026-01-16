# FinMate AI 💳🤖

## O que é
FinMate AI é uma experiência digital de relacionamento financeiro (educativa) guiada por IA generativa (Gemini) e boas práticas de UX.  
Ele conversa em linguagem natural, responde com base em uma base de conhecimento e faz simulações simples (ex.: juros compostos e reserva de emergência), mantendo contexto de conversa.

## Por que eu construí
Construí para consolidar meu aprendizado em:
- IA generativa (Gemini)
- Python básico
- Streamlit (UX simples e funcional)
- Estrutura de projeto (docs, testes e avaliação)

## Funcionalidades
- Chat com memória de sessão (contexto)
- FAQ inteligente via base de conhecimento em Markdown
- Simulações demonstrativas:
  - Juros compostos
  - Reserva de emergência
- Respostas estruturadas com “dica de decisão” e “próximo passo”
- Modo debug: exibe trechos usados da base e resultados de cálculo

## Stack
- Python
- Streamlit
- Google GenAI SDK (Gemini)
- Markdown Knowledge Base

## Como rodar
1) `pip install -r requirements.txt`  
2) Crie `.env` com `GEMINI_API_KEY=...`  
3) `streamlit run app.py`

## Próximos passos (roadmap)
- Avaliação automatizada (dataset de perguntas e métricas)
- Testes unitários para cálculos e parsing
- Melhorar retrieval (embeddings)
- Simulação de parcelas/financiamento
