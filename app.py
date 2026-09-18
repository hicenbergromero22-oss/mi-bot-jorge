from flask import Flask, request, render_template_string

app = Flask(__name__)

MENU = """
<style>
body{background:#0a0a0a;color:white;font-family:sans-serif;text-align:center;padding:20px}
.btn{display:block;background:#ff0040;color:white;padding:18px;margin:15px auto;max-width:350px;border-radius:15px;text-decoration:none;font-weight:bold;font-size:18px}
h1{margin-top:30px}
</style>
<h1>Mi Bot Jorge V7 🔥</h1>
<p>Elige que quieres hacer</p>
<a class="btn" href="/chat">💬 Preguntar lo que sea</a>
<a class="btn" href="/descargar">📲 TikToks sin marca</a>
<a class="btn" href="/pelis">🎬 Películas</a>
<a class="btn" href="/cine" style="background:#222">📺 Mi Cine Hisense</a>
"""

@app.route('/')
def home():
    return MENU

@app.route('/chat')
def chat():
    return MENU.replace("Mi Bot Jorge V7", "Preguntar lo que sea - Próximamente")

@app.route('/descargar')
def descargar():
    return render_template_string(MENU + "<p>Pega el link de TikTok aquí</p>")

@app.route('/pelis')
def pelis():
    return render_template_string(MENU + "<p>Buscador de pelis aquí</p>")

@app.route('/cine')
def cine():
    # Aquí va tu código original de Hisense que me mandaste en la foto
    return render_template_string(open('templates/cine.html').read() if False else """
    <body style="background:#111;color:white;text-align:center;font-family:sans-serif">
    <h1>Mi Cine Hisense 📺</h1>
    <h3>Elige tu mp4 de Statham / Van Damme ya bajado</h3>
    <input type=file><br><br>
    <video controls width="90%"></video><br><br>
    <a class="btn" href="/">⬅️ Volver al menú</a>
    </body>
    """)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
