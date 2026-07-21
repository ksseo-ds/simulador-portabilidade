from flask import Flask, render_template, request, redirect, url_for
from services.calculadora import OperacaoPortabilidade
from datetime import datetime,timedelta
from decimal import Decimal
from routes.investments_routes import investments_bp
from services.iof import calcular_iof_adicional_portabilidade

app = Flask(__name__)

app.register_blueprint(investments_bp)


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
    carencia_padrao = datetime.today().date() + timedelta(days=30)
    parcela_total = Decimal('0.00')

    if request.method == 'POST':
        try:
            nomes_bancos = [n for n in request.form.getlist('nome_banco')]
            num_contratos = [n for n in request.form.getlist('num_contrato')]
            parcelas = [Decimal(p) for p in request.form.getlist('valor_parcelas')]
            saldos = [Decimal(s) for s in request.form.getlist('saldos')]
            nova_parcela = Decimal(request.form.get('nova_parcela'))
            parcela_total = nova_parcela + sum(parcelas, Decimal('0.00')) # inculi o Decumal para evitar de somar com listas vazias, estava dando erro 
            prazo = int(request.form.get('prazo'))
            juros = Decimal(request.form.get('juros'))
            data_pagamento_str = request.form.get('data_pagamento')
            data_pagamento = datetime.strptime(data_pagamento_str, "%Y-%m-%d").date()
            
            indices_portados = {int(indice) for indice in request.form.getlist('operacao_portada')} # inclusão de informação para identificação de operações portadas para recalculo de IOF adicional
            operacoes_portadas = [indice in indices_portados for indice in range(len(saldos))] # percore o set para identificar se na quantidade de saldos encotnrados o indice_portado se encontra entre esses saldos, isso serve para identificar as operações oriundas de portabilidaed
          
            # cria a operação lá na Calculadora
           
            operacao = OperacaoPortabilidade(
                ajuste_margem=nova_parcela,
                prazo=prazo,
                juros_mensal=juros,
                data_pagamento=data_pagamento,
                saldos=saldos,
                parcelas=parcelas
            )

            
            contratos = list(zip(parcelas, saldos)) # necessário para não apagar os dados preenchidos dos contratos adicionados
            resultado_base = operacao.calcular_troco() # resultado com o IOF original e calculo de troco liquido, sem BITRIBUTAÇÃO
           
            
            iof_adicional = round(calcular_iof_adicional_portabilidade(
                prazo_meses = prazo,
                saldos = saldos,
                operacoes_portadas = operacoes_portadas),2)

            resultado = {
                **resultado_base,
                "iof_original":resultado_base['iof'],
                "iof_adicional":iof_adicional,
                "iof": round(resultado_base['iof'] + iof_adicional,2),
                "troco_liquido": round(resultado_base['troco_liquido'] - iof_adicional,2),
            }

            for banco, contrato, parcela, saldo, operacao_portada in zip(nomes_bancos, num_contratos, parcelas, saldos, operacoes_portadas ):
                dados_contratos.append(
                    {
                        'nome_banco': banco,
                        'num_contrato': contrato,
                        'parcela':parcela,
                        'saldo':saldo,
                        'operacao_portada':operacao_portada

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
        contratos=contratos,
        carencia_padrao = carencia_padrao
    )



if __name__ == '__main__':
    app.run(host ="0.0.0.0", port=5000, debug=True)
