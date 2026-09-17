from flask import Flask, request, jsonify
import os, requests
app=Flask(__name__)

def cerebro(m):
    k=os.environ.get("GROQ_API_KEY")
    if not k: return "Falta GROQ_API_KEY"
    try:
        j=requests.post("https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": f"Bearer {k}", "Content-Type": "application/json"},
            json={"model":"openai/gpt-oss-20b","messages":[{"role":"system","content":"Eres Bot Jorge"},{"role":"user","content":m}]},
            timeout=25).json()
        return j['choices'][0]['message']['content']
    except Exception as e:
        return f"Error IA: {e}"

@app.route('/')
def home():
    q=request.args.get('q','')
    if q: return jsonify(r=cerebro(q))
    return """<html><body style="background:#000;color:#0f0;font-family:sans-serif;text-align:center;padding:20px">
<h1>BOT JORGE V9.1 FIX</h1><input id=q style="padding:12px;width:85%;border-radius:8px"><br><br>
<button onclick="fetch('/?q='+encodeURIComponent(q.value)).then(r=>r.json()).then(d=>a.innerText=d.r)" style="padding:12px 20px;background:#0f0;border:0;border-radius:8px;font-weight:bold">PREGUNTAR</button>
<div id=a style="margin-top:20px;background:#111;padding:15px;border-radius:10px;text-align:left;white-space:pre-wrap"></div>
<br><hr><a href=/pelis style="color:#0f0"><h2>🎬 IR A PELIS</h2></a></body></html>"""

@app.route('/pelis')
def pelis():
    q=request.args.get('q','')
    html=f"""
<html><body style="background:#000;color:#fff;font-family:sans-serif;text-align:center;padding:20px">
<h1 style="color:#0f0">🎬 BUSCADOR PELIS V9.1 FIX</h1>
<form><input name=q value="{q}" style="padding:12px;width:70%;border-radius:8px" placeholder="Jason Statham"><button style="padding:12px;background:#0f0;border:0;border-radius:8px">BUSCAR</button></form><hr>"""
    if q:
        try:
            # NUEVO DOMINIO QUE SI JALA
            url=f"https://yts.lt/api/v2/list_movies.json?query_term={q}"
            r=requests.get(url, timeout=15).json()
            movies=r.get('data',{}).get('movies',[])
            if not movies:
                html+="<p>No hay en YTS, prueba solo 'Statham' sin nombre</p>"
            for m in movies[:12]:
                html+=f"<div style='background:#111;margin:15px;padding:10px;border-radius:10px'><img src='{m['medium_cover_image']}' width=120><br><b>{m['title']} ({m['year']})</b><br>"
                for t in m.get('torrents',[]):
                    html+=f"<a href='{t['url']}' style='color:#0f0'> {t['quality']} - {t['size']} </a><br>"
                html+="</div>"
        except Exception as e:
            html+=f"<p>Error: {e} - Probando respaldo...</p>"
            # Respaldo 2
            try:
                r=requests.get(f"https://yts.am/api/v2/list_movies.json?query_term={q}", timeout=15).json()
                movies=r.get('data',{}).get('movies',[])
                for m in movies[:12]:
                    html+=f"<div style='background:#111;margin:10px;padding:10px'><b>{m['title']}</b> - <a href='{m['torrents'][0]['url']}' style='color:#0f0'>Descargar</a></div>"
            except Exception as e2:
                html+=f"<p>Fallo respaldo: {e2}</p>"
    return html+"</body></html>"

@app.route('/whatsapp', methods=['POST'])
def wa():
    msg=request.values.get('Body','')
    return f"<Response><Message>{cerebro(msg)}</Message></Response>",200,{'Content-Type':'text/xml'}
