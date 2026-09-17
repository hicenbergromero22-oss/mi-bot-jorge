from flask import Flask, request
import requests, random

app = Flask(__name__)

# CEREBRO GRATIS SIN API KEY (Usa una IA libre)
def cerebro_ia(texto_del_usuario):
    try:
        # Usamos una IA gratis
        url = "https://api.affiliateplus.xyz/api/chatbot"
        params = {
            "message": texto_del_usuario,
            "botname": "Jorge Bot",
            "ownername": "Jorge",
            "user": "1"
        }
        r = requests.get(url, params=params, timeout=10).json()
        return r.get("message", "No entendí, repite")
    except:
        # Si falla la IA, entra el respaldo
        return random.choice([
            f"Para '{texto_del_usuario}' dile: 'jajaja alv neta? no te creo'",
            "Dile: 'Uy, me dejaste pensando... tú siempre tan misteriosa'",
            "Contesta: 'Jaja te pasas, ¿y luego qué le dijiste?'"
        ])

@app.route('/')
def home():
    q = request.args.get('q')
    nombre = request.args.get('nombre', 'Crack')

    if not q:
        return f"""
        <body style="background:#0a0a0a;color:white;font-family:sans-serif;text-align:center;padding:30px;">
            <h1>🧠 BOT JORGE V5 - CON CEREBRO</h1>
            <p>Hola {nombre}, ya respondo a LO QUE SEA</p>
            <div style="background:#1a1a1a;padding:20px;border-radius:20px;max-width:500px;margin:auto;">
               
