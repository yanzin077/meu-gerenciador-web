from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Banco de dados temporário em memória para testes
historico_apostas = []
painel_bonus_dados = []

@app.route('/')
@app.route('/dashboard')
def index():
    lucro_total = sum(a.get('lucro', 0) for a in historico_apostas)
    investimento_total = sum(a.get('investimento', 0) for a in historico_apostas)
    roi_acumulado = (lucro_total / investimento_total * 100) if investimento_total > 0 else 0
    
    return render_template(
        'index.html', 
        apostas=historico_apostas,
        lucro_total=lucro_total,
        investimento_total=investimento_total,
        roi_acumulado=roi_acumulado
    )

@app.route('/nova_aposta', methods=['GET', 'POST'])
def nova_aposta():
    if request.method == 'POST':
        evento = request.form.get('evento')
        estrategia = request.form.get('estrategia', 'Arbitragem')
        observacao = request.form.get('observacao', '')
        
        # Recebe as listas de dados enviadas pelo formulário
        casas = request.form.getlist('casa')
        odds = request.form.getlist('odd')
        valores = request.form.getlist('valor')
        
        investimento = sum(float(v) for v in valores if v)
        
        # Salva o registro
        historico_apostas.append({
            'evento': evento,
            'estrategia': estrategia,
            'observacao': observacao,
            'casas': casas,
            'investimento': investimento,
            'lucro': 0.0, # Pode ser atualizado ao finalizar a aposta
            'status': 'Pendente'
        })
        return redirect(url_for('index'))

    return render_template('nova_aposta.html')

@app.route('/painel_bonus', methods=['GET', 'POST'])
def painel_bonus():
    if request.method == 'POST':
        casa = request.form.get('casa')
        valor_bonus = float(request.form.get('valor_bonus', 0))
        rollover = request.form.get('rollover', '')
        
        painel_bonus_dados.append({
            'casa': casa,
            'valor_bonus': valor_bonus,
            'rollover': rollover,
            'status': 'Em Andamento'
        })
        return redirect(url_for('painel_bonus'))

    return render_template('painel_bonus.html', bonus_list=painel_bonus_dados)

if __name__ == '__main__':
    # Define o host para liberar todas as conexões e usa a porta 80 (padrão HTTP)
    app.run(host='0.0.0.0', port=80, debug=True)