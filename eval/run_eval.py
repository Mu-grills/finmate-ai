import os
import json
import time
from typing import Dict, Any, List, Tuple

from dotenv import load_dotenv
from tqdm import tqdm
from google import genai

from src.retrieval import retrieve_context
from src.tooling import detect_tool
from src.calculos import juros_compostos, reserva_emergencia
from src.agent import build_prompt, ask_gemini


def load_jsonl(path: str) -> List[Dict[str, Any]]:
    rows = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def has_structured_sections(text: str) -> bool:
    # Heurística: procurar sinais dos 5 blocos
    t = text.lower()
    keys = [
        "1)", "2)", "3)", "4)", "5)",
        "resumo", "opç", "proximo passo", "próximo passo", "dica"
    ]
    score = sum(1 for k in keys if k in t)
    return score >= 6  # tolerante


def has_educational_disclaimer(text: str) -> bool:
    t = text.lower()
    patterns = [
        "conteúdo educativo",
        "educativo",
        "não substitui",
        "não é recomendação financeira",
        "nao é recomendação financeira",
        "aconselhamento financeiro"
    ]
    return any(p in t for p in patterns)


def mentions_numbers_if_calc(text: str) -> bool:
    # Se houve cálculo, a resposta deveria citar números
    import re
    return bool(re.search(r"\d", text))


def length_ok(text: str, min_chars: int = 300, max_chars: int = 2500) -> bool:
    return min_chars <= len(text) <= max_chars


def run_tools_if_needed(user_msg: str) -> Tuple[str, str]:
    """
    Retorna (tool_name, calc_result_text_or_NoneAsEmpty).
    """
    tool_info = detect_tool(user_msg)
    calc_result = ""
    tool_name = tool_info.get("tool")

    try:
        if tool_name == "juros":
            args = tool_info["args"]
            if None in (args.get("aporte_inicial"), args.get("taxa_mensal"), args.get("meses")):
                calc_result = (
                    "Para simular juros compostos, preciso de: valor inicial, taxa mensal e meses.\n"
                    "Exemplo: 'Simule 1000 com 2% ao mês por 12 meses'."
                )
            else:
                r = juros_compostos(args["aporte_inicial"], args["taxa_mensal"], args["meses"])
                calc_result = (
                    f"- Simulação: juros compostos\n"
                    f"- Aporte inicial: R$ {args['aporte_inicial']:.2f}\n"
                    f"- Taxa mensal: {args['taxa_mensal']*100:.2f}%\n"
                    f"- Período: {args['meses']} meses\n"
                    f"- Montante estimado: R$ {r.montante:.2f}\n"
                    f"- Juros no período: R$ {r.juros:.2f}\n"
                )

        elif tool_name == "reserva":
            args = tool_info["args"]
            if None in (args.get("gasto_mensal"), args.get("valor_reserva")):
                calc_result = (
                    "Para calcular reserva de emergência, preciso de: gasto mensal e valor da reserva.\n"
                    "Exemplo: 'Reserva de emergência: gasto 2500 e tenho 8000'."
                )
            else:
                meses = reserva_emergencia(args["gasto_mensal"], args["valor_reserva"])
                calc_result = (
                    f"- Simulação: reserva de emergência\n"
                    f"- Gasto mensal: R$ {args['gasto_mensal']:.2f}\n"
                    f"- Reserva atual: R$ {args['valor_reserva']:.2f}\n"
                    f"- Cobertura estimada: {meses:.1f} meses\n"
                )
    except Exception as e:
        calc_result = f"Falha ao calcular: {e}"

    return tool_name, calc_result


def main():
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY não encontrada no .env")

    client = genai.Client(api_key=api_key)

    dataset = load_jsonl("eval/dataset.jsonl")
    results = []
    t0 = time.time()

    # histórico “fake” vazio (avaliamos respostas isoladas)
    history = []

    for row in tqdm(dataset, desc="Avaliando"):
        user_msg = row["user"]
        expect_tool = row.get("expect_tool")

        kb_context, scored = retrieve_context(user_msg, top_k=3)
        tool_name, calc_result = run_tools_if_needed(user_msg)

        prompt = build_prompt(
            user_msg=user_msg,
            kb_context=kb_context,
            history=history,
            calc_result=(calc_result if calc_result else None),
        )

        try:
            answer = ask_gemini(client, prompt)
        except Exception as e:
            answer = f"[ERRO_API] {e}"

        # métricas
        m_struct = has_structured_sections(answer)
        m_disc = has_educational_disclaimer(answer)
        m_len = length_ok(answer)

        # métricas condicionais
        m_calc_numbers = True
        if expect_tool in ("juros", "reserva"):
            m_calc_numbers = mentions_numbers_if_calc(answer)

        # validação de ferramenta (proxy): se detector não bateu, marca
        m_tool_match = True
        if expect_tool is not None:
            m_tool_match = (tool_name == expect_tool)

        results.append({
            "id": row["id"],
            "user": user_msg,
            "expect_tool": expect_tool,
            "detected_tool": tool_name,
            "metrics": {
                "structured_sections": m_struct,
                "educational_disclaimer": m_disc,
                "length_ok": m_len,
                "calc_mentions_numbers": m_calc_numbers,
                "tool_match": m_tool_match,
            },
            "answer_preview": answer[:240].replace("\n", " ") + ("..." if len(answer) > 240 else ""),
        })

    elapsed = time.time() - t0

    # agregação
    def rate(key: str) -> float:
        vals = [r["metrics"][key] for r in results]
        return sum(1 for v in vals if v) / max(1, len(vals))

    summary = {
        "n": len(results),
        "seconds": round(elapsed, 2),
        "rates": {
            "structured_sections": rate("structured_sections"),
            "educational_disclaimer": rate("educational_disclaimer"),
            "length_ok": rate("length_ok"),
            "calc_mentions_numbers": rate("calc_mentions_numbers"),
            "tool_match": rate("tool_match"),
        }
    }

    os.makedirs("eval/out", exist_ok=True)
    with open("eval/out/results.json", "w", encoding="utf-8") as f:
        json.dump({"summary": summary, "results": results}, f, ensure_ascii=False, indent=2)

    print("\n=== RESUMO ===")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    print("\nArquivo gerado: eval/out/results.json")


if __name__ == "__main__":
    main()
