from datetime import datetime

from utils.perguntas import (
    perguntar_texto,
    perguntar_telefone,
    perguntar_sim_nao,
    perguntar_opcao,
)


from utils.salvar_pedido import salvar_pedido



def iniciar_servico_funerario():
    print("\n🕊️ Atendimento Funerário - Funerária Marcelo")
    print("Sentimos muito pela sua perda.")
    print("Vou fazer algumas perguntas para agilizar o atendimento.\n")

    cliente_nome = perguntar_texto(
        "Antes de começarmos, qual é o seu nome? "
    )

    print(f"\nPrazer em te atender, {cliente_nome}.\n")

    pedido = {}
    pedido["data_hora"] = datetime.now().strftime("%d/%m/%Y %H:%M")

    print("📍 DADOS DO ATENDIMENTO\n")

    pedido["cidade"] = perguntar_texto("Cidade do atendimento: ")
    pedido["bairro"] = perguntar_texto(
        "Bairro (opcional): ", obrigatorio=False, min_len=0
    )
    pedido["endereco"] = perguntar_texto(
        "Endereço ou referência (opcional): ",
        obrigatorio=False,
        min_len=0,
    )

    print("\n👤 RESPONSÁVEL\n")

    print(f"{cliente_nome}, você é o responsável pelo atendimento?")
    confirm_resp = perguntar_sim_nao("(sim/não): ")

    if confirm_resp:
        pedido["responsavel_nome"] = cliente_nome
    else:
        pedido["responsavel_nome"] = perguntar_texto(
            "Nome do responsável: "
        )

    pedido["responsavel_telefone"] = perguntar_telefone(
        "Telefone do responsável: "
    )

    pedido["responsavel_documento"] = perguntar_texto(
        "CPF (opcional): ",
        obrigatorio=False,
        min_len=0,
    )

    print("\n🕯️ DADOS DO FALECIDO\n")

    pedido["falecido_nome"] = perguntar_texto("Nome do falecido: ")
    pedido["falecido_idade"] = perguntar_texto(
        "Idade aproximada (opcional): ",
        obrigatorio=False,
        min_len=0,
    )

    print("\n⚙️ TIPO DE SERVIÇO\n")

    tipo_cod, tipo_desc = perguntar_opcao(
        "Qual tipo de atendimento?",
        {"1": "Sepultamento", "2": "Cremação"},
    )

    pedido["tipo_servico_cod"] = tipo_cod
    pedido["tipo_servico"] = tipo_desc

    print("\n⚖️ PORTE / PESO\n")

    porte_cod, porte_desc = perguntar_opcao(
        "Qual porte aproximado?",
        {
            "1": "Até 80 kg",
            "2": "81 a 120 kg",
            "3": "Acima de 120 kg",
        },
    )

    pedido["porte_cod"] = porte_cod
    pedido["porte"] = porte_desc

    print("\n⚰️ URNA\n")

    urna_cod, urna_desc = perguntar_opcao(
        "Escolha o modelo de urna:",
        {
            "1": "Simples",
            "2": "Intermediária",
            "3": "Premium",
        },
    )

    pedido["urna_cod"] = urna_cod
    pedido["urna"] = urna_desc

    print("\n🏛️ VELÓRIO\n")

    tem_velorio = perguntar_sim_nao("Haverá velório? ")

    pedido["velorio"] = "Sim" if tem_velorio else "Não"

    if tem_velorio:
        pedido["local_velorio"] = perguntar_texto(
            "Local do velório: "
        )
    else:
        pedido["local_velorio"] = ""

    print("\n🚐 TRASLADO\n")

    precisa_traslado = perguntar_sim_nao(
        "Será necessário traslado? "
    )

    pedido["traslado"] = "Sim" if precisa_traslado else "Não"

    if precisa_traslado:
        pedido["traslado_origem"] = perguntar_texto(
            "Origem do traslado: "
        )
        pedido["traslado_destino"] = perguntar_texto(
            "Destino do traslado: "
        )
    else:
        pedido["traslado_origem"] = ""
        pedido["traslado_destino"] = ""

    pedido["observacoes"] = perguntar_texto(
        "\nObservações adicionais (opcional): ",
        obrigatorio=False,
        min_len=0,
    )

    valor = 3000

    if pedido["tipo_servico_cod"] == "2":
        valor += 2000

    if pedido["porte_cod"] == "2":
        valor += 400
    elif pedido["porte_cod"] == "3":
        valor += 900

    if pedido["urna_cod"] == "2":
        valor += 600
    elif pedido["urna_cod"] == "3":
        valor += 1500

    if tem_velorio:
        valor += 500

    if precisa_traslado:
        valor += 800

    pedido["valor_estimado"] = valor

    print("\n✅ RESUMO DO ATENDIMENTO")
    print("----------------------------------")
    print("Cidade:", pedido["cidade"])
    print("Responsável:", pedido["responsavel_nome"])
    print("Falecido:", pedido["falecido_nome"])
    print("Tipo:", pedido["tipo_servico"])
    print("Urna:", pedido["urna"])
    print("Velório:", pedido["velorio"])
    print("Traslado:", pedido["traslado"])
    print(f"💰 Valor estimado: R$ {valor}")
    print("----------------------------------\n")

    confirmar = perguntar_sim_nao(
        "Deseja enviar o pedido para o plantonista? "
    )

    if confirmar:
        salvar_pedido(pedido)

        print(f"\n✅ Atendimento registrado, {cliente_nome}.")
        print("Nossa equipe entrará em contato em seguida.\n")
    else:
        print("\nPedido não enviado.\n")

