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

    print("RESPOSTA ULTRAMSG:", response.text)

    return response.text
