class LoginError(Exception):
    """Impossivel logar"""
    pass


class NotXenforoPage(Exception):
    """Elementos de uma pagina xenforo nao encontrados"""
    pass


class CookiesNotFound(Exception):
    """Cookies do navegador nao encontrados"""
    pass


class DatabaseNotBeRead(Exception):
    """Database nao existe ou esta bloqueado"""
    pass
