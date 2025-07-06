from flask import Flask, render_template, request
from logica.calculadora import OperacaoPortabilidade
from datetime import datetime
from decimal import Decimal


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('resultado.html')

@app.route('/complexo', methods=['GET','POST'])
def complexo():
    resultado = None
    nova_parcela = prazo = juros = data_pagamento_str = None
    contratos = []
    dados_contratos=[]

    if request.method == 'POST':
        try:
            nomes_bancos = [n for n in request.form.getlist('nome_banco')]
            num_contratos = [n for n in request.form.getlist('num_contrato')]
            parcelas = [Decimal(p) for p in request.form.getlist('valor_parcelas')]
            saldos = [Decimal(s) for s in request.form.getlist('saldos')]
            nova_parcela = Decimal(request.form.get('nova_parcela'))
            prazo = int(request.form.get('prazo'))
            juros = Decimal(request.form.get('juros'))
            data_pagamento_str = request.form.get('data_pagamento')
            data_pagamento = datetime.strptime(data_pagamento_str, "%Y-%m-%d").date()

            # cria a operação lá na Calculadora
            operacao = OperacaoPortabilidade(
                nova_parcela=nova_parcela,
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
        'complexo.html',
        dados_contratos=dados_contratos,
        resultado=resultado,
        nova_parcela=nova_parcela,
        prazo=prazo,
        juros=juros,
        data_pagamento=data_pagamento_str,
        contratos=contratos
    )


@app.route('/calcular', methods=['GET', 'POST'])
def calcular():
    resultado = None
    nova_parcela = prazo = juros = data_pagamento_str = None
    contratos = []
    dados_contratos=[]

    if request.method == 'POST':
        try:
            nomes_bancos = [n for n in request.form.getlist('nome_banco')]
            num_contratos = [n for n in request.form.getlist('num_contrato')]
            parcelas = [Decimal(p) for p in request.form.getlist('valor_parcelas')]
            saldos = [Decimal(s) for s in request.form.getlist('saldos')]
            nova_parcela = Decimal(request.form.get('nova_parcela'))
            prazo = int(request.form.get('prazo'))
            juros = Decimal(request.form.get('juros'))
            data_pagamento_str = request.form.get('data_pagamento')
            data_pagamento = datetime.strptime(data_pagamento_str, "%Y-%m-%d").date()

            # cria a operação lá na Calculadora
            operacao = OperacaoPortabilidade(
                nova_parcela=nova_parcela,
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
        'complexo.html',
        dados_contratos=dados_contratos,
        resultado=resultado,
        nova_parcela=nova_parcela,
        prazo=prazo,
        juros=juros,
        data_pagamento=data_pagamento_str,
        contratos=contratos
    )

if __name__ == '__main__':
    app.run(debug=True)