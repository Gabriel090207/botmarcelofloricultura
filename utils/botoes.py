def menu_texto(titulo, opcoes):
    """
    Exibe menu em texto (modo terminal)
    e retorna opção escolhida.
    """

    print(f"\n{titulo}\n")

    for chave, descricao in opcoes.items():
        print(f"{chave} - {descricao}")

    escolha = input("\nEscolha uma opção: ").strip()
    return escolha


def gerar_botoes_whatsapp(titulo, opcoes):
    """
    Estrutura futura para WhatsApp.
    Ainda não envia, só prepara formato.
    """

    botoes = []

    for chave, descricao in opcoes.items():
        botoes.append({
            "id": chave,
            "title": descricao
        })

    return {
        "title": titulo,
        "buttons": botoes
    }
