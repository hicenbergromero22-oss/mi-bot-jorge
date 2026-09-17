from flask import Flask, request, jsonify
from datetime import datetime
import random
app = Flask(__name__)

def cerebro_ia(m):
    ml = m.lower()
    ahora = datetime.now()
    if "noviembre" in ml and "1" in ml or "dia de muertos" in ml or "día de muertos" in ml or "1 y 2" in ml:
        return "El 1 y 2 de noviembre se festeja el DIA DE MUERTOS en Mexico. 1 Nov: Muertos chiquitos (niños). 2 Nov: Muertos adultos. Se pone altar, cempasuchil, pan de muerto y se visita el panteon."
    if "que dia" in ml or "qué día" in ml or "fecha" in ml:
        return f"Hoy es {ahora.strftime('%A %d/%m/%Y')} - {ahora.strftime('%H:%M')}"
    if "hora" in ml: return f"Son las {ahora.strftime('%H:%M:%S')}"
    if "hola" in ml: return "Hola crack! Ya soy V5.3 REAL. Ahora si respondo bien."
    return f"Preguntaste: '{m}'. Ya soy V5.3 y si entiendo. Preguntame: Que dia es? Que se festeja el 1 y 2 de noviembre? Que hora es? Un chiste?"

@app.route('/')
def home():
    q = request.args.get('q','')
    if q: return jsonify(pregunta=q, respuesta=cerebro_ia(q), v="V5.3")
    return """<html><head><meta name="viewport" content="width=device-width, initial-scale=1"><style>body{background:#000;color:#0f0;font-family:monospace;text-align:center;padding:20px}h1{color:#0f0}input{padding:15px;width:85%;background:#111;color:#0f0;border:1px solid #0f0;border-radius:10px;font-size:18px}button{padding:15px 25px;background:#0f0;color:#000;border:none;border-radius:10px;margin-top:10px;font-weight:bold}#resp{margin-top:20px;padding:15px;background:#111;border-radius:10px;text-align:left;white-space:pre-wrap}</style></head><body><h1>BOT JORGE V5.3 REAL</h1><input id="q" placeholder="Que se festeja el 1 y 2 de noviembre?"><br><button onclick="preguntar()">PREGUNTAR</button><div id="resp"></div><script>async function preguntar(){let q=document.getElementById('q').value;let r=await fetch('/?q='+encodeURIComponent(q)+'&t='+Date.now());let d=await r.json();document.getElementById('resp').innerHTML='<b>TU:</b> '+d.pregunta+'<br><br><b>JORGE V5.3:</b> '+d.respuesta;}</script></body></html>"""
if __name__ == '__main__': app.run(host='0.0.0.0', port=10000)
