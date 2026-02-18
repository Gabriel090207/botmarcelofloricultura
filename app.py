from flask import Flask, request, jsonify

from utils.sessao import obter_sessao, atualizar_etapa
from integracoes.ultramsg import enviar_mensagem
from fluxos.funerario import fluxo_funerario

app = Flask(__name__)


@app.route("/", methods=["GET"])
def home():
    return "Bot Funerária Marcelo ONLINE", 200


@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        data = request.json or {}

        # Ignorar mensagens do próprio bot
        if data.get("data", {}).get("fromMe") is True:
            return jsonify({"status": "ignored"}), 200

        numero = data["data"].get("from")
        mensagem = data["data"].get("body")

        if not numero or not mensagem:
            return jsonify({"status": "no message"}), 200

        numero = numero.replace("@c.us", "")
        mensagem = mensagem.strip().lower()

        sessao = obter_sessao(numero)
        etapa = sessao["etapa"]

        # MENU INICIAL
        if etapa == "inicio":

            enviar_mensagem(
                numero,
                "👋 Bem-vindo à Funerária Marcelo.\n\n"
                "Digite:\n"
                "1 - Serviço funerário\n"
                "9 - Falar com atendente"
            )

            atualizar_etapa(numero, "menu")
            return jsonify({"status": "ok"}), 200

        # MENU
        if etapa == "menu":

            if mensagem == "1":
                enviar_mensagem(numero, "Qual é o seu nome?")
                atualizar_etapa(numero, "nome")
                return jsonify({"status": "ok"}), 200

            elif mensagem == "9":
                enviar_mensagem(numero, "Um atendente falará com você.")
                return jsonify({"status": "ok"}), 200

            else:
                enviar_mensagem(numero, "Digite 1 ou 9.")
                return jsonify({"status": "ok"}), 200

        # FLUXO FUNERÁRIO
        fluxo_funerario(numero, mensagem, sessao, enviar_mensagem)

        return jsonify({"status": "ok"}), 200

    except Exception as e:
        print("ERRO:", e)
        return jsonify({"status": "error"}), 500
