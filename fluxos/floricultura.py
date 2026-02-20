from datetime import datetime
from utils.sessao import salvar_dado, atualizar_etapa, limpar_sessao, obter_sessao
from utils.salvar_pedido import salvar_pedido


def fluxo_floricultura(numero, mensagem, sessao, enviar_mensagem):
    etapa = sessao["etapa"]

    if etapa == "floricultura":

        if mensagem == "1":
            produto = "coroa_padrao"
            valor = 250
        elif mensagem == "2":
            produto = "coroa_luxo"
            valor = 450
        elif mensagem == "3":
            produto = "arranjo_especial"
            valor = 350
        else:
            enviar_mensagem(numero, "Escolha 1, 2 ou 3.")
            return

        salvar_dado(numero, "produto", produto)
        salvar_dado(numero, "valor_produto", valor)

        enviar_mensagem(numero, "Qual mensagem deseja colocar na faixa?")
        atualizar_etapa(numero, "flor_mensagem")
        return

    if etapa == "flor_mensagem":
        salvar_dado(numero, "mensagem_faixa", mensagem)
        enviar_mensagem(numero, "Local de entrega?")
        atualizar_etapa(numero, "flor_local")
        return

    if etapa == "flor_local":

        salvar_dado(numero, "local_entrega", mensagem)

        sessao_atualizada = obter_sessao(numero)
        dados = sessao_atualizada["dados"]

        dados["categoria"] = "floricultura"
        dados["status"] = "aguardando_pagamento"
        dados["data_hora"] = datetime.now().strftime("%d/%m/%Y %H:%M")

        resumo = (
            "🌹 RESUMO DO PEDIDO\n\n"
            f"Produto: {dados.get('produto')}\n"
            f"Valor: R$ {dados.get('valor_produto')}\n"
            f"Entrega: {dados.get('local_entrega')}\n\n"
            "Confirmar pedido? (sim/não)"
        )

        enviar_mensagem(numero, resumo)
        atualizar_etapa(numero, "flor_confirmar")
        return

    if etapa == "flor_confirmar":

        if mensagem.lower() in ["sim", "s"]:
            sessao_final = obter_sessao(numero)
            salvar_pedido(sessao_final["dados"])

            enviar_mensagem(
                numero,
                "✅ Pedido registrado.\n"
                "Aguardando pagamento."
            )
        else:
            enviar_mensagem(numero, "Pedido cancelado.")

        limpar_sessao(numero)
        return