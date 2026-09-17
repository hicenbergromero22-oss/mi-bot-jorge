from flask import Flask, request, session
import random

app = Flask(__name__)
app.secret_key = 'jorge123' # Clave para que recuerde el juego

frases_ligue = [
    "Dile: 'Jaja, aburrido yo? Espérate a conocerme bien y me ruegas que me vaya 😏'",
    "Dile: 'Uy perdón, estaba pensando en que decirte para impresionarte y se me fue el tiempo'",
    "Dile: 'Aburrido? Yo soy el premio mayor, tú te lo pierdes'",
    "Respuesta pro: 'Jajaja te pasas, ¿qué andas haciendo que andas tan aburrida?' (Le cambias el tema)",
    "Respuesta tierna: 'No soy aburrido, solo me pongo nervioso contigo'"
]

@app.route('/')
def home():
    nombre = request.args.get('nombre', 'Crack')
    edad = request.args.get('edad')
    numero = request.args.get('juego')
    ligar = request.args.get('ligar')

    # --- LÓGICA DEL JUEGO ---
    if 'numero_secreto' not in session:
        session['numero_secreto'] = random.randint(1, 100)
    
    mensaje_juego = ""
    if numero:
        try:
            num = int(numero)
            secreto = session['numero_secreto']
            if num == secreto:
                mensaje_juego = f"¡LE ATINASTE! Era el {secreto} 🎉🎉 Jugamos de nuevo, ya puse otro número."
                session['numero_secreto'] = random.randint(1, 100)
            elif num < secreto:
                mensaje_juego = f"El {num} es muy BAJO, súbele más 👆"
            else:
                mensaje_juego = f"El {num} es muy ALTO, bájale 👇"
        except:
            mensaje_juego = "Pon un número del 1 al 100"

    # --- LÓGICA DEL LIGUE ---
    mensaje_ligue = ""
    if ligar is not None:
        mensaje_ligue = random.choice(frases_ligue)

    # --- HTML ---
    return f"""
    <body style="font-family: sans-serif; background: #0f0f0f; color: white; text-align: center; padding: 20px;">
        <h1>🤖 Bot de Jorge V3.0</h1>
        <p style="color: #aaa;">Hola {nombre}!</p>

        <div style="background: #1e1e1e; padding: 20px; border-radius: 20px; max-width: 400px; margin: 20px auto; border: 1px solid #333;">
            <h2>🎮 Adivina el número (1-100)</h2>
            <p style="color: #00ff88; font-weight: bold;
