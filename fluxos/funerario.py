from datetime import datetime

from utils.salvar_pedido import salvar_pedido
from utils.sessao import salvar_dado, atualizar_etapa, limpar_sessao, obter_sessao
from servicos.calculo import calcular_orcamento
from servicos.pagamento import gerar_pagamento_simulado


def fluxo_funerario(numero, mensagem, sessao, enviar_mensagem):
    etapa = sessao["etapa"]

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

        if mensagem == "1":
            tipo = "sepultamento"
        elif mensagem == "2":
            tipo = "cremacao"
        else:
            enviar_mensagem(numero, "Escolha 1 ou 2.")
            return

        salvar_dado(numero, "tipo", tipo)

        enviar_mensagem(
            numero,
            "⚖️ Porte:\n"
            "1 - Até 80kg\n"
            "2 - 81 a 120kg\n"
            "3 - Acima 120kg"
        )
        atualizar_etapa(numero, "porte")
        return

    # ==============================
    # PORTE
    # ==============================
    if etapa == "porte":

        if mensagem == "1":
            porte = "ate_80kg"
        elif mensagem == "2":
            porte = "81_a_120kg"
        elif mensagem == "3":
            porte = "acima_120kg"
        else:
            enviar_mensagem(numero, "Escolha 1, 2 ou 3.")
            return

        salvar_dado(numero, "porte", porte)

        enviar_mensagem(
            numero,
            "⚰️ Urna:\n"
            "1 - Simples\n"
            "2 - Intermediária\n"
            "3 - Premium"
        )
        atualizar_etapa(numero, "urna")
        return

    # ==============================
    # URNA
    # ==============================
    if etapa == "urna":

        if mensagem == "1":
            urna = "simples"
        elif mensagem == "2":
            urna = "intermediaria"
        elif mensagem == "3":
            urna = "premium"
        else:
            enviar_mensagem(numero, "Escolha 1, 2 ou 3.")
            return

        salvar_dado(numero, "urna", urna)

        enviar_mensagem(numero, "🏛️ Haverá velório? (sim/não)")
        atualizar_etapa(numero, "velorio")
        return

    # ==============================
    # VELÓRIO
    # ==============================
    if etapa == "velorio":

        m = mensagem.lower().strip()
        if m in ["sim", "s"]:
            velorio = "sim"
        elif m in ["nao", "não", "n"]:
            velorio = "nao"
        else:
            enviar_mensagem(numero, "Responda com sim ou não.")
            return

        salvar_dado(numero, "velorio", velorio)

        enviar_mensagem(numero, "🚐 Será necessário traslado? (sim/não)")
        atualizar_etapa(numero, "traslado")
        return

    # ==============================
    # TRASLADO
    # ==============================
    if etapa == "traslado":

        m = mensagem.lower().strip()
        if m in ["sim", "s"]:
            traslado = "sim"
        elif m in ["nao", "não", "n"]:
            traslado = "nao"
        else:
            enviar_mensagem(numero, "Responda com sim ou não.")
            return

        salvar_dado(numero, "traslado", traslado)

        enviar_mensagem(numero, "📝 Alguma observação adicional?")
        atualizar_etapa(numero, "observacao")
        return

    # ==============================
    # OBSERVAÇÃO + RESUMO
    # ==============================
    if etapa == "observacao":

        salvar_dado(numero, "observacao", mensagem)

        sessao_atualizada = obter_sessao(numero)
        dados = sessao_atualizada["dados"]

        resultado = calcular_orcamento(dados)

        dados["valor_estimado"] = resultado["total"]
        dados["sinal_10"] = resultado["sinal_10"]
        dados["categoria"] = "servico_funerario"
        dados["status"] = "aguardando_pagamento"
        dados["data_hora"] = datetime.now().strftime("%d/%m/%Y %H:%M")

        resumo = (
            "✅ RESUMO DO ATENDIMENTO\n\n"
            f"Total estimado: R$ {resultado['total']}\n"
            f"Sinal (10%): R$ {resultado['sinal_10']}\n\n"
            "Confirmar envio? (sim/não)"
        )

        enviar_mensagem(numero, resumo)
        atualizar_etapa(numero, "confirmar")
        return

    # ==============================
    # CONFIRMAR + GERAR PAGAMENTO
    # ==============================
    if etapa == "confirmar":

        if mensagem.lower() in ["sim", "s"]:

            sessao_final = obter_sessao(numero)
            dados = sessao_final["dados"]

            pagamento = gerar_pagamento_simulado(dados)

            dados["pedido_id"] = pagamento["pedido_id"]
            dados["link_pagamento"] = pagamento["link_pagamento"]
            dados["status"] = "pagamento_gerado"

            salvar_pedido(dados)

            enviar_mensagem(
                numero,
                "💳 PAGAMENTO DO SINAL\n\n"
                f"Valor: R$ {pagamento['valor']}\n\n"
                f"Pague através do link abaixo:\n"
                f"{pagamento['link_pagamento']}\n\n"
                "Após o pagamento nossa equipe dará continuidade."
            )
        else:
            enviar_mensagem(numero, "Pedido cancelado.")

        limpar_sessao(numero)
        return