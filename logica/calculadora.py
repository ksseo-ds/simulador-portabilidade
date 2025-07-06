from datetime import date
from decimal import Decimal
from .carencia import calcular_juros_carencia
from .iof import calcular_iof

class OperacaoPortabilidade:
    '''
    Class que recebe os dados de contratos e simulação para efetuar a lógica do calculo de troco.

    Passa pelo calculo do crédito total conforme a taxa, passa pelo calculo do IOF depois calcula a CARENCIA e depois diminui dos saldos de operações para dar o troco 
    
    '''
    
    def __init__(self, nova_parcela:Decimal, prazo, juros_mensal:Decimal, data_pagamento, saldos:Decimal, parcelas:int):
        self.nova_parcela = Decimal(nova_parcela)
        self.prazo = prazo
        self.juros_mensal = Decimal(juros_mensal) / Decimal(100)
        self.data_pagamento = data_pagamento
        self.saldos = [Decimal(s) for s in saldos]
        self.parcelas = parcelas
        self.hoje = date.today()

    def calcular_valor_base(self):
        '''
        Método para calcular o valor total do empréstimo de acordo com a parcela e o valor da taxa, para depois serem calculados os outros componentes

        '''
        
        juros = float(self.juros_mensal)
        coef = (1 - (1 + juros) ** -self.prazo) / juros
        return self.nova_parcela * Decimal(coef)

    def calcular_troco(self):
        '''
        Método da classe para calcular o Troco levando em consideração o IOF e a CARENCIA 
        não recebe argumentos
        '''
        valor_base = self.calcular_valor_base()
        saldo_total = sum(self.saldos)
        valor_base_para_iof = valor_base - saldo_total

        iof = calcular_iof(self.prazo, valor_base_para_iof)
        juros_carencia = calcular_juros_carencia(
            self.hoje, self.data_pagamento, valor_base, self.juros_mensal
        )

        troco_liquido = max(valor_base - saldo_total - juros_carencia - iof, Decimal(0))

        return {
            "parcela": round(self.nova_parcela, 2),
            "prazo": self.prazo,
            "juros": round(self.juros_mensal * 100, 2),
            "valor_total": round(valor_base, 2),
            "iof": round(iof, 2),
            "juros_carencia": round(juros_carencia, 2),
            "troco_liquido": round(troco_liquido, 2)
        }
