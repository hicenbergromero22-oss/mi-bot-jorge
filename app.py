from flask import Flask, request, jsonify
import random

app = Flask(__name__)

def cerebro_ia(mensaje):
    mensaje = mensaje.lower()
    if "hola" in mensaje or "ola" in mensaje:
        return "¡Hola Crack! Soy Bot Jorge V5 con cerebro nuevo. ¿En qué te ayudo? 😎"
    elif "como estas" in mensaje:
        return "¡Al 100 bro! Ya con el cerebro V5 instalado y listo para lo que sea. ¿Tú qué tal?"
    elif "quien eres" in mensaje:
        return "Soy Bot Jorge V5, tu bot con cerebro. Ya no soy el juego del ligar, ahora sí razono."
    else:
        return f"Va bro, entendí: '{mensaje}'. Dime qué necesitas y te lo armo."

@app.route('/')
def home():
    q = request.args.get('q', '')
    if q:
        respuesta = cerebro_ia(q)
        return jsonify({"pregunta": q, "respuesta": respuesta, "version": "V5 CEREBRO"})
    return """
    <html><head><meta name="viewport" content="width=device-width, initial-scale=1">
    <title>BOT JORGE V5</title>
    <style>
        body{background:#000;color:#0f0;font-family:monospace;text-align:center;padding:20px}
        h1{color:#0f0;text-shadow:0 0 10px #0f0}
        input{padding:15px;width:80%;max-width:400px;background:#111;color:#0f0;border:1px solid #0f0;border-radius:10px;font-size:18px}
        button{padding:15px 25px;background:#0f0;color:#000;border:none;border-radius:10px;font-size:18px;margin-top:10px;font-weight:bold}
        #resp{margin-top:20px;padding:15px;background:#111;border-radius:10px;text-align:left}
    </style></head>
    <body>
        <h1>BOT JORGE V5 CEREBRO 🧠</h1>
        <p>Ya no es el juego V3.1, ahora si tiene cerebro</p>
        <input id="q" placeholder="Escribe algo... ej: hola">
        <br><button onclick="preguntar()">PREGUNTAR</button>
        <div id="resp"></div>
        <script>
        async function preguntar(){
            let q=document.getElementById('q').value;
            let r=await fetch('/?q='+encodeURIComponent(q));
            let data=await r.json();
            document.getElementById('resp').innerHTML='<b>TU:</b> '+data.pregunta+'<br><br><b>JORGE V5:</b> '+data.respuesta;
        }
        </script>
    </body></html>
    """
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
