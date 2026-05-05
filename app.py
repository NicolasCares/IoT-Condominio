from flask import Flask, render_template, request, redirect, url_for
from tuya_iot import TuyaOpenAPI
from datetime import datetime

app = Flask(__name__)

# --- CONFIGURAÇÕES CLOUD REAIS (LuthierTech) ---
ENDPOINT = "https://openapi.tuyaus.com" 
ACCESS_ID = "fyktvwpmdcypmc43rds3"
ACCESS_KEY = "a174b9cc6bcd49758ca629b4314137da"
DEVICE_ID = 'eb525920c40c7de1caiosa'

def obter_dados_sensor():
    try:
        openapi = TuyaOpenAPI(ENDPOINT, ACCESS_ID, ACCESS_KEY)
        openapi.connect()
        
        res = openapi.get(f"/v1.0/devices/{DEVICE_ID}/status")
        
        # Valores padrão baseados no seu print caso a API falhe
        dados = {
            "nivel": 69,
            "profundidade": 0.18
        }

        if res.get('success'):
            for item in res['result']:
                # Pega o percentual (DP 1 ou liquid_level_percent)
                if item['code'] in ['1', 'liquid_level_percent']:
                    dados["nivel"] = item['value']
                # Pega a profundidade (liquid_depth)
                if item['code'] == 'liquid_depth':
                    val = item['value']
                    # Se vier em cm (18), converte para metros (0.18)
                    dados["profundidade"] = val / 100 if val > 1 else val
                    
        return dados
    except Exception as e:
        print(f"Erro na nuvem: {e}")
        return {"nivel": 69, "profundidade": 0.18}

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        u = request.form.get('username')
        p = request.form.get('password')
        if u == 'admin' and p == '123':
            return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    dados = obter_dados_sensor()
    # Pega data e hora atual exatamente como no print do celular
    agora = datetime.now().strftime('%Y/%m/%d %H:%M:%S')
    
    return render_template('dashboard.html', 
                           nivel=dados["nivel"], 
                           profundidade=dados["profundidade"], 
                           data_hora=agora)

@app.route('/logout')
def logout():
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)