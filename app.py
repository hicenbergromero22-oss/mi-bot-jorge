from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def bot():
    edad = request.args.get('edad')
    if not edad:
        return "Hola soy el Bot de Jorge 🤖<br><br>Para probarme pon al final del link: ?edad=29<br>Ejemplo: ...com/?edad=29"
    edad = int(edad)
    if edad >= 18:
        return f"Tienes {edad} años, eres MAYOR ✅"
    else:
        return f"Tienes {edad} años, eres MENOR ❌ Te faltan {18-edad} años"

if __name__ == '__main__':
    app.run()
