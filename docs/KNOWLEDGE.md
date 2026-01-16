# FinMate AI — Base de Conhecimento

## Onde fica
A base está em `knowledge_base/` e é composta por arquivos Markdown:

- `faq.md`: termos comuns (CDI, CDB, Tesouro Direto etc.)
- `produtos.md`: descrições didáticas de produtos
- `politicas.md`: limites e políticas do assistente

---

## Como escrever (padrão recomendado)
- Títulos com `#` e `##`
- Parágrafos curtos
- Linguagem simples
- Evitar jargão sem explicação

Exemplo:

## O que é CDB?
CDB é um título emitido por bancos. Em termos simples, você empresta dinheiro ao banco e recebe juros.

---

## Boas práticas
- Sempre incluir avisos quando existir risco (ex.: cartão, rotativo, dívidas)
- Manter os textos “didáticos” e neutros
- Atualizar com base em dúvidas reais dos usuários

---

## Como o sistema usa a base
O arquivo `src/retrieval.py`:
1. lê todos os `.md`
2. divide em trechos menores (chunks)
3. pontua por palavras-chave presentes na pergunta
4. retorna os top trechos para o agente usar no prompt
