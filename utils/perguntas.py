def perguntar_texto(pergunta, obrigatorio=True, min_len=2):
    while True:
        resp = input(pergunta).strip()

        if not resp and obrigatorio:
            print("⚠️ Informação obrigatória.\n")
            continue

        if obrigatorio and len(resp) < min_len:
            print("⚠️ Resposta muito curta.\n")
            continue

        return resp


def perguntar_telefone(pergunta):
    while True:
        resp = input(pergunta).strip()
        digitos = "".join(c for c in resp if c.isdigit())

        if len(digitos) < 8:
            print("⚠️ Telefone inválido. Informe com DDD.\n")
            continue

        return resp


def perguntar_sim_nao(pergunta):
    while True:
        resp = input(pergunta).strip().lower()

        if resp in ["s", "sim"]:
            return True
        if resp in ["n", "nao", "não"]:
            return False

        print("⚠️ Responda sim ou não.\n")


def perguntar_opcao(pergunta, opcoes):
    while True:
        print(pergunta)

        for k, v in opcoes.items():
            print(f"{k} - {v}")

        resp = input("Escolha uma opção: ").strip()

        if resp in opcoes:
            return resp, opcoes[resp]

        print("⚠️ Opção inválida.\n")
