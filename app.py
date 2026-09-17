from flask import Flask, request, jsonify
import os, requests
app=Flask(__name__)
def cerebro(m):
 k=os.environ.get("GROQ_API_KEY")
 if not k: return "Falta GROQ_API_KEY en Render > Environment, pon tu gsk..."
 try:
  d=requests.post("https://api.groq.com/openai/v1/chat/completions",headers={"Authorization":f"Bearer {k}","Content-Type":"application/json"},json={"model":"llama-3.1-8b-instant","messages":[{"role":"system","content":"Eres Bot Jorge V6, mexicano barrio, responde corto y claro"},{"role":"user","content":m}]},timeout=20).json()
  return d['choices'][0]['message']['content']
 except Exception as e: return f"Error: {e}"
@app.route('/')
def h():
 q=request.args.get('q','')
 if q: return jsonify(r=cerebro(q))
 return "<h1>BOT JORGE V6 PRO</h1><input id=q><button onclick=fetch('/?q='+q.value).then(r=>r.json()).then(d=>document.body.innerHTML+='<p>'+d.r)>OK</button>"
