from flask import Flask, request, render_template_string, send_file
import os
import yt_dlp

app = Flask(__name__)

CSS = """
<style>
body{background:#0f0f0f;color:white;font-family:Arial;padding:20px;text-align:center}
.card{background:#1e1e1e;padding:20px;border-radius:15px;margin:15px auto;max-width:500px}
.btn{display:inline-block;padding:12px 20px;border-radius:10px;text-decoration:none;color:white;margin:5px;font-weight:bold}
input{width:90%;padding:12px;border-radius:10px;border:none;margin:10px 0}
</style>
"""

@app.route('/')
def home():
    return render_template_string(CSS + """
    <h1>🤖 Bot de Jorge</h1>
    <div class="card">
        <a class="btn" style="background:#e84393" href="/tiktok">⬇️ TikTok</a>
        <a class="btn" style="background:#00b894" href="/cnc">⚙️ CNC con Foto</a>
    </div>
    """)

@app.route('/tiktok', methods=['GET','POST'])
def tiktok():
    if request.method == 'POST':
        url = request.form.get('url')
        if url:
            ydl_opts = {'outtmpl': '/tmp/%(title)s.%(ext)s', 'quiet': True}
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)
                return send_file(filename, as_attachment=True)
    return render_template_string(CSS + """
    <h1>⬇️ TikTok Downloader</h1>
    <div class="card">
        <form method="POST"><input name="url" placeholder="Pega link TikTok" required>
        <button class="btn" style="background:#e84393" type="submit">Descargar</button></form>
    </div>
    <a class="btn" href="/" style="background:#333">Volver</a>
    """)

@app.route('/cnc', methods=['GET','POST'])
def cnc():
    gcode = ""
    texto = ""
    if request.method == 'POST':
        desc = request.form.get('descripcion','PLACA 100x60')
        archivo = request.files.get('plano')
        if archivo and archivo.filename != "":
            try:
                from PIL import Image
                import pytesseract
                ruta = "/tmp/" + archivo.filename
                archivo.save(ruta)
                texto = pytesseract.image_to_string(Image.open(ruta))
            except Exception as e:
                texto = "Foto recibida. " + str(e)

        gcode = f"""%
O1001 ({desc})
G21 G40 G49 G80 G90
G17 G54
T01 M06 (FRESA 6MM)
G00 X0 Y0 Z50.
M03 S1500 M08
G00 Z5. F300
G01 Z-2. F150
X100. Y0
Y60.
X0
Y0
G00 Z50.
M30
%
"""
        if texto:
            gcode = gcode + "\\n( TEXTO PLANO: " + texto[:100] + " )"

    return render_template_string(CSS + """
    <h1>⚙️ CNC con Foto</h1>
    <div class="card">
        <form method="POST" enctype="multipart/form-data">
            <input name="descripcion" placeholder="Ej: Placa 100x60 4 barrenos" required>
            <input type="file" name="plano" accept="image/*">
            <button class="btn" style="background:#00b894" type="submit">Generar G-CODE</button>
        </form>
        {% if texto %} <p style="background:#222;padding:10px">Leí del plano: {{texto}}</p> {% endif %}
        {% if gcode %} <textarea style="width:90%;height:250px;background:#000;color:#0f0;padding:10px">{{gcode}}</textarea> {% endif %}
    </div>
    <a class="btn" href="/" style="background:#333">Volver</a>
    """, gcode=gcode, texto=texto)

if __name__ == '__main__':
    app.run()
