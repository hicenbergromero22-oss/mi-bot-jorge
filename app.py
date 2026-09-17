from flask import Flask, request, jsonify
import random

app = Flask(__name__)

def cerebro_ia(mensaje):
    mensaje = mensaje.lower()
    
    if "hola" in mensaje or "ola" in mensaje:
        return "¡Hola Crack! Soy Bot Jorge V5 con cerebro nuevo. ¿En qué te ayudo? 😎"
    elif "como estas" in mensaje:
        return "¡Al 100 bro! Ya con el cerebro V5 instalado y listo para lo que sea. ¿Tú qué tal?"
    elif "quien eres" in mensaje:
        return "Soy Bot Jorge V5, tu bot con cerebro. Ya no soy el juego del ligar, ahora sí razono y te ayudo."
    elif "ligar" in mensaje or "crack" in mensaje:
        return "Jajaja ese era el V3.1 viejo. Ahora soy V5 con cerebro, pregúntame lo que quieras y te respondo."
    elif "ayuda" in mensaje:
        return "Dime lo que necesites bro: tareas, consejos, chistes, ligar, lo que sea. ¿Qué quieres que hagamos?"
    elif mensaje.strip() == "":
        return "Escríbeme algo bro, estoy listo."
    else:
        respuestas = [
            f"Va, entendí que me dices: '{mensaje}'. ¡Dime más y te ayudo con eso!",
            f"Interesante lo de '{mensaje}' bro. A ver, cuéntame más para darte una buena respuesta.",
            f"Ok, sobre '{mensaje}'... ¿qué quieres que haga exactamente? Te ar
