import os
from flask import Flask, render_template, request, redirect, url_for
from tuya_connector import TuyaOpenAPI
from datetime import datetime
from dotenv import load_dotenv
import logging
import traceback

load_dotenv()

app = Flask(__name__)

# ==================== CONFIGURAÇÕES TUYA ====================
ENDPOINT = "https://openapi.tuyaus.com" 
ACCESS_ID = os.getenv("ACCESS_ID")
ACCESS_KEY = os.getenv("ACCESS_KEY")
DEVICE_ID = os.getenv("DEVICE_ID")

def obter_dados_sensor():
    try:
        print("\n=== INICIANDO CONEXÃO COM TUYA ===")
        print(f"DEVICE_ID: {DEVICE_ID}")

        openapi = TuyaOpenAPI(ENDPOINT, ACCESS_ID, ACCESS_KEY)
        
        # Limpa token antigo
        openapi.token_info = None
        
        connected = openapi.connect()
        print(f"Connect(): {connected}")

        if not connected:
            print("❌ Falha na autenticação")
            return {"nivel": 0, "profundidade": 0.0}

        print("✅ Conectado com sucesso!")

        # Requisição dos dados
        res = openapi.get(f"/v1.0/devices/{DEVICE_ID}/status")
        print(f"RESPOSTA STATUS: {res}")

        dados = {"nivel": 0, "profundidade": 0.0}

        if res.get('success') and isinstance(res.get('result'), list):
            print("\n📊 DADOS DO SENSOR:")
            for item in res['result']:
                code = str(item.get('code', ''))
                value = item.get('value')
                print(f"   DP: {code} = {value}")

                if code in ["liquid_level_percent", "22"]:
                    dados["nivel"] = int(value) if value is not None else 0
                elif code in ["liquid_depth", "2"]:
                    val = float(value)
                    dados["profundidade"] = round(val / 100, 2) if val > 10 else round(val, 2)

        return dados

    except Exception as e:
        print(f"\n❌ ERRO: {e}")
        traceback.print_exc()
        return {"nivel": 0, "profundidade": 0.0}


# ==================== ROTAS FLASK ====================
@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form.get('username') == 'admin' and request.form.get('password') == '123':
            return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    dados = obter_dados_sensor()
    agora = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    
    return render_template('dashboard.html', 
                           nivel=dados["nivel"], 
                           profundidade=dados["profundidade"], 
                           data_hora=agora)

@app.route('/logout')
def logout():
    return redirect(url_for('login'))


if __name__ == '__main__':
    print("🚀 Servidor rodando em http://127.0.0.1:5000")
    app.run(debug=True)