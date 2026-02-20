def interpretar_entrada(texto: str) -> str:
    """
    Converte qualquer entrada do usuário (texto / número / botão no futuro)
    em comandos internos padronizados.

    Retorna:
      - comandos tipo: MENU_SERVICOS, MENU_PLANOS_FAMILIARES, MENU_ATENDENTE
      - ou TEXTO:xxxx (quando for texto livre, ex: nome, cidade, etc)
    """
    if not texto:
        return ""

    t = texto.strip().lower()

    # Compatibilidade com o modelo antigo por números
    if t == "1":
        return "MENU_SERVICOS"
    if t == "2":
        return "MENU_PLANOS_FAMILIARES"
    if t == "3":
        return "MENU_PLANOS_EMPRESARIAIS"
    if t == "4":
        return "MENU_FLORICULTURA"
    if t == "9":
        return "MENU_ATENDENTE"

    # Atalhos por texto (pra você testar no terminal/postman sem botão ainda)
    if "serv" in t:
        return "MENU_SERVICOS"
    if "fami" in t:
        return "MENU_PLANOS_FAMILIARES"
    if "empre" in t:
        return "MENU_PLANOS_EMPRESARIAIS"
    if "flor" in t:
        return "MENU_FLORICULTURA"
    if "atend" in t or "humano" in t:
        return "MENU_ATENDENTE"

    # Texto livre (ex: nome, endereço, etc)
    return f"TEXTO:{texto.strip()}"