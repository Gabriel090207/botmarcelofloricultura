import uuid


def gerar_pagamento_simulado(dados: dict) -> dict:
    """
    Gera um link de pagamento fictício
    (estrutura pronta para Mercado Pago depois)
    """

    pedido_id = str(uuid.uuid4())[:8]

    link_pagamento = f"https://pagamento.local/{pedido_id}"

    return {
        "pedido_id": pedido_id,
        "link_pagamento": link_pagamento,
        "valor": dados.get("sinal_10") or dados.get("valor_estimado"),
    }