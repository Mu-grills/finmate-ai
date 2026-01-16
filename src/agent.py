from typing import List, Dict, Optional
from google import genai

MODEL = "gemini-2.5-flash-lite"

SYSTEM_STYLE = """
Você é um consultor amigável de relacionamento financeiro.
Você ajuda o usuário a entender opções e tomar decisões com segurança.

Regras:
- Tom: acolhedor, claro e prático (iniciante).
- Faça perguntas curtas se faltarem dados: objetivo, prazo, valor, tolerância a risco.
- Sempre responda com esta estrutura:

1) Resumo em 1-2 linhas
2) O que eu entendi do seu objetivo
3) Opções (2 a 4) com prós e contras
4) Dica de tomada de decisão (um critério simples)
5) Próximo passo (uma ação curta)

Limites:
- Conteúdo educativo, não é recomendação financeira profissional.
- Não solicite dados sensíveis (senhas, número de cartão, agência/conta).

Quando houver resultados de cálculo, use-os explicitamente e explique a conta de forma simples.
"""

def build_prompt(
    user_msg: str,
    kb_context: str,
    history: List[Dict[str, str]],
    calc_result: Optional[str] = None
) -> str:
    last_turns = history[-6:] if history else []
    hist_text = "\n".join([f"{m['role'].upper()}: {m['content']}" for m in last_turns])

    calc_block = f"\n\nResultados de cálculo (validados pelo sistema):\n{calc_result}\n" if calc_result else ""

    return f"""
{SYSTEM_STYLE}

Base de conhecimento (use se for relevante):
{kb_context if kb_context else "(vazio)"}

Histórico recente:
{hist_text if hist_text else "(sem histórico)"}
{calc_block}
Pergunta do usuário:
{user_msg}
""".strip()

def ask_gemini(client: genai.Client, prompt: str) -> str:
    resp = client.models.generate_content(model=MODEL, contents=prompt)
    return resp.text or ""
