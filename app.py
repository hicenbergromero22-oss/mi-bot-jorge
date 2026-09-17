from flask import Flask, request
import random

app = Flask(__name__)

frases = [
    "Dile: 'Jaja, aburrido yo? Espérate a conocerme bien 😏'",
    "Dile: 'Aburrido? Yo soy el premio mayor'",
    "Dile: '¿Aburrida? Te entretengo yo, ¿qué quieres hacer?'"
]

# Guardamos el número en una variable global simple para que no falle
NUMERO_SECRETO = random.randint(1, 100)

@app.route('/')
def home():
    global NUMERO_SECRETO
    nombre = request.args.get('nombre', 'Crack')
    intento = request.args.get('juego')
    ligar = request.args.get('ligar')

    msg_juego = "Tengo un número del 1 al 100, ¡adivínalo!"
    if intento:
        try:
            n = int(intento)
            if n == NUMERO_SECRETO:
                msg_juego = f"¡LE DISTE! Era el {NUMERO_SECRETO} 🎉 Ya puse otro."
                NUMERO_SECRETO = random.randint(1, 100)
            elif n < NUMERO_SECRETO:
                msg_juego = f"{n} es muy BAJO, subele 👆"
            else:
                msg_juego = f"{n} es muy ALTO, bajale 👇"
        except:
            msg_juego = "Pon un número válido"

    msg_ligue = ""
    if ligar:
        msg_ligue = random.choice(frases)

    return f"""
    <html><body style="background:#111;color:white;font-family:sans-serif;text-align:center;padding:20px;">
    <h1>🤖 Bot Jorge V3.1 FIX</h1>
    <p>Hola {nombre}</p>
    <div style="background:#222;padding:20px;border-radius:20px;max-width:400px;margin:20px auto;">
        <h3>🎮 Adivina (1-100)</h3>
        <p style="color:#00ff88;font-weight:bold;">{msg_juego}</p>
        <a href="/?juego=25&nombre={nombre}" style="background:#333;padding:10px;border-radius:10px;color:white;text-decoration:none;margin:5px;display:inline-block;">25</a>
        <a href="/?juego=50&nombre={nombre}" style="background:#333;padding:10px;border-radius:10px;color:white;text-decoration:none;margin:5px;display:inline-block;">50</a>
        <a href="/?juego=75&nombre={nombre}" style="background:#333;padding:10px;border-radius:10px;color:white;text-decoration:none;margin:5px;display:inline-block;">75</a>
        <br><br>
        <form><input type="hidden" name="nombre" value="{nombre}"><input name="juego" type="number" placeholder="Tu número" style="padding:10px;border-radius:10px;border:none;"><button style="padding:10px;background:#00c853;color:white;border:none;border-radius:10px;margin-left:5px;">Probar</button></form>
    </div>
    <div style="background:#222;padding:20px;border-radius:20px;max-width:400px;margin:20px auto;">
        <h3>🔥 Ligar</h3>
        <p style="color:#ff4081;">{msg_ligue}</p>
        <a href="/?ligar=1&nombre={nombre}" style="background:#ff4081;padding:12px 20px;border-radius:30px;color:white;text-decoration:none;">Dame frase</a>
    </div>
    <p style="color:#555;font-size:12px;">Si ves esto, el V3.1 ya jaló</p>
    </body></html>
    """
