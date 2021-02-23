import igninterage.exceptions as ex
from igninterage.interage import Interage
from igninterage.utils import get_cookies_do_navegador, save_cookie_file, load_cookie_file


class Igninterage(Interage):
    def __init__(self, url, cache_file_name=None, navegador='firefox', caminho_database=None, profile_position=None,
                 header=Interage.headers):
        """
        Clase principal do modulo. Responsavel por recuperar os cookies do navegador e
        utiliza-los para realizar as requisições no fórum IGN Boards opcionalmente é possivel
        salva-los em arquivo de cache.

        É possível:
            * Postar em um tpc.
            * Editar o post.
            * reagir a um post.
            * Enviar mensagem privada.

        Args:
            url (str): url do forum.

            cache_file_name (str): Opcional, caminho/nome do arquivo de cache com o cookie de login.

             caso não definido o arquivo não será criado (ign_login usara diretamente o DB do navegador,
              xenforo2_login fara o login diretamente).

            navegador (str): navegador usado para recuperar os cookies: firefox ou chrome, default=firefox.

            caminho_database (str): (OPCIONAL) caminho completo do local do database. O programa automaticamente
             ja acessa o local de instalacao padrao.

            profile_position (int): posicao do arquivo de perfil na pasta Profiles, troque o valor de acordo
                       com o perfil (firefox somente).

            header : Opcional, para inserir um User-agent customizado.
        """
        super(Igninterage, self).__init__(url, header)
        self._cache_file_name = cache_file_name
        self.navegador = navegador
        self.caminho_database = caminho_database
        self.profile = profile_position

    def ign_login(self):
        try:
            if self._cache_file_name:
                try:
                    print('[!] Logando usando o cache de sessão.')
                    cookies = load_cookie_file(self._cache_file_name)
                    self.set_cookie(cookies)
                except FileNotFoundError:
                    print(
                        f'[!] O arquivo cache da sessão não existe criando um novo usando o navegador {self.navegador}')
                    cookie = get_cookies_do_navegador(self.navegador, self.caminho_database, self.profile)
                    self.set_cookie(cookie)
                    save_cookie_file(cookie, self._cache_file_name)
            else:
                print(f'[!] Logando usando o DB do {self.navegador}.')
                cookie = get_cookies_do_navegador(self.navegador, self.caminho_database, self.profile)
                self.set_cookie(cookie)
        except (ConnectionError, ex.NotXenforoPage, ex.LoginError):
            raise

    def xenforo2_login(self, username, password):
        try:
            if self._cache_file_name:
                try:
                    print('[!] Logando usando o cache de sessão.')
                    cookies = load_cookie_file(self._cache_file_name)
                    self.set_cookie(cookies)
                except FileNotFoundError:
                    print(
                        f'[!] O arquivo cache da sessão não existe criando um novo usando o navegador {self.navegador}')
                    cookie = self._xenforo2_login(username, password)
                    self.set_cookie(cookie)
                    save_cookie_file(cookie, self._cache_file_name)
            else:
                print('[!] Logando sem cache (não recomendado).')
                cookie = self._xenforo2_login(username, password)
                self.set_cookie(cookie)

        except (ConnectionError, ex.NotXenforoPage, ex.LoginError):
            raise
