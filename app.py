from flask import Flask, request, jsonify
import os

from utils.sessao import obter_sessao, atualizar_etapa, salvar_dado, limpar_sessao
from integracoes.ultramsg import enviar_mensagem

app = Flask(__name__)


@app.route("/", methods=["GET"])
def home():
    return "Bot Funerária Marcelo ONLINE", 200


@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        data = request.json or {}
        print("DADOS RECEBIDOS:", data)

        # UltraMsg geralmente envia assim:
        # {
        #   "data": {
        #       "from": "551699999999",
        #       "body": "oi"
        #   }
        # }

        numero = None
        mensagem = None

        # Tentativa padrão UltraMsg
        if "data" in data:
            numero = data["data"].get("from")
            mensagem = data["data"].get("body")

        # Fallback se vier diferente
        if not numero:
            numero = data.get("from")

        if not mensagem:
            mensagem = data.get("body")

        if not numero or not mensagem:
            return jsonify({"status": "ignored"}), 200

        mensagem = mensagem.strip().lower()

        # ===== CONTROLE DE SESSÃO =====
        sessao = obter_sessao(numero)
        etapa = sessao["etapa"]

        # ===== INÍCIO =====
        if etapa == "inicio":
            enviar_mensagem(
                numero,
                "👋 Olá! Bem-vindo à Funerária Marcelo.\n\n"
                "Digite:\n"
                "1️⃣ Serviço funerário\n"
                "9️⃣ Falar com atendente"
            )
            atualizar_etapa(numero, "menu")
            return jsonify({"status": "ok"}), 200

        # ===== MENU =====
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
                enviar_mensagem(
                    numero,
                    "Opção inválida.\nDigite 1 para serviço funerário."
                )

            return jsonify({"status": "ok"}), 200

        # ===== NOME =====
        if etapa == "nome":
            salvar_dado(numero, "nome_cliente", mensagem)

            enviar_mensagem(
                numero,
                f"Prazer em te atender, {mensagem}.\n\n"
                "📍 Em qual cidade ocorrerá o atendimento?"
            )

            atualizar_etapa(numero, "cidade")
            return jsonify({"status": "ok"}), 200

        # ===== CIDADE =====
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
