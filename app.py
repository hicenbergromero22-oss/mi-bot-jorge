from flask import Flask, request
import requests
import random

app = Flask(__name__)

def cerebro_ia(texto):
    try:
        # Cerebro gratis
        r = requests.get(f"https://api.affiliateplus.xyz/api/chatbot?message={texto}&botname=Jorge&ownername=Jorge&user=1", timeout=8).json()
        resp = r.get("message", "")
        if resp:
            return resp
    except:
        pass
    # Respaldo por si falla internet
    return random.choice([
        f"Para eso de '{texto}' dile algo curioso y chido",
        "Jajaja dile: 'Uy, me dejaste pensando en eso'",
        "Contéstale: 'Neta? Cuenta más'"
    ])

@app.route('/')
def home():
    q = request.args.get('q', '')
    nombre = request.args.get('nombre', 'Crack')

    if not q:
        return f"""
        <html><body style="background:#0a0a0a;color:white;font-family:sans-serif;text-align:center;padding:25px;">
        <h1>🧠 BOT JORGE V5 CEREBRO</h1>
        <p>Hola {nombre}, ahora respondo a LO QUE SEA</p>
        <div style="background:#1a1a1a;padding:20px;border-radius:20px;max-width:500px;margin:20px auto;">
            <form method="get">
                <input name="q" placeholder="Escribe lo que te dijo ella..." style="width:90%;padding:15px;border-radius:30px;border:none;font-size:16px;">
                <br><br>
                <button style="padding:15px 40px;border-radius:30px;border:none;background:#00ff88;font-weight:bold;font-size:16px;">PREGUNTAR 🧠</button>
            </form>
        </div>
        <p style="color:#555;">Prueba: /?q=hola | /?q=como le hago para ligar</p>
        </body></html>
        """
    
    respuesta = cerebro_ia(q)
    return f"""
    <html><body style="background:#0a0a0a;color:white;font-family:sans-serif;text-align:center;padding:25px;">
    <p style="color:#888;">Te dijo:</p>
    <h2>{q}</h2>
    <div style="background:#00ff88;color:black;padding:20px;border-radius:20px;max-width:500px;margin:20px auto;font-size:19px;font-weight:bold;">
        {respuesta}
    </div>
    <a href="/" style="background:#222;color:white;padding:12px 25px;border-radius:30px;text-decoration:none;">Preguntar otra cosa</a>
    </body></html>
    """

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
