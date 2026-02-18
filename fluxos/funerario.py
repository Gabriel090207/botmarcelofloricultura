from datetime import datetime
from utils.salvar_pedido import salvar_pedido
from utils.sessao import salvar_dado, atualizar_etapa, limpar_sessao


def fluxo_funerario(numero, mensagem, sessao, enviar_mensagem):
    etapa = sessao["etapa"]
    dados = sessao["dados"]

    # ==============================
    # NOME
    # ==============================
    if etapa == "nome":
        salvar_dado(numero, "nome_cliente", mensagem)
        enviar_mensagem(numero, "📍 Cidade do atendimento?")
        atualizar_etapa(numero, "cidade")
        return

    # ==============================
    # CIDADE
    # ==============================
    if etapa == "cidade":
        salvar_dado(numero, "cidade", mensagem)
        enviar_mensagem(
            numero,
            "⚙️ Tipo de serviço:\n1 - Sepultamento\n2 - Cremação"
        )
        atualizar_etapa(numero, "tipo")
        return

    # ==============================
    # TIPO
    # ==============================
    if etapa == "tipo":
        salvar_dado(numero, "tipo", mensagem)
        enviar_mensagem(
            numero,
            "⚖️ Porte:\n1 - Até 80kg\n2 - 81 a 120kg\n3 - Acima 120kg"
        )
        atualizar_etapa(numero, "porte")
        return

    # ==============================
    # PORTE
    # ==============================
    if etapa == "porte":
        salvar_dado(numero, "porte", mensagem)
        enviar_mensagem(
            numero,
            "⚰️ Urna:\n1 - Simples\n2 - Intermediária\n3 - Premium"
        )
        atualizar_etapa(numero, "urna")
        return

    # ==============================
    # URNA
    # ==============================
    if etapa == "urna":
        salvar_dado(numero, "urna", mensagem)
        enviar_mensagem(numero, "🏛️ Haverá velório? (sim/não)")
        atualizar_etapa(numero, "velorio")
        return

    # ==============================
    # VELÓRIO
    # ==============================
    if etapa == "velorio":
        salvar_dado(numero, "velorio", mensagem)
        enviar_mensagem(numero, "🚐 Será necessário traslado? (sim/não)")
        atualizar_etapa(numero, "traslado")
        return

    # ==============================
    # TRASLADO
    # ==============================
    if etapa == "traslado":
        salvar_dado(numero, "traslado", mensagem)
        enviar_mensagem(numero, "📝 Alguma observação adicional?")
        atualizar_etapa(numero, "observacao")
        return

    # ==============================
    # OBSERVAÇÃO + RESUMO
    # ==============================
    if etapa == "observacao":

        salvar_dado(numero, "observacao", mensagem)

        valor = 3000

        if dados["tipo"] == "2":
            valor += 2000

        if dados["porte"] == "2":
            valor += 400
        elif dados["porte"] == "3":
            valor += 900

        if dados["urna"] == "2":
            valor += 600
        elif dados["urna"] == "3":
            valor += 1500

        if dados["velorio"] in ["sim", "s"]:
            valor += 500

        if dados["traslado"] in ["sim", "s"]:
            valor += 800

        dados["valor_estimado"] = valor
        dados["data_hora"] = datetime.now().strftime("%d/%m/%Y %H:%M")

        resumo = (
            "✅ RESUMO DO ATENDIMENTO\n\n"
            f"Nome: {dados['nome_cliente']}\n"
            f"Cidade: {dados['cidade']}\n"
            f"Valor estimado: R$ {valor}\n\n"
            "Confirmar envio? (sim/não)"
        )

        enviar_mensagem(numero, resumo)

        atualizar_etapa(numero, "confirmar")
        return

    # ==============================
    # CONFIRMAR
    # ==============================
    if etapa == "confirmar":

        if mensagem in ["sim", "s"]:
            salvar_pedido(dados)
            enviar_mensagem(
                numero,
                "✅ Pedido registrado com sucesso.\n"
                "Nossa equipe entrará em contato."
            )
        else:
            enviar_mensagem(numero, "Pedido cancelado.")

        limpar_sessao(numero)
        return
