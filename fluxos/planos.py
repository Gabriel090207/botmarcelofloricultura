from datetime import datetime
from utils.sessao import salvar_dado, atualizar_etapa, limpar_sessao, obter_sessao
from utils.salvar_pedido import salvar_pedido


def fluxo_plano_familiar(numero, mensagem, sessao, enviar_mensagem):
    etapa = sessao["etapa"]

    if etapa == "plano_familiar":
        salvar_dado(numero, "quantidade_pessoas", mensagem)
        enviar_mensagem(numero, "Qual a idade média dos participantes?")
        atualizar_etapa(numero, "plano_idade")
        return

    if etapa == "plano_idade":
        salvar_dado(numero, "idade_media", mensagem)
        enviar_mensagem(
            numero,
            "Tipo de cobertura:\n"
            "1 - Básica\n"
            "2 - Intermediária\n"
            "3 - Completa"
        )
        atualizar_etapa(numero, "plano_tipo")
        return

    if etapa == "plano_tipo":

        if mensagem == "1":
            tipo = "basica"
            valor = 79
        elif mensagem == "2":
            tipo = "intermediaria"
            valor = 129
        elif mensagem == "3":
            tipo = "completa"
            valor = 199
        else:
            enviar_mensagem(numero, "Escolha 1, 2 ou 3.")
            return

        salvar_dado(numero, "tipo_plano", tipo)
        salvar_dado(numero, "valor_mensal", valor)

        sessao_atualizada = obter_sessao(numero)
        dados = sessao_atualizada["dados"]

        dados["categoria"] = "plano_familiar"
        dados["status"] = "aguardando_contato"
        dados["data_hora"] = datetime.now().strftime("%d/%m/%Y %H:%M")

        resumo = (
            "📋 RESUMO DO PLANO FAMILIAR\n\n"
            f"Pessoas: {dados.get('quantidade_pessoas')}\n"
            f"Idade média: {dados.get('idade_media')}\n"
            f"Plano: {tipo}\n"
            f"Valor mensal: R$ {valor}\n\n"
            "Confirmar contratação? (sim/não)"
        )

        enviar_mensagem(numero, resumo)
        atualizar_etapa(numero, "plano_confirmar")
        return

    if etapa == "plano_confirmar":

        if mensagem.lower() in ["sim", "s"]:
            sessao_final = obter_sessao(numero)
            salvar_pedido(sessao_final["dados"])

            enviar_mensagem(
                numero,
                "✅ Plano registrado.\n"
                "Nossa equipe entrará em contato."
            )
        else:
            enviar_mensagem(numero, "Solicitação cancelada.")

        limpar_sessao(numero)
        return