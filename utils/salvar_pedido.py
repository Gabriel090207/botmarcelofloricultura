import os
import json
from datetime import datetime


def salvar_pedido(pedido):
    pasta = "dados/pedidos"

    # garante que a pasta existe
    os.makedirs(pasta, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nome_arquivo = f"pedido_{timestamp}.json"

    caminho = os.path.join(pasta, nome_arquivo)

    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(pedido, f, ensure_ascii=False, indent=4)

    print(f"\n💾 Pedido salvo em: {caminho}")
