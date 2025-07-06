from decimal import Decimal

def calcular_iof(prazo_meses: int, valor_base: Decimal) -> Decimal:
    """
    Calcula o IOF com base apenas no valor base (sem carência).

    esse calculo foi feito levando em consideração quanto daria o coeficiente do IOF que pra 1 ano é 0.033730 em cima de um valor base ...

    o calculo precisa ser melhor pois o IOF tem metodologia com o desconto em cima do capital o que muda a cada pagamento de parcela.
    
    """
    ALIQ_FIXA = Decimal("0.0038")
    ALIQ_DIARIA = Decimal("0.000082")

    dias_totais = min(prazo_meses * 30, 365)
    
    iof_coef = (ALIQ_DIARIA * Decimal(dias_totais))+ALIQ_FIXA

    iof = valor_base-(valor_base/(1+iof_coef))
    print(iof_coef)

    return  iof
