from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

CSS = """
<style>
body{background:#0a0a0a;color:white;font-family:sans-serif;text-align:center;padding:20px}
.btn{display:block;background:#ff0040;color:white;padding:18px;margin:15px auto;max-width:350px;border-radius:15px;text-decoration:none;font-weight:bold;font-size:18px;border:none;width:90%}
input{padding:15px;width:85%;max-width:330px;border-radius:10px;border:none;margin:10px;font-size:16px}
.card{background:#1a1a1a;padding:20px;border-radius:15px;max-width:400px;margin:20px auto}
</style>
"""

MENU = CSS + """
<h1>Mi Bot Jorge V7 🔥</h1>
<p>Elige que quieres hacer</p>
<a class="btn" href="/chat">💬 Preguntar lo que sea</a>
<a class="btn" href="/descargar">📲 TikToks sin marca</a>
<a class="btn" href="/peliculas">🎬 Películas</a>
<a class="btn" href="/cine" style="background:#222">📺 Mi Cine Hisense</a>
"""

@app.route('/')
def home():
    return MENU

@app.route('/descargar', methods=['GET', 'POST'])
def descargar():
    video_url = None
    if request.method == 'POST':
        link = request.form.get('link')
        try:
            # API gratis de TikWM
            r = requests.post("https://www.tikwm.com/api/", data={"url": link}, timeout=15).json()
            if r.get('code') == 0:
                video_url = r['data'].get('play')
        except:
            video_url = None

    return render_template_string(CSS + f"""
    <h1>📲 TikToks sin marca</h1>
    <div class="card">
    <form method="POST">
        <input name="link" placeholder="Pega aquí el link de TikTok" required>
        <button class="btn" type="submit">Descargar</button>
    </form>
    {"<video src='"+video_url+"' controls autoplay width='100%'></video><br><a class='btn' href='"+video_url+"'>⬇️ Guardar Video</a>" if video_url else ""}
    </div>
    <a class="btn" href="/" style="background:#333">⬅️ Volver</a>
    """)

@app.route('/chat')
def chat():
    return MENU

@app.route('/peliculas')
def pelis():
    return MENU.replace("Elige que quieres hacer", "Buscador de Pelis - ya casi queda")

@app.route('/cine')
def cine():
    return render_template_string(CSS + """
    <h1>Mi Cine Hisense 📺</h1>
    <p>Elige tu mp4 de Statham / Van Damme ya bajado</p>
    <input type=file id="f"><video id="v" controls width="90%"></video><br>
    <button class="btn" onclick="document.getElementById('v').requestFullscreen()">Pantalla Completa</button>
    <a class="btn" href="/" style="background:#333">⬅️ Volver</a>
    <script>
    f.onchange=e=>{v.src=URL.createObjectURL(e.target.files[0]); v.play()}
    </script>
    """)

app.run(host='0.0.0.0', port=10000)
