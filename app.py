from flask import Flask, request, jsonify
import os

from utils.sessao import (
    obter_sessao,
    atualizar_etapa,
    salvar_dado,
    limpar_sessao,
)

from integracoes.ultramsg import (
    enviar_mensagem,
    enviar_botoes,
)

app = Flask(__name__)


@app.route("/", methods=["GET"])
def home():
    return "Bot Funerária Marcelo ONLINE", 200


@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        data = request.json or {}
        print("DADOS RECEBIDOS:", data)

        # 🔥 IGNORAR mensagens enviadas pelo próprio bot
        if data.get("data", {}).get("fromMe") is True:
            return jsonify({"status": "ignored_self"}), 200

        numero = None
        mensagem = None

        if "data" in data:
            numero = data["data"].get("from")
            mensagem = data["data"].get("body")

        if not numero or not mensagem:
            return jsonify({"status": "no message"}), 200

        # remover sufixo @c.us
        numero = numero.replace("@c.us", "")
        mensagem = mensagem.strip().lower()

        sessao = obter_sessao(numero)
        etapa = sessao["etapa"]

        # ==============================
        # INÍCIO
        # ==============================
        if etapa == "inicio":

            enviar_botoes(
                numero,
                "Funerária Marcelo",
                "👋 Olá! Como podemos ajudar?",
                [
                    {"id": "1", "title": "Serviço funerário"},
                    {"id": "9", "title": "Falar com atendente"}
                ]
            )

            atualizar_etapa(numero, "menu")
            return jsonify({"status": "ok"}), 200

        # ==============================
        # MENU
        # ==============================
        if etapa == "menu":

            if mensagem == "1":

                enviar_mensagem(
                    numero,
                    "Antes de continuarmos, qual é o seu nome?"
                )

                atualizar_etapa(numero, "nome")

            elif mensagem == "9":

                enviar_mensagem(
                    numero,
                    "👤 Um atendente humano falará com você em instantes."
                )

                limpar_sessao(numero)

            else:

                enviar_botoes(
                    numero,
                    "Funerária Marcelo",
                    "Escolha uma opção válida:",
                    [
                        {"id": "1", "title": "Serviço funerário"},
                        {"id": "9", "title": "Falar com atendente"}
                    ]
                )

            return jsonify({"status": "ok"}), 200

        # ==============================
        # NOME
        # ==============================
        if etapa == "nome":

            salvar_dado(numero, "nome_cliente", mensagem)

            enviar_mensagem(
                numero,
                f"Prazer em te atender, {mensagem}.\n\n"
                "📍 Em qual cidade ocorrerá o atendimento?"
            )

            atualizar_etapa(numero, "cidade")
            return jsonify({"status": "ok"}), 200

        # ==============================
        # CIDADE
        # ==============================
        if etapa == "cidade":

            salvar_dado(numero, "cidade", mensagem)

            enviar_mensagem(
                numero,
                "Obrigado.\nNossa equipe entrará em contato imediatamente."
            )

            limpar_sessao(numero)
            return jsonify({"status": "ok"}), 200

        return jsonify({"status": "ok"}), 200

    except Exception as e:
        print("ERRO NO WEBHOOK:", e)
        return jsonify({"status": "error"}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
