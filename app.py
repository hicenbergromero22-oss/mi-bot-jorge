from flask import Flask, request, render_template_string, send_file
import os, requests, base64, io, yt_dlp
from PIL import Image

app = Flask(__name__)

CSS = """
<style>
body{background:#0f0f0f;color:white;font-family:Arial;padding:20px;text-align:center}
.card{background:#1e1e1e;padding:20px;border-radius:15px;margin:15px auto;max-width:550px}
.btn{display:inline-block;padding:12px 20px;border-radius:10px;text-decoration:none;color:white;margin:5px;font-weight:bold;border:none;cursor:pointer}
input{width:90%;padding:12px;border-radius:10px;border:none;margin:10px 0}
textarea{width:90%;height:300px;background:#000;color:#0f0;padding:10px;border-radius:10px;font-size:12px}
</style>
"""

@app.route('/')
def home():
    return render_template_string(CSS + """
    <h1>Bot de Jorge - V5.1 FIX</h1>
    <div class="card">
        <a class="btn" style="background:#e84393" href="/tiktok">TikTok HD</a>
        <a class="btn" style="background:#ff0000" href="/youtube">YouTube / Insta</a>
        <a class="btn" style="background:#00b894" href="/cnc">CNC con Foto</a>
    </div>
    """)

@app.route('/tiktok', methods=['GET','POST'])
def tiktok():
    msg=""
    if request.method=='POST':
        url=request.form.get('url','').strip()
        if url:
            try:
                r=requests.post("https://www.tikwm.com/api/", data={"url":url,"count":12,"cursor":0,"web":1,"hd":1}, headers={"User-Agent":"Mozilla/5.0"}, timeout=20).json()
                data=r.get('data',{})
                play = data.get('hdplay') or data.get('play') or data.get('wmplay')
                if play:
                    if play.startswith('/'): play='https://www.tikwm.com'+play
                    v=requests.get(play, headers={"User-Agent":"Mozilla/5.0"}, stream=True, timeout=40)
                    out="/tmp/tiktok.mp4"
                    with open(out,'wb') as f:
                        for c in v.iter_content(1024*1024): f.write(c)
                    return send_file(out, as_attachment=True, download_name="tiktok_hd.mp4")
                else:
                    msg="No se pudo leer ese link."
            except Exception as e:
                msg=f"Error: {e}"
    return render_template_string(CSS+f"""
    <h1>TikTok HD Sin Marca</h1>
    <div class="card"><form method="POST"><input name="url" placeholder="Pega link TikTok" required>
    <button class="btn" style="background:#e84393" type="submit">Bajar HD</button></form><p style="color:#ff7675">{msg}</p></div>
    <a class="btn" href="/" style="background:#333">Volver</a>
    """)

@app.route('/youtube', methods=['GET','POST'])
def youtube():
    msg=""
    if request.method=='POST':
        url=request.form.get('url','').strip()
        if url:
            try:
                out="/tmp/yt.%(ext)s"
                ydl_opts={'outtmpl':out,'format':'best[ext=mp4]/best','quiet':True,'noplaylist':True}
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info=ydl.extract_info(url, download=True)
                    fname=ydl.prepare_filename(info)
                return send_file(fname, as_attachment=True, download_name="video.mp4")
            except Exception as e:
                msg=f"Error: {e}"
    return render_template_string(CSS+f"""
    <h1>YouTube / Instagram / FB</h1>
    <div class="card"><form method="POST"><input name="url" placeholder="Pega link" required>
    <button class="btn" style="background:#ff0000" type="submit">Descargar</button></form><p style="color:#ff7675">{msg}</p></div>
    <a class="btn" href="/" style="background:#333">Volver</a>
    """)

@app.route('/cnc', methods=['GET','POST'])
def cnc():
    gcode=""; img_b64=""; desc_txt=""
    if request.method=='POST':
        desc_txt=request.form.get('descripcion','PLACA 100x60')
        f=request.files.get('plano')
        if f and f.filename:
            img=Image.open(f.stream); buf=io.BytesIO(); img.save(buf,format="JPEG")
            img_b64=base64.b64encode(buf.getvalue()).decode()
        # AQUI ESTABA LA FALLA - YA ESTA ARREGLADO SIN F-STRING TRIPLE
        gcode = "%\n"
        gcode += "O1001 (" + desc_txt.upper() + ")\n"
        gcode += "G21 G40 G49 G80 G90 G17 G54\n"
        gcode += "T01 M06 (FRESA 6MM)\n"
        gcode += "G00 X0 Y0 Z50.\n"
        gcode += "M03 S1800 M08\n"
        gcode += "G00 Z5. F400\n"
        gcode += "G01 Z-2. F200\n"
        gcode += "G01 X100. F300\n"
        gcode += "Y60.\n"
        gcode += "X0 Y0\n"
        gcode += "G00 Z50. M05 M09\n"
        gcode += "M30\n%\n"
        
    return render_template_string(CSS+f"""
    <h1>CNC con Foto</h1>
    <div class="card">
        <form method="POST" enctype="multipart/form-data">
            <input name="descripcion" placeholder="Ej: Placa 100x60" value="{desc_txt}" required>
            <input type="file" name="plano" accept="image/*">
            <button class="btn" style="background:#00b894" type="submit">Generar G-CODE</button>
        </form>
    </div>
    <a class="btn" href="/" style="background:#333">Volver</a>
    """)

if __name__=='__main__':
    app.run()
