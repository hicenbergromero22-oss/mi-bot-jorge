from flask import Flask, request, jsonify
import os, requests
app=Flask(__name__)

def cerebro(m):
    k=os.environ.get("GROQ_API_KEY")
    if not k:
        return "Falta GROQ_API_KEY en Render > Environment"
    try:
        r=requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": f"Bearer {k}", "Content-Type": "application/json"},
            json={
                "model":"llama-3.1-8b-instant",
                "messages":[
                    {"role":"system","content":"Eres Bot Jorge V6, mexicano barrio, buena onda, corto y claro."},
                    {"role":"user","content":m}
                ]
            },
            timeout=25
        ).json()
        return r['choices'][0]['message']['content']
    except Exception as e:
        return f"Error: {e} - {r if 'r' in locals() else ''}"

@app.route('/')
def h():
    q=request.args.get('q','')
    if q:
        return jsonify(r=cerebro(q))
    return """
<html><body style="background:#000;color:#0f0;font-family:sans-serif;text-align:center;padding:20px">
<h1>BOT JORGE V6 PRO - YA JALA</h1>
<input id=q style="padding:12px;width:80%;border-radius:8px" placeholder="Pregunta lo que sea, ej: teja?">
<br><br>
<button onclick="fetch('/?q='+encodeURIComponent(document.getElementById('q').value)).then(r=>r.json()).then(d=>{document.getElementById('a').innerText=d.r})" style="padding:12px 20px;background:#0f0;border:0;border-radius:8px;font-weight:bold">PREGUNTAR</button>
<div id=a style="margin-top:20px;background:#111;padding:15px;border-radius:10px;text-align:left;white-space:pre-wrap"></div>
</body></html>
"""
