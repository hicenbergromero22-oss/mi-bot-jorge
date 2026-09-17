from flask import Flask, render_template_string

app = Flask(__name__)

HTML = """
<html>
<head><meta name="viewport" content="width=device-width, initial-scale=1">
<style>body{font-family:Arial;background:#111;color:#fff;text-align:center;padding:20px}
button{padding:15px 30px;background:#ff0040;color:#fff;border:0;border-radius:10px;font-size:18px;margin:10px}
video{width:100%;max-width:700px;border-radius:15px;margin-top:15px}</style>
</head>
<body>
<h1>Mi Cine Hisense 📺</h1>
<p>Elige tu mp4 de Statham / Van Damme ya bajado</p>
<input type="file" id="f" accept="video/*">
<video id="v" controls></video><br>
<button onclick="document.getElementById('v').requestFullscreen()">Pantalla Completa</button>
<button onclick="alert('En Chrome: 3 puntitos arriba > Guardar y compartir > Transmitir > Elige Hisense TV')">Mandar a Hisense</button>
<script>
f.onchange=e=>{
  v.src=URL.createObjectURL(e.target.files[0]);
  v.play();
}
</script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
