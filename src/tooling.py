import re
from typing import Optional, Dict, Any

def _to_float(s: str) -> Optional[float]:
    # aceita "1.234,56" ou "1234.56" ou "1234,56"
    s = s.strip()
    s = s.replace(".", "").replace(",", ".") if s.count(",") == 1 else s.replace(",", ".")
    try:
        return float(s)
    except:
        return None

def detect_tool(user_msg: str) -> Dict[str, Any]:
    """
    Retorna:
      {"tool": "juros"|"reserva"|None, "args": {...}}
    """
    text = user_msg.lower()

    # Juros compostos: palavras-chave
    if any(k in text for k in ["juros", "juros compostos", "rendimento", "montante"]):
        # tenta pegar: valor, taxa (%), meses
        nums = re.findall(r"(\d[\d\.,]*)", text)
        # heurística: primeiro número = valor, segundo = taxa, terceiro = meses
        valor = _to_float(nums[0]) if len(nums) > 0 else None
        taxa = _to_float(nums[1]) if len(nums) > 1 else None
        meses = int(_to_float(nums[2])) if len(nums) > 2 and _to_float(nums[2]) is not None else None

        # se taxa veio em %, converte para decimal
        if taxa is not None and taxa > 1:
            taxa = taxa / 100.0

        return {"tool": "juros", "args": {"aporte_inicial": valor, "taxa_mensal": taxa, "meses": meses}}

    # Reserva de emergência
    if any(k in text for k in ["reserva de emergência", "reserva emergencia", "emergência", "emergencia"]):
        nums = re.findall(r"(\d[\d\.,]*)", text)
        # heurística: primeiro número = gasto mensal, segundo = valor da reserva
        gasto = _to_float(nums[0]) if len(nums) > 0 else None
        reserva = _to_float(nums[1]) if len(nums) > 1 else None
        return {"tool": "reserva", "args": {"gasto_mensal": gasto, "valor_reserva": reserva}}

    return {"tool": None, "args": {}}
