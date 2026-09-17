from flask import Flask, request, jsonify
from datetime import datetime
import random

app = Flask(__name__)

def cerebro_ia(mensaje):
    msg = mensaje.lower()
    ahora = datetime.now()
    dias = ["Lunes","Martes","Miércoles","Jueves","Viernes","Sábado","Domingo"]
    dia_nombre = dias[ahora.weekday()]

    if "hola" in msg or "ola" in msg:
        return "¡Hola Crack! Soy Jorge V5.1 ya con cerebro real. ¿Qué necesitas?"
    elif "que dia" in msg or "qué día" in msg or "fecha" in msg:
        return f"Hoy es {dia_nombre} {ahora.day} de {ahora.month} del {ahora.year} bro 📅"
    elif "hora" in msg or "que hora" in msg:
        return f"Son las {ahora.strftime('%H:%M')} en este momento 🕒"
    elif "como estas" in msg:
        return "Al 100 bro, con el V5.1 ya soy otro. ¿Tú cómo vas?"
    elif "quien eres" in msg:
        return "Soy Bot Jorge V5.1 CEREBRO REAL, ya no soy el juego viejo, ahora sí pienso."
    elif "chiste" in msg:
        return random.choice([
            "¿Por qué el programador fue al psicólogo? ¡Porque tenía muchos bugs mentales! 😂",
            "Va uno: -¿Sabes que mi bot ya tiene cerebro? -No, ¿desde cuándo? -Desde que tú tienes novia 🤣",
            "¿Qué le dice un bit a otro? Nos vemos en el bus 🚌"
        ])
    elif "ayuda" in msg:
        return "Dime lo que sea: qué día es, qué hora, un chiste, consejo para ligar, tarea, lo que quieras y te lo armo."
    elif msg.strip() == "":
        return "Escribe algo bro, estoy listo."
    else:
        return f"Va, sobre '{mensaje}' -> Te ayudo. Dime exactamente qué quieres que te haga con eso y te lo armo en corto."

@app.route('/')
def home():
    q = request.args.get('q','')
    if q:
        return jsonify({"pregunta":q,"respuesta":cerebro_ia(q),"version":"V5.1 REAL"})
    return """
    <html><head><meta name="viewport" content="width=device-width, initial-scale=1"><title>BOT JORGE V5.1</title>
    <style>
        body{background:#000;color:#0f0;font-family:monospace;text-align:center;padding:20px}
        h1{color:#0f0;text-shadow:0 0 10px #0f0}
        input{padding:15px;width:80%;max-width:400px;background:#111;color:#0f0;border:1px solid #0f0;border-radius:10px;font-size:18px}
        button{padding:15px 25px;background:#0f0;color:#000;border:none;border-radius:10px;font-size:18px;margin-top:10px;font-weight:bold}
        #resp{margin-top:20px;padding:15px;background:#111;border-radius:10px;text-align:left;white-space:pre-wrap}
    </style></head>
    <body>
        <h1>BOT JORGE V5.1 CEREBRO REAL 🧠</h1>
        <p>Ahora si responde de verdad</p>
        <input id="q" placeholder="Ej: Que dia es?">
        <br><button onclick="preguntar()">PREGUNTAR</button>
        <div id="resp"></div>
        <script>
        async function preguntar(){
            let q=document.getElementById('q').value;
            let r=await fetch('/?q='+encodeURIComponent(q));
            let data=await r.json();
            document.getElementById('resp').innerHTML='<b>TU:</b> '+data.pregunta+'<br><br><b>JORGE V5.1:</b> '+data.respuesta;
        }
        </script>
    </body></html>
    """
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
