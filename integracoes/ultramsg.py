import requests
import os


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
    return response.text


def enviar_botoes(numero, titulo, texto, botoes):
    """
    botoes = [
        {"id": "1", "title": "Serviço funerário"},
        {"id": "9", "title": "Falar com atendente"}
    ]
    """

    url = f"https://api.ultramsg.com/{ULTRAMSG_INSTANCE}/messages/buttons"

    payload = {
        "token": ULTRAMSG_TOKEN,
        "to": numero,
        "title": titulo,
        "body": texto,
        "buttons": botoes
    }

    response = requests.post(url, json=payload)
    return response.text
