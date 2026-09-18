from flask import Flask, request, render_template_string, send_file
import yt_dlp
import os

app = Flask(__name__)

CSS = """
<style>
body{background:#0f0f0f;color:white;font-family:Arial;text-align:center;padding:20px}
.card{background:#1e1e1e;padding:20px;border-radius:15px;max-width:500px;margin:20px auto}
.btn{display:block;background:#ff0050;color:white;padding:15px;margin:10px auto;border-radius:10px;text-decoration:none;width:85%;border:none;font-size:17px;font-weight:bold}
input{padding:12px;border-radius:10px;border:none;width:85%;margin:10px}
textarea{width:85%}
</style>
"""

@app.route('/')
def menu():
    return render_template_string(CSS + """
    <h1>GE - Menu Jorge</h1>
    <div class="card">
        <a class="btn" href="/descargar">🎵 TikTok Sin Marca</a>
        <a class="btn" href="/cnc" style="background:#00b894">⚙️ Generador CNC FANUC mm</a>
        <a class="btn" href="/whatsapp" style="background:#25D366">💬 WhatsApp Link</a>
    </div>
    """)

# --- 1. TIKTOK - NO SE TOCA ---
@app.route('/descargar', methods=['GET', 'POST'])
def descargar():
    mensaje = ""
    if request.method == 'POST':
        url = request.form.get('url')
        try:
            ydl_opts = {'outtmpl': '/tmp/%(id)s.mp4', 'quiet': True}
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                archivo = ydl.prepare_filename(info)
            return send_file(archivo, as_attachment=True)
        except Exception as e:
            mensaje = f"Error: {e}"
    return render_template_string(CSS + f"""
    <h1>🎵 TikTok Downloader</h1>
    <div class="card">
        <form method="POST">
            <input name="url" placeholder="Pega link de TikTok aquí" required>
            <button class="btn" type="submit">Descargar</button>
        </form>
        <p style="color:#ff5555">{mensaje}</p>
    </div>
    <a class="btn" href="/" style="background:#333">⬅️ Volver</a>
    """)

--- 2. CNC FANUC MM ---
@app.route('/cnc', methods=['GET', 'POST'])
def cnc():
    gcode = ""
    if request.method == 'POST':
        desc = request.form.get('descripcion','PIEZA')
        gcode = f"""%
O1001 ({desc.upper()} - FANUC MM)
G21 G40 G49 G80 G90
G17 G54
T01 M06 (FRESA 10MM)
G00 X0 Y0
G43 H01 Z50.
M03 S1500 M08
G00 Z5.0
G01 Z-5.0 F100
( CONTORNO 100x50 EJEMPLO )
G01 X100.0 F250
Y50.0
X0
Y0
G00 Z50.0
M09
M05
G91 G28 Z0
G28 X0 Y0
M30
%
"""
    return render_template_string(CSS + f"""
    <h1>⚙️ CNC FANUC mm</h1>
    <div class="card">
        <form method="POST">
            <input name="descripcion" placeholder="Ej: Placa 120x60 4 barrenos 8mm" required>
            <button class="btn" style="background:#00b894" type="submit">Generar G-CODE</button>
        </form>
        {"<textarea id='code' style='height:320px;background:#000;color:#0f0;padding:15px;border-radius:10px;margin-top:20px;font-family:monospace'>"+gcode+"</textarea><br><button class='btn' style='background:#00b894' onclick='navigator.clipboard.writeText(document.getElementById(`code`).value);alert(`Copiado!`)'>📋 Copiar Programa</button>" if gcode else "<p style='color:#888'>Describe la pieza y te genero el programa</p>"}
    </div>
    <a class="btn" href="/" style="background:#333">⬅️ Volver</a>
    """)
# --- 3. WHATSAPP ---
@app.route('/whatsapp', methods=['GET', 'POST'])
def whatsapp():
    link = ""
    if request.method == 'POST':
        num = request.form.get('numero','').replace('+','').replace(' ','')
        msg = request.form.get('mensaje','')
        link = f"https://wa.me/{num}?text={msg.replace(' ', '%20')}"
    return render_template_string(CSS + f"""
    <h1>💬 Generador WhatsApp</h1>
    <div class="card">
        <form method="POST">
            <input name="numero" placeholder="Número ej: 52811xxxxxxx" required>
            <input name="mensaje" placeholder="Mensaje">
            <button class="btn" style="background:#25D366" type="submit">Generar Link</button>
        </form>
        {"<a class='btn' style='background:#25D366' href='"+link+"' target='_blank'>Abrir WhatsApp: "+link+"</a>" if link else ""}
    </div>
    <a class="btn" href="/" style="background:#333">⬅️ Volver</a>
    """)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
