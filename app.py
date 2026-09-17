from flask import Flask, render_template_string
app = Flask(__name__)

HTML = """
<html><head><meta name="viewport" content="width=device-width, initial-scale=1">
<style>
body{background:#111;color:#fff;font-family:Arial;text-align:center;padding:15px}
.card{background:#222;border-radius:15px;padding:15px;margin:15px 0}
button{padding:12px 20px;border:0;border-radius:10px;margin:5px;font-weight:bold}
.red{background:#ff0040;color:#fff} .gray{background:#444;color:#fff} .white{background:#fff;color:#000}
video{width:100%;border-radius:12px;background:#000}
</style></head>
<body>
<h1>Mi Cine Hisense 📺</h1>
<input type="file" id="f" accept="video/*" multiple>
<video id="v" controls></video>

<div class="card">
<h3>Opciones</h3>
<button class="red" onclick="v.requestFullscreen()">📺 Pantalla Completa</button>
<button class="red" onclick="cast()">📡 Mandar a Hisense</button>
<button class="gray" onclick="v.playbackRate=1">▶️ Normal</button>
<button class="gray" onclick="v.playbackRate=1.
