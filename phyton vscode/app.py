from flask import Flask, request
from config import VERIFY_TOKEN
from services.commands import processar
from database import init_db
from scheduler import iniciar_scheduler

app = Flask(__name__)

init_db()
iniciar_scheduler()

@app.route("/webhook", methods=["GET"])
def verify():
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if token == VERIFY_TOKEN:
        return challenge
    return "erro", 403

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json

    try:
        msg = data["entry"][0]["changes"][0]["value"]["messages"][0]
        numero = msg["from"]
        texto = msg["text"]["body"]

        processar(numero, texto)

    except:
        pass

    return "ok", 200

if __name__ == "__main__":
    app.run()