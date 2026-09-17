from flask import Flask, request, jsonify
import os
import requests
app = Flask(__name__)

def cerebro_real(mensaje):
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        return "Bro, me falta la llave. Pon la GROQ_API_KEY en Render > Environment. Sin eso solo soy V5 basico."
    try:
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
        data = {"model": "llama-3.1-8b-instant","messages": [{"role": "system", "content": "Eres Bot Jorge V6, mexicano, barrio, buena onda. Responde corto, claro, como compa. Explica bien fechas mexicanas como 1 y 2 de noviembre Dia de Muertos."},{"role": "user", "content": mensaje}],"temperature": 0.7}
        r = requests.post(url, headers=headers, json=data, timeout=20)
        res = r.json()
        return res['choices'][0]['message']['content']
    except Exception as e:
        return f"Error cerebro real: {e}"

@app.route('/')
def home():
    q = request.args.get('q','')
    if q: return jsonify(pregunta=q, respuesta=cerebro_real(q), version="V6 PRO")
    return """<html><head><meta name="viewport" content="width=device-width, initial-scale=1"><title>BOT JORGE V6 PRO</title><style>body{background:#000;color:#0f0;font-family:monospace;text-align:center;padding:20px}h1{color:#0f0;text-shadow:0 0 15px #0f0}input{padding:15px;width:85%;max-width:500px;background:#111;color:#0f0;border:1px solid #0f0;border-radius:10px;font-size:18px}button{padding:15px 25px;background:#0f0;color:#000;border:none;border-radius:12px;font-size:18px;margin-top:12px;font-weight:bold}#resp{margin-top:20px;padding:18px;background:#111;border-radius:12px;text-align:left;white-space:pre-wrap}</style></head><body><h1>BOT JORGE V6 PRO 🧠🔥</h1><p>Ahora si entiendo TODO</p><input id="q" placeholder="Preguntame lo que sea..."><br><button onclick="preguntar()">PREGUNTAR</button><div id="resp">Escribe algo...</div><script>async function preguntar(){let q=document.getElementById('q').value;if(!q)return;document.getElementById('resp').innerHTML='Pensando...';let r=await fetch('/?q='+encodeURIComponent(q)+'&t='+Date.now());let d=await r.json();document.getElementById('resp').innerHTML='<b>TU:</b> '+d.pregunta+'<br><br><b>JORGE V6:</b> '+d.respuesta;}</script></body></html>"""
if __name__ == '__main__': app.run(host='0.0.0.0', port=10000)
