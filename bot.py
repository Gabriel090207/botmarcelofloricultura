from fluxos.funerario import iniciar_servico_funerario
from utils.botoes import menu_texto


def menu_principal():
    while True:
        opcoes = {
            "1": "Serviço funerário",
            "2": "Coroas e flores",
            "3": "Planos familiares",
            "9": "Falar com atendente",
            "0": "Sair"
        }

        escolha = menu_texto(
            "=== FUNERÁRIA MARCELO ===",
            opcoes
        )

        if escolha in opcoes:
            return escolha

        print("\n⚠️ Opção inválida.\n")


while True:
    op = menu_principal()

    if op == "1":
        iniciar_servico_funerario()

    elif op == "2":
        print("\n🌷 Em breve: venda de coroas e flores.\n")

    elif op == "3":
        print("\n📄 Em breve: planos familiares.\n")

    elif op == "9":
        print("\n👤 Encaminhando para atendente humano...\n")

    elif op == "0":
        print("\nAtendimento encerrado.\n")
        break
