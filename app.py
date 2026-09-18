@app.route('/')
def inicio():
    return """
    <style>
        body{background:#111;color:white;font-family:sans-serif;text-align:center;padding:20px}
        .btn{display:block;background:#ff0040;color:white;padding:18px;margin:15px;border-radius:12px;text-decoration:none;font-size:18px;font-weight:bold}
    </style>
    <h1>Bot Jorge V7 🔥</h1>
    <a class="btn" href="/chat">💬 Preguntar lo que sea</a>
    <a class="btn" href="/descargar">📲 Descargar TikToks / Reels sin marca</a>
    <a class="btn" href="/pelis">🎬 Buscar Películas</a>
    <a class="btn" href="/cine" style="background:#333">📺 Mi Cine Hisense</a>
    """
