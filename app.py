from flask import Flask, request, render_template_string, send_file
import os, base64, yt_dlp
from PIL import Image
import io

app = Flask(__name__)

CSS = """
<style>
body{background:#0f0f0f;color:white;font-family:Arial;padding:20px;text-align:center}
.card{background:#1e1e1e;padding:20px;border-radius:15px;margin:15px auto;max-width:500px}
.btn{display:inline-block;padding:12px 20px;border-radius:10px;text-decoration:none;color:white;margin:5px;font-weight:bold;border:none}
input{width:90%;padding:12px;border-radius:10px;border:none;margin:10px 0}
textarea{width:90%;height:280px;background:#000;color:#0f0;padding:10px;border-radius:10px}
</style>
"""

@app.route('/')
def home():
    return render_template_string(CSS + """
    <h1>🤖 Bot de Jorge - LIVE</h1>
    <div class="card">
        <a class="btn" style="background:#e84393" href="/tiktok">⬇️ TikTok</a>
        <a class="btn" style="background:#00b894" href="/cnc">⚙️ CNC con Foto</a>
    </div>
    """)

@app.route('/tiktok', methods=['GET','POST'])
def tiktok():
    msg = ""
    if request.method == 'POST':
        url = request.form.get('url','').strip()
        if url:
            try:
                out = "/tmp/video.mp4"
                ydl_opts = {'outtmpl': out, 'format': 'mp', 'quiet': True, 'noplaylist': True}
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
                return send_file(out, as_attachment=True, download_name="tiktok.mp4")
            except Exception as e:
                msg = f"Error: {str(e)[:200]}"
    return render_template_string(CSS + """
    <h1>⬇️ TikTok</h1>
    <div class="card">
        <form method="POST"><input name="url" placeholder="Pega link TikTok" required>
        <button class="btn" style="background:#e84393" type="submit">Descargar</button></form>
        <p style="color:#ff7675">{{msg}}</p>
    </div>
    <a class="btn" href="/" style="background:#333">Volver</a>
    """, msg=msg)

@app.route('/cnc', methods=['GET','POST'])
def cnc():
    gcode = ""
    img_b64 = ""
    if request.method == 'POST':
        desc = request.form.get('descripcion','PLACA 100x60')
        f = request.files.get('plano')
        if f and f.filename:
            img = Image.open(f.stream)
            # convertimos a base64 para mostrarla sin guardarla en Render
            buffered = io.BytesIO()
            img.save(buffered, format="JPEG")
            img_b64 = base64.b64encode(buffered.getvalue()).decode()

        gcode = f"""%
O1001 ({desc})
G21 G40 G49 G80 G90
G17 G54
T01 M06 (FRESA 6MM)
G00 X0 Y0 Z50.
M03 S1500 M08
G00 Z5. F300
G01 Z-2. F150
G01 X100. Y0
Y60.
X0
Y0
G00 Z50.
M05 M09
M30
%
( PLANO: {desc} )
"""

    return render_template_string(CSS + """
    <h1>⚙️ CNC + Foto</h1>
    <div class="card">
        <form method="POST" enctype="multipart/form-data">
            <input name="descripcion" placeholder="Ej: Placa 100x60 4 barrenos 8mm" required>
            <input type="file" name="plano" accept="image/*">
            <button class="btn" style="background:#00b894" type="submit">Generar</button>
        </form>
        {% if img_b64 %}<img src="data:image/jpeg;base64,{{img_b64}}" style="width:100%;border-radius:10px;margin-top:15px">{% endif %}
        {% if gcode %}<textarea id="c">{{gcode}}</textarea><br>
        <button class="btn" style="background:#00b894" onclick="navigator.clipboard.writeText(document.getElementById('c').value)">📋 Copiar G-CODE</button>{% endif %}
    </div>
    <a class="btn" href="/" style="background:#333">Volver</a>
    """, gcode=gcode, img_b64=img_b64)

if __name__ == '__main__':
    app.run()
