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
    print("RESPOSTA CHAT:", response.text)
    return response.text


def enviar_botoes(numero, titulo, texto, botoes):
    url = f"https://api.ultramsg.com/{ULTRAMSG_INSTANCE}/messages/buttons"

    payload = {
        "token": ULTRAMSG_TOKEN,
        "to": numero,
        "title": titulo,
        "body": texto,
        "buttons": str(botoes)  # 🔥 IMPORTANTE
    }

    response = requests.post(url, data=payload)
    print("RESPOSTA BOTAO:", response.text)
    return response.text
