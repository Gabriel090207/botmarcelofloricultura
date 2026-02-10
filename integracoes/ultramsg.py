import requests


# CONFIGURAR DEPOIS
ULTRAMSG_INSTANCE = "instance161393"
ULTRAMSG_TOKEN = "8t1mtgzcr1koqulf"


def enviar_mensagem(numero, mensagem):
    url = f"https://api.ultramsg.com/{ULTRAMSG_INSTANCE}/messages/chat"

    payload = {
        "token": ULTRAMSG_TOKEN,
        "to": numero,
        "body": mensagem,
    }

    try:
        response = requests.post(url, data=payload)
        return response.json()

    except Exception as e:
        print("Erro ao enviar mensagem:", e)
        return None
