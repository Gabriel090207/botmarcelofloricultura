import requests
import os
import json


ULTRAMSG_INSTANCE = os.environ.get("ULTRAMSG_INSTANCE")
ULTRAMSG_TOKEN = os.environ.get("ULTRAMSG_TOKEN")


def enviar_mensagem(numero, mensagem):
    url = f"https://api.ultramsg.com/{ULTRAMSG_INSTANCE}/messages/chat"

    payload = {
        "token": ULTRAMSG_TOKEN,
        "to": numero,
        "body": mensagem,
    }

    response = requests.post(url, data=payload)
    print("RESPOSTA CHAT:", response.text)
    return response.text


def enviar_botoes(numero, titulo, texto, botoes):
    """
    Envio de botão no formato novo da UltraMsg
    """

    url = f"https://api.ultramsg.com/{ULTRAMSG_INSTANCE}/messages/interactive"

    payload = {
        "token": ULTRAMSG_TOKEN,
        "to": numero,
        "type": "button",
        "header": titulo,
        "body": texto,
        "footer": "",
        "buttons": json.dumps(botoes)
    }

    response = requests.post(url, data=payload)
    print("RESPOSTA INTERACTIVE:", response.text)
    return response.text
