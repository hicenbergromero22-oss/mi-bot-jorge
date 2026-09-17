from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def home():
    edad = request.args.get('edad')

    if not edad:
        return """
        <body style="font-family: sans-serif; background: #111; color: white; text-align: center; padding: 40px;">
            <h1 style="font-size: 50px;">🚧</h1>
            <h1>Hola, soy el Bot de Jorge</h1>
            <p style="color: #aaa; font-size: 20px;">Estoy en desarrollo, aún estoy aprendiendo.</p>
            <p style="color: #aaa;">Por ahora solo se calcular si eres mayor de edad.</p>
            <br>
            <a href="?edad=29" style="background: white; color: black; padding: 15px 25px; border-radius: 30px; text-decoration: none; font-weight: bold; margin: 5px; display: inline-block;">Probar 29 años (Mayor)</a>
            <a href="?edad=15" style="background: #555; color: white; padding: 15px 25px; border-radius: 30px; text-decoration: none; font-weight: bold; margin: 5px; display: inline-block;">Probar 15 años (Menor)</a>
            <br><br><br>
            <p style="color: #555;">Creado por Jorge - 2026</p>
        </body>
        """

    # AQUI ES DONDE CAMBIA DE COLOR SOLO
    es_mayor = int(edad) >= 18
    color = "#00c853" if es_mayor else "#ff1744"
    mensaje = "eres MAYOR ✅" if es_mayor else "eres MENOR ❌"

    return f"""
    <body style="font-family: sans-serif; background: {color}; color: white; text-align: center; padding: 50px;">
        <h1 style="font-size: 45px;">Tienes {edad} años, {mensaje}</h1>
        <br>
        <a href="/" style="background: white; color: {color}; padding: 15px 30px; text-decoration: none; border-radius: 30px; font-weight: bold;">Volver</a>
    </body>
    """

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
