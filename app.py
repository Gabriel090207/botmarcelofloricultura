from flask import Flask, request, jsonify

from utils.sessao import obter_sessao, atualizar_etapa, limpar_sessao
from utils.interpretador import interpretar_entrada

from integracoes.ultramsg import enviar_mensagem

from fluxos.funerario import fluxo_funerario
from fluxos.planos import fluxo_plano_familiar
from fluxos.planos_empresarial import fluxo_plano_empresarial
from fluxos.floricultura import fluxo_floricultura

app = Flask(__name__)


@app.route("/", methods=["GET"])
def home():
    return "Bot Funerária Marcelo ONLINE", 200


def texto_menu_principal() -> str:
    return (
        "👋 Bem-vindo à Funerária Marcelo.\n\n"
        "Escolha uma opção:\n"
        "1 - Serviços funerários\n"
        "2 - Planos Familiares\n"
        "3 - Planos Empresariais\n"
        "4 - Floricultura\n"
        "9 - Falar com atendente"
    )


def processar_mensagem(numero, mensagem):
    numero = (numero or "").replace("@c.us", "").strip()
    mensagem = (mensagem or "").strip()

    if not numero or not mensagem:
        return None

    comando = interpretar_entrada(mensagem)

    sessao = obter_sessao(numero)
    etapa = sessao.get("etapa", "inicio")

    resposta = None

    # ==============================
    # INÍCIO (mostra menu)
    # ==============================
    if etapa == "inicio":
        resposta = texto_menu_principal()
        atualizar_etapa(numero, "menu")

        enviar_mensagem(numero, resposta)
        return resposta

    # ==============================
    # MENU PRINCIPAL
    # ==============================
    if etapa == "menu":

        if comando == "MENU_SERVICOS":
            resposta = "🕊 Serviços funerários selecionado.\nQual é o seu nome?"
            atualizar_etapa(numero, "nome")
            enviar_mensagem(numero, resposta)
            return resposta

        if comando == "MENU_PLANOS_FAMILIARES":
            resposta = (
                "👨‍👩‍👧 Planos Familiares selecionado.\n"
                "Quantas pessoas participarão do plano?"
            )
            atualizar_etapa(numero, "plano_familiar")
            enviar_mensagem(numero, resposta)
            return resposta

        if comando == "MENU_PLANOS_EMPRESARIAIS":
            resposta = (
                "🏢 Planos Empresariais selecionado.\n"
                "Quantos funcionários a empresa possui?"
            )
            atualizar_etapa(numero, "plano_empresarial")
            enviar_mensagem(numero, resposta)
            return resposta

        if comando == "MENU_FLORICULTURA":
            resposta = (
                "🌹 Floricultura selecionado.\n"
                "Escolha uma opção:\n"
                "1 - Coroa padrão (R$ 250)\n"
                "2 - Coroa luxo (R$ 450)\n"
                "3 - Arranjo especial (R$ 350)"
            )
            atualizar_etapa(numero, "floricultura")
            enviar_mensagem(numero, resposta)
            return resposta

        if comando == "MENU_ATENDENTE":
            resposta = "👤 Um atendente falará com você em instantes."
            atualizar_etapa(numero, "atendente")
            enviar_mensagem(numero, resposta)
            return resposta

        resposta = "Escolha uma opção válida do menu."
        enviar_mensagem(numero, resposta)
        return resposta

    # ==============================
    # ATENDENTE (por enquanto só mantém)
    # ==============================
    if etapa == "atendente":
        # Aqui no futuro: registrar ticket, avisar painel, etc.
        enviar_mensagem(numero, "👤 Você já está na fila do atendente. Em instantes alguém te responde.")
        return None

    # ==============================
    # FLUXO FUNERÁRIO
    # ==============================
    if etapa in ["nome", "cidade", "tipo", "porte", "urna", "velorio", "traslado", "observacao", "confirmar"]:
        fluxo_funerario(numero, mensagem, sessao, enviar_mensagem)
        return None

    # ==============================
    # PLANO FAMILIAR
    # ==============================
    if etapa in ["plano_familiar", "plano_idade", "plano_tipo", "plano_confirmar"]:
        fluxo_plano_familiar(numero, mensagem, sessao, enviar_mensagem)
        return None

    # ==============================
    # PLANO EMPRESARIAL
    # ==============================
    if etapa in ["plano_empresarial", "empresa_cidade", "empresa_tipo", "empresa_confirmar"]:
        fluxo_plano_empresarial(numero, mensagem, sessao, enviar_mensagem)
        return None

    # ==============================
    # FLORICULTURA
    # ==============================
    if etapa in ["floricultura", "flor_mensagem", "flor_local", "flor_confirmar"]:
        fluxo_floricultura(numero, mensagem, sessao, enviar_mensagem)
        return None

    # ==============================
    # FALLBACK: se etapa estiver desconhecida
    # ==============================
    resposta = "Vamos recomeçar 😊\n\n" + texto_menu_principal()
    limpar_sessao(numero)
    enviar_mensagem(numero, resposta)
    return resposta


@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        data = request.json or {}

        # Ignorar mensagens do próprio bot
        if data.get("data", {}).get("fromMe") is True:
            return jsonify({"status": "ignored"}), 200

        numero = data.get("data", {}).get("from")
        mensagem = data.get("data", {}).get("body")

        if not numero or not mensagem:
            return jsonify({"status": "no message"}), 200

        processar_mensagem(numero, mensagem)

        return jsonify({"status": "ok"}), 200

    except Exception as e:
        print("ERRO:", e)
        return jsonify({"status": "error"}), 500


from utils.atualizar_pedido import confirmar_pagamento_por_id


@app.route("/confirmar_pagamento/<pedido_id>", methods=["GET"])
def confirmar_pagamento(pedido_id):
    sucesso = confirmar_pagamento_por_id(pedido_id)

    if sucesso:
        return jsonify({
            "status": "ok",
            "mensagem": "Pagamento confirmado com sucesso."
        }), 200
    else:
        return jsonify({
            "status": "erro",
            "mensagem": "Pedido não encontrado."
        }), 404

# ==============================
# MODO TERMINAL (LOCAL)
# ==============================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)