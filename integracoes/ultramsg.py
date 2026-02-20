import requests
import os


ULTRAMSG_INSTANCE = os.environ.get("ULTRAMSG_INSTANCE")
ULTRAMSG_TOKEN = os.environ.get("ULTRAMSG_TOKEN")

def enviar_mensagem(numero, mensagem):

    print("\n===== MENSAGEM SIMULADA =====")
    print("Para:", numero)
    print("Mensagem:")
    print(mensagem)
    print("=============================\n")

    return "modo_teste"