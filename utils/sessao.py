# armazenamento simples em memória
# depois podemos mover para banco de dados

sessoes = {}


def obter_sessao(numero):
    """
    Retorna sessão do usuário.
    Se não existir, cria nova.
    """
    if numero not in sessoes:
        sessoes[numero] = {
            "etapa": "inicio",
            "dados": {}
        }

    return sessoes[numero]


def atualizar_etapa(numero, etapa):
    sessao = obter_sessao(numero)
    sessao["etapa"] = etapa


def salvar_dado(numero, chave, valor):
    sessao = obter_sessao(numero)
    sessao["dados"][chave] = valor


def limpar_sessao(numero):
    if numero in sessoes:
        del sessoes[numero]
