from src.calculos import juros_compostos, reserva_emergencia

def test_juros_compostos_basico():
    r = juros_compostos(1000, 0.02, 12)
    assert r.montante > 1000
    assert round(r.juros, 2) == round(r.montante - 1000, 2)

def test_reserva_emergencia():
    meses = reserva_emergencia(2500, 8000)
    assert meses > 3.0
    assert meses < 3.3
