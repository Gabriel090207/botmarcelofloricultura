import os
import json
from datetime import datetime


PASTA_PEDIDOS = "dados/pedidos"


def confirmar_pagamento_por_id(pedido_id: str) -> bool:
    """
    Procura o pedido pelo pedido_id,
    atualiza status para 'pago'
    e adiciona data_pagamento.
    """

    for nome_arquivo in os.listdir(PASTA_PEDIDOS):
        caminho = os.path.join(PASTA_PEDIDOS, nome_arquivo)

        with open(caminho, "r", encoding="utf-8") as f:
            dados = json.load(f)

        if dados.get("pedido_id") == pedido_id:
            dados["status"] = "pago"
            dados["data_pagamento"] = datetime.now().strftime("%d/%m/%Y %H:%M")

            with open(caminho, "w", encoding="utf-8") as f:
                json.dump(dados, f, indent=4, ensure_ascii=False)

            return True

    return False