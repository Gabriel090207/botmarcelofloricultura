def calcular_orcamento(dados: dict) -> dict:
    """
    Recebe os 'dados' normalizados do atendimento e devolve:
      - total (int)
      - detalhamento (lista de itens/valores)
      - sinal_10 (int)
    """

    itens = []
    total = 0

    # Base
    base = 3000
    itens.append(("Base do serviço", base))
    total += base

    # Tipo
    if dados.get("tipo") == "cremacao":
        itens.append(("Adicional cremação", 2000))
        total += 2000

    # Porte
    porte = dados.get("porte")
    if porte == "81_a_120kg":
        itens.append(("Adicional porte 81-120kg", 400))
        total += 400
    elif porte == "acima_120kg":
        itens.append(("Adicional porte acima 120kg", 900))
        total += 900

    # Urna
    urna = dados.get("urna")
    if urna == "intermediaria":
        itens.append(("Upgrade urna intermediária", 600))
        total += 600
    elif urna == "premium":
        itens.append(("Upgrade urna premium", 1500))
        total += 1500

    # Velório
    if dados.get("velorio") == "sim":
        itens.append(("Velório", 500))
        total += 500

    # Traslado
    if dados.get("traslado") == "sim":
        itens.append(("Traslado", 800))
        total += 800

    sinal_10 = int(round(total * 0.10))

    return {
        "total": total,
        "itens": itens,
        "sinal_10": sinal_10,
    }