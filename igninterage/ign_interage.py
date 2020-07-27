# -*- coding: utf-8 -*-
import igninterage.exceptions as ex
from igninterage import utils
from igninterage.interage import Interage


class Igninterage(Interage):
    def __init__(self, cache_file_name, url, header=Interage.headers):
        """Clase principal do modulo. Responsavel por recuperar os cookies do navegador
        Firefox, salva-los em arquivo de cache e utiliza-los para realizar as requisições,
        no fórum IGN Boards.

        É possível:
            * Postar em um tpc.
            * Editar o post.
            * reagir a um post.
            * Enviar mensagem privada.

        Args:
            cache_file_name (str): caminho/nome para salvar o arquivo de cache com o cookie de login.
            url (str): url do forum.
            header : Opcional, para inserir um User-agent customizado.
        """
        super(Igninterage, self).__init__(url, header)
        self._cache_file_name = cache_file_name

    def _load_cache_cookies(self):
        try:
            cookies = utils.load_cookie_file(self._cache_file_name)
            self.set_cookie(cookies)
            return True
        except FileNotFoundError:
            pass

    def _load_from_firefox(self):
        cookie = utils.get_ign_firefox_cookie_from_sqlite()
        try:
            self.set_cookie(cookie)
        except (ConnectionError, ex.NotXenforoPage, ex.LoginError):
            raise
        utils.save_cookie_file(cookie, self._cache_file_name)
        print('[!] O arquivo cache da sessão está nao existe ou esta expirado, criando um novo usando o navegador '
              'firefox...')
        return True

    def xenforo2_login(self, username, password):
        if not self._load_cache_cookies():
            ck = self._xenforo2_login(username, password)
            utils.save_cookie_file(ck, self._cache_file_name)
        print(f'[!] Cookies carregados do arquivo "{self._cache_file_name}"')

    def ign_login(self):
        if not self._load_cache_cookies():
            self._load_from_firefox()
        print(f'[!] Cookies carregados do arquivo "{self._cache_file_name}"')
