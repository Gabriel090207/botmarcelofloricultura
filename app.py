from flask import Flask, request, jsonify

from utils.sessao import obter_sessao, atualizar_etapa, salvar_dado
from integracoes.ultramsg import enviar_mensagem

app = Flask(__name__)


@app.route("/", methods=["GET"])
def home():
    return "Bot Funerária Marcelo online", 200


@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json or {}

    # Ajuste conforme payload real da UltraMsg
    numero = data.get("from", "")
    mensagem = data.get("body", "").strip().lower()

    if not numero:
        return jsonify({"status": "ignored"}), 200

    sessao = obter_sessao(numero)
    etapa = sessao["etapa"]

    if etapa == "inicio":
        enviar_mensagem(
            numero,
            "Olá! Bem-vindo à Funerária Marcelo.\n"
            "Digite:\n"
            "1 - Serviço funerário\n"
            "0 - Falar com atendente"
        )
        atualizar_etapa(numero, "menu")
        return jsonify({"status": "ok"}), 200

    if etapa == "menu":
        if mensagem == "1":
            enviar_mensagem(
                numero,
                "Antes de continuarmos, qual é o seu nome?"
            )
            atualizar_etapa(numero, "nome")
        else:
            enviar_mensagem(
                numero,
                "Encaminhando para um atendente."
            )
            atualizar_etapa(numero, "inicio")

        return jsonify({"status": "ok"}), 200

    if etapa == "nome":
        salvar_dado(numero, "nome_cliente", mensagem)
        enviar_mensagem(
            numero,
            f"Prazer em te atender, {mensagem}.\n"
            "Em qual cidade ocorrerá o atendimento?"
        )
        atualizar_etapa(numero, "cidade")
        return jsonify({"status": "ok"}), 200

    if etapa == "cidade":
        salvar_dado(numero, "cidade", mensagem)

        enviar_mensagem(
            numero,
            "Obrigado. Nossa equipe dará continuidade ao atendimento."
        )

        atualizar_etapa(numero, "inicio")
        return jsonify({"status": "ok"}), 200

    return jsonify({"status": "ok"}), 200


if __name__ == "__main__":
    app.run(debug=True)
