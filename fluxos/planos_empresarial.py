from datetime import datetime
from utils.sessao import salvar_dado, atualizar_etapa, limpar_sessao, obter_sessao
from utils.salvar_pedido import salvar_pedido


def fluxo_plano_empresarial(numero, mensagem, sessao, enviar_mensagem):
    etapa = sessao["etapa"]

    if etapa == "plano_empresarial":
        salvar_dado(numero, "quantidade_funcionarios", mensagem)
        enviar_mensagem(numero, "Qual a cidade da empresa?")
        atualizar_etapa(numero, "empresa_cidade")
        return

    if etapa == "empresa_cidade":
        salvar_dado(numero, "empresa_cidade", mensagem)
        enviar_mensagem(
            numero,
            "Tipo de cobertura:\n"
            "1 - Básica\n"
            "2 - Intermediária\n"
            "3 - Completa"
        )
        atualizar_etapa(numero, "empresa_tipo")
        return

    if etapa == "empresa_tipo":

        if mensagem == "1":
            tipo = "basica"
            valor = 59
        elif mensagem == "2":
            tipo = "intermediaria"
            valor = 99
        elif mensagem == "3":
            tipo = "completa"
            valor = 149
        else:
            enviar_mensagem(numero, "Escolha 1, 2 ou 3.")
            return

        salvar_dado(numero, "tipo_plano", tipo)
        salvar_dado(numero, "valor_por_funcionario", valor)

        sessao_atualizada = obter_sessao(numero)
        dados = sessao_atualizada["dados"]

        total = int(dados.get("quantidade_funcionarios", 0)) * valor

        dados["total_estimado"] = total
        dados["categoria"] = "plano_empresarial"
        dados["status"] = "aguardando_contato"
        dados["data_hora"] = datetime.now().strftime("%d/%m/%Y %H:%M")

        resumo = (
            "🏢 RESUMO DO PLANO EMPRESARIAL\n\n"
            f"Funcionários: {dados.get('quantidade_funcionarios')}\n"
            f"Cidade: {dados.get('empresa_cidade')}\n"
            f"Plano: {tipo}\n"
            f"Total estimado: R$ {total}\n\n"
            "Confirmar contratação? (sim/não)"
        )

        enviar_mensagem(numero, resumo)
        atualizar_etapa(numero, "empresa_confirmar")
        return

    if etapa == "empresa_confirmar":

        if mensagem.lower() in ["sim", "s"]:
            sessao_final = obter_sessao(numero)
            salvar_pedido(sessao_final["dados"])

            enviar_mensagem(
                numero,
                "✅ Proposta registrada.\n"
                "Nossa equipe comercial entrará em contato."
            )
        else:
            enviar_mensagem(numero, "Solicitação cancelada.")

        limpar_sessao(numero)
        return