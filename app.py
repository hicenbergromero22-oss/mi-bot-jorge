from flask import Flask, request, render_template_string, send_file
import os, requests, base64, io
from PIL import Image

app = Flask(__name__)

CSS = """
<style>
body{background:#0f0f0f;color:white;font-family:Arial;padding:20px;text-align:center}
.card{background:#1e1e1e;padding:20px;border-radius:15px;margin:15px auto;max-width:500px}
.btn{display:inline-block;padding:12px 20px;border-radius:10px;text-decoration:none;color:white;margin:5px;font-weight:bold;border:none}
input{width:90%;padding:12px;border-radius:10px;border:none;margin:10px 0}
</style>
"""

@app.route('/')
def home():
    return render_template_string(CSS + "<h1>🤖 Bot de Jorge - V4</h1><div class='card'><a class='btn' style='background:#e84393' href='/tiktok'>⬇️ TikTok</a><a class='btn' style='background:#00b894' href='/cnc'>⚙️ CNC</a></div>")

@app.route('/tiktok', methods=['GET','POST'])
def tiktok():
    msg = ""
    if request.method == 'POST':
        url = request.form.get('url','').strip()
        if url:
            try:
                api_url = "https://www.tikwm.com/api/"
                data = {"url": url, "count": 12, "cursor": 0, "web": 1, "hd": 1}
                headers = {"User-Agent": "Mozilla/5.0", "Content-Type": "application/x-www-form-urlencoded"}
                r = requests.post(api_url, data=data, headers=headers, timeout=20).json()
                
                play = r.get('data',{}).get('play') or r.get('data',{}).get('hdplay')
                if play:
                    # FIX para el error de tu foto
                    if play.startswith('/'):
                        play = 'https://www.tikwm.com' + play
                    
                    v = requests.get(play, headers={"User-Agent":"Mozilla/5.0"}, stream=True, timeout=30)
                    out = "/tmp/tiktok.mp4"
                    with open(out, 'wb') as f:
                        for chunk in v.iter_content(1024*1024):
                            f.write(chunk)
                    return send_file(out, as_attachment=True, download_name="tiktok.mp4")
                else:
                    msg = f"No se pudo obtener video. {str(r)[:300]}"
            except Exception as e:
                msg = f"Error: {e}"

    return render_template_string(CSS + """
    <h1>⬇️ TikTok V4</h1>
    <div class="card">
        <form method="POST"><input name="url" placeholder="Pega link TikTok" required>
        <button class="btn" style="background:#e84393" type="submit">Descargar</button></form>
        <p style="color:#ff7675">{{msg}}</p>
    </div>
    <a class="btn" href="/" style="background:#333">Volver</a>
    """, msg=msg)

@app.route('/cnc', methods=['GET','POST'])
def cnc():
    gcode=""; img_b64=""
    if request.method == 'POST':
        desc=request.form.get('descripcion','PLACA')
        f=request.files.get('plano')
        if f and f.filename:
            img=Image.open(f.stream); buf=io.BytesIO(); img.save(buf,format="JPEG")
            img_b64=base64.b64encode(buf.getvalue()).decode()
        gcode=f"%\\nO1001 ({desc})\\nG21 G90\\nM30\\n%"
    return render_template_string(CSS + "<h1>⚙️ CNC</h1><div class='card'><form method='POST' enctype='multipart/form-data'><input name='descripcion' required><input type='file' name='plano' accept='image/*'><button class='btn' style='background:#00b894' type='submit'>Generar</button></form></div><a class='btn' href='/' style='background:#333'>Volver</a>")

if __name__ == '__main__':
    app.run()
