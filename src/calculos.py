from dataclasses import dataclass

@dataclass
class ResultadoJuros:
    montante: float
    juros: float

def juros_compostos(aporte_inicial: float, taxa_mensal: float, meses: int) -> ResultadoJuros:
    """
    taxa_mensal: em decimal (ex: 0.02 = 2% ao mês)
    """
    if aporte_inicial < 0 or taxa_mensal < 0 or meses < 0:
        raise ValueError("Valores não podem ser negativos.")

    montante = aporte_inicial * ((1 + taxa_mensal) ** meses)
    juros = montante - aporte_inicial
    return ResultadoJuros(montante=montante, juros=juros)

def reserva_emergencia(gasto_mensal: float, valor_reserva: float) -> float:
    """
    Retorna quantos meses de custo fixo a reserva cobre.
    """
    if gasto_mensal <= 0:
        raise ValueError("Gasto mensal deve ser maior que zero.")
    if valor_reserva < 0:
        raise ValueError("Reserva não pode ser negativa.")

    return valor_reserva / gasto_mensal
