from datetime import date
from decimal import Decimal

def calcular_juros_carencia(data_hoje: date, data_primeira_parcela: date, valor_base: Decimal, taxa_juros_mensal: Decimal) -> Decimal:
    dias = (data_primeira_parcela - data_hoje).days

    dias_carencia = max(0, dias - 30)
    
    taxa_dia = (Decimal(1) + taxa_juros_mensal) ** (Decimal('1') / Decimal('30')) - Decimal(1)

    juros = valor_base * taxa_dia * Decimal(dias_carencia)
    return juros
