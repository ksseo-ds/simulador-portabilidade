from flask import Flask, render_template, request, redirect, url_for
from logica.calculadora import OperacaoPortabilidade
from datetime import datetime
from decimal import Decimal


app = Flask(__name__)

@app.route('/')
def index():
    return redirect(url_for('simulador_portabilidade'))

@app.route('/simulador', methods=['GET','POST'])
def simulador_portabilidade():
    resultado = None
    nova_parcela = prazo = juros = data_pagamento_str = None
    contratos = []
    dados_contratos=[]
    parcelas = []

    if nova_parcela is not None:
        parcela_total = nova_parcela + sum(parcelas)
    else:
        parcela_total = 0

    if request.method == 'POST':
        try:
            nomes_bancos = [n for n in request.form.getlist('nome_banco')]
            num_contratos = [n for n in request.form.getlist('num_contrato')]
            parcelas = [Decimal(p) for p in request.form.getlist('valor_parcelas')]
            parcela_total = parcela_total 
            saldos = [Decimal(s) for s in request.form.getlist('saldos')]
            nova_parcela = Decimal(request.form.get('nova_parcela'))
            prazo = int(request.form.get('prazo'))
            juros = Decimal(request.form.get('juros'))
            data_pagamento_str = request.form.get('data_pagamento')
            data_pagamento = datetime.strptime(data_pagamento_str, "%Y-%m-%d").date()

            # cria a operação lá na Calculadora
            operacao = OperacaoPortabilidade(
                ajuste_margem=nova_parcela,
                prazo=prazo,
                juros_mensal=juros,
                data_pagamento=data_pagamento,
                saldos=saldos,
                parcelas=parcelas
            )

            resultado = operacao.calcular_troco()
            contratos = list(zip(parcelas, saldos)) # necessário para não apagar os dados preenchidos dos contratos adicionados
            
            
            for banco, contrato, parcela, saldo in zip(nomes_bancos, num_contratos, parcelas, saldos ):
                dados_contratos.append(
                    {
                        'nome_banco': banco,
                        'num_contrato': contrato,
                        'parcela':parcela,
                        'saldo':saldo

                    })
        except Exception as e:
            resultado = {'erro': f'Erro ao calcular: {str(e)}'}

    # esse return é necessário para não apagar os dados preenchidos antes dos contratos
    return render_template(
        'simulador.html',
        dados_contratos=dados_contratos,
        resultado=resultado,
        nova_parcela = nova_parcela,
        parcela_total = parcela_total,
        prazo=prazo,
        juros=juros,
        data_pagamento=data_pagamento_str,
        contratos=contratos
    )



if __name__ == '__main__':
    app.run(host ="0.0.0.0", port=5000, debug=True)
