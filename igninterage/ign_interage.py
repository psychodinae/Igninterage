# -*- coding: utf-8 -*-
import igninterage.exceptions as ex
from igninterage import utils
from igninterage.interage import Interage


class Igninterage(Interage):
    def __init__(self, url, cache_file_name=None, header=Interage.headers):
        """Clase principal do modulo. Responsavel por recuperar os cookies do navegador
        Firefox, salva-los em arquivo de cache e utiliza-los para realizar as requisições,
        no fórum IGN Boards.

        É possível:
            * Postar em um tpc.
            * Editar o post.
            * reagir a um post.
            * Enviar mensagem privada.

        Args:
            url (str): url do forum.
            cache_file_name (str): Opcional, caminho/nome do arquivo de cache com o cookie de login.
             caso não definido o arquivo não será criado (ign_login usara diretamente o DB do Firefox,
              xenforo2_login fara o login diretamente).
            header : Opcional, para inserir um User-agent customizado.
        """
        super(Igninterage, self).__init__(url, header)
        self._cache_file_name = cache_file_name

    def ign_login(self):
        try:
            if self._cache_file_name:
                try:
                    print('[!] Logando usando o cache de sessão.')
                    cookies = utils.load_cookie_file(self._cache_file_name)
                    self.set_cookie(cookies)
                except FileNotFoundError:
                    print('[!] O arquivo cache da sessão não existe criando um novo usando o navegador Firefox...')
                    cookie = utils.get_ign_firefox_cookie_from_sqlite()
                    self.set_cookie(cookie)
                    utils.save_cookie_file(cookie, self._cache_file_name)
            else:
                print('[!] Logando usando o DB do firefox.')
                cookie = utils.get_ign_firefox_cookie_from_sqlite()
                self.set_cookie(cookie)
        except (ConnectionError, ex.NotXenforoPage, ex.LoginError):
            raise

    def xenforo2_login(self, username, password):
        try:
            if self._cache_file_name:
                try:
                    print('[!] Logando usando o cache de sessão.')
                    cookies = utils.load_cookie_file(self._cache_file_name)
                    self.set_cookie(cookies)
                except FileNotFoundError:
                    print('[!] O arquivo cache da sessão não existe criando um novo usando o navegador Firefox...')
                    cookie = self._xenforo2_login(username, password)
                    self.set_cookie(cookie)
                    utils.save_cookie_file(cookie, self._cache_file_name)
            else:
                print('[!] Logando sem cache (não recomendado).')
                cookie = self._xenforo2_login(username, password)
                self.set_cookie(cookie)

        except (ConnectionError, ex.NotXenforoPage, ex.LoginError):
            raise
   
