from flask import Flask, request, jsonify
import os, requests
app=Flask(__name__)

# --- CEREBRO V6 ---
def cerebro(m):
    k=os.environ.get("GROQ_API_KEY")
    if not k: return "Pon tu GROQ_API_KEY en Render > Environment"
    try:
        j=requests.post("https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": f"Bearer {k}", "Content-Type": "application/json"},
            json={"model":"openai/gpt-oss-20b","messages":[{"role":"system","content":"Eres Bot Jorge V9, mexicano barrio, corto, buena onda, sabes de todo."},{"role":"user","content":m}]},
            timeout=30).json()
        return j['choices'][0]['message']['content']
    except Exception as e:
        # Si falla ese modelo, prueba el otro
        try:
            j=requests.post("https://api.groq.com/openai/v1/chat/completions",
                headers={"Authorization": f"Bearer {k}", "Content-Type": "application/json"},
                json={"model":"openai/gpt-oss-120b","messages":[{"role":"system","content":"Eres Bot Jorge"},{"role":"user","content":m}]},
                timeout=30).json()
            return j['choices'][0]['message']['content']
        except Exception as e2:
            return f"Error: {e} / {e2} - {j if 'j' in locals() else ''}"

@app.route('/')
def home():
    q=request.args.get('q','')
    if q: return jsonify(r=cerebro(q))
    return """
<html><body style="background:#000;color:#0f0;font-family:sans-serif;text-align:center;padding:20px">
<h1>BOT JORGE V9 - TODO EN 1</h1>
<input id=q style="padding:12px;width:85%;border-radius:8px" placeholder="Pregunta lo que sea">
<br><br>
<button onclick="fetch('/?q='+encodeURIComponent(q.value)).then(r=>r.json()).then(d=>a.innerText=d.r)" style="padding:12px 20px;background:#0f0;border:0;border-radius:8px;font-weight:bold">PREGUNTAR</button>
<div id=a style="margin-top:20px;background:#111;padding:15px;border-radius:10px;text-align:left;white-space:pre-wrap"></div>
<hr style="margin:30px 0">
<h2>🎬 PELIS</h2><a href=/pelis style="color:#0f0">Ir a buscador de pelis -> /pelis</a>
<h2>📥 TIKTOK / YOUTUBE</h2><a href=/descargar style="color:#0f0">Ir a descargador -> /descargar</a>
<h2>💬 WHATSAPP</h2><p>Endpoint: /whatsapp (para Twilio)</p>
</body></html>
"""

# --- WHATSAPP ---
@app.route('/whatsapp', methods=['POST'])
def wa():
    msg=request.values.get('Body','') or request.values.get('body','')
    resp=cerebro(msg) if msg else "Hola soy Bot Jorge V9"
    # Respuesta para Twilio
    return f"<Response><Message>{resp}</Message></Response>", 200, {'Content-Type':'text/xml'}

# --- PELIS - YTS ---
@app.route('/pelis')
def pelis():
    q=request.args.get('q','')
    html="""
<html><body style="background:#000;color:#fff;font-family:sans-serif;text-align:center;padding:20px">
<h1 style="color:#0f0">🎬 BUSCADOR PELIS V9</h1>
<form><input name=q value='{0}' style="padding:12px;width:70%;border-radius:8px" placeholder="Ej: Deadpool"><button style="padding:12px;background:#0f0;border:0;border-radius:8px">BUSCAR</button></form><hr>
""".format(q)
    if q:
        try:
            r=requests.get(f"https://yts.mx/api/v2/list_movies.json?query_term={q}", timeout=15).json()
            movies=r.get('data',{}).get('movies',[])
            if not movies: html+="<p>No encontradas</p>"
            for m in movies[:10]:
                html+=f"<div style='background:#111;margin:15px;padding:10px;border-radius:10px'><img src='{m['medium_cover_image']}' width=120><br><b>{m['title']} ({m['year']})</b><br>"
                for t in m.get('torrents',[]):
                    html+=f"<a href='{t['url']}' style='color:#0f0'>Descargar {t['quality']} {t['size']}</a> | "
                html+="</div>"
        except Exception as e:
            html+=f"<p>Error pelis: {e}</p>"
    return html+"</body></html>"

# --- DESCARGADOR TIKTOK ---
@app.route('/descargar')
def descargar():
    link=request.args.get('q','')
    html="""
<html><body style="background:#000;color:#fff;font-family:sans-serif;text-align:center;padding:20px">
<h1 style="color:#0f0">📥 DESCARGADOR SIN MARCA</h1>
<form><input name=q value='' style="padding:12px;width:70%;border-radius:8px" placeholder="Pega link de TikTok"><button style="padding:12px;background:#0f0;border:0;border-radius:8px">BAJAR</button></form>
"""
    if link:
        try:
            # API gratis tikwm
            r=requests.get(f"https://www.tikwm.com/api/?url={link}", headers={"User-Agent":"Mozilla"}, timeout=15).json()
            if r.get('data'):
                v=r['data'].get('play') or r['data'].get('hdplay')
                html+=f"<br><video src='{v}' controls style='width:90%'></video><br><br><a href='{v}' style='background:#0f0;color:#000;padding:12px;border-radius:8px;text-decoration:none'>DESCARGAR VIDEO</a>"
            else:
                html+=f"<p>No se pudo: {r}</p>"
        except Exception as e:
            html+=f"<p>Error: {e}</p>"
    return html+"</body></html>"
