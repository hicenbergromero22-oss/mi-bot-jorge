from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def home():
    edad = request.args.get('edad')
    nombre = request.args.get('nombre')

    if not edad:
        return f"""
        <body style="font-family: sans-serif; background: #111; color: white; text-align: center; padding: 40px;">
            <h1 style="font-size: 50px;">🚧</h1>
            <h1>Hola, soy el Bot de Jorge</h1>
            <p style="color: #aaa; font-size: 20px;">Estoy en desarrollo, aún estoy aprendiendo.</p>
            <p style="color: #aaa;">Por ahora solo sé calcular si eres mayor de edad.</p>
            <br>
            <p>Pruebame aquí:</p>
            <a href="?edad=29" style="background: white; color: black; padding: 15px 25px; border-radius: 30px; text-decoration: none; font-weight: bold;">Probar con 29 años</a>
            <br><br><br>
            <p style="color: #555;">Creado por Jorge - 2026</p>
        </body>
        """

    es_mayor = int(edad) >= 18
    color = "#00c853" if es_mayor else "#ff1744"
    mensaje = "eres MAYOR ✅" if es_mayor else "eres MENOR ❌"
    saludo = f"Hola {nombre}!" if nombre else "Hola!"

    return f"""
    <body style="font-family: sans-serif; background: {color}; color: white; text-align: center; padding: 50px;">
        <h1>{saludo}</h1>
        <h1 style="font-size: 45px;">Tienes {edad} años, {mensaje}</h1>
        <br>
        <a href="/" style="background: white; color: {color}; padding: 15px 30px; text-decoration: none; border-radius: 30px;">Volver</a>
    </body>
    """

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
