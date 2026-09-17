from flask import Flask, request
import random
from datetime import datetime

app = Flask(__name__)

chistes = [
    "¿Por qué el programador cruzó la calle? ¡Para llegar al otro commit!",
    "Mi código no tiene bugs, tiene funciones ocultas.",
    "¿Qué hace una abeja en GitHub? Hace buzz requests."
]

@app.route('/')
def home():
    edad = request.args.get('edad')
    nombre = request.args.get('nombre')

    # Si no hay nada, muestra el menu principal
    if not edad and not nombre:
        return f"""
        <body style="font-family: sans-serif; background: #111; color: white; text-align: center; padding: 30px;">
            <h1 style="font-size: 50px;">🤖</h1>
            <h1>Bot de Jorge V2</h1>
            <p style="color: #aaa;">Estoy en desarrollo</p>
            <br>
            <div style="background: #222; padding: 20px; border-radius: 20px; max-width: 350px; margin: auto;">
                <h3>Pruebame:</h3>
                <a href="?edad=29" style="background: #00c853; color: white; padding: 12px 20px; border-radius: 30px; text-decoration: none; display: block; margin: 10px;">¿Soy mayor con 29 años?</a>
                <a href="?nombre=Jorge" style="background: #2196F3; color: white; padding: 12px 20px; border-radius: 30px; text-decoration: none; display: block; margin: 10px;">Saludame: Jorge</a>
                <a href="?nombre=Jorge&edad=22" style="background: #9C27B0; color: white; padding: 12px 20px; border-radius: 30px; text-decoration: none; display: block; margin: 10px;">Todo junto</a>
            </div>
            <br>
            <p style="color: #555;">Hora del server: {datetime.now().strftime('%H:%M:%S')}</p>
            <p style="color: #555;">Chiste random: {random.choice(chistes)}</p>
            <br>
            <p style="color: #333;">Creado por Jorge - 2026</p>
        </body>
        """

    # Si hay nombre y edad
    saludo = f"Hola {nombre}!" if nombre else "Hola!"
    
    if edad:
        es_mayor = int(edad) >= 18
        color = "#00c853" if es_mayor else "#ff1744"
        mensaje = "eres MAYOR ✅" if es_mayor else "eres MENOR ❌"
        texto_edad = f"Tienes {edad} años, {mensaje}"
    else:
        color = "#2196F3"
        texto_edad = "No me dijiste tu edad"

    return f"""
    <body style="font-family: sans-serif; background: {color}; color: white; text-align: center; padding: 50px;">
        <h1>{saludo}</h1>
        <h1 style="font-size: 35px;">{texto_edad}</h1>
        <br>
        <a href="/" style="background: white; color: {color}; padding: 15px 30px; text-decoration: none; border-radius: 30px; font-weight: bold;">Volver al inicio</a>
    </body>
    """

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
