import requests
import utils
from firefox_cookies_loader import FirefoxCookiesLoader
from interage import Interage


class IGNInteract(Interage):
    _site = 'https://www.ignboards.com/'
    _re_fx1 = 'data-csrf="'
    _re_fx2 = '"'
    _re_log1 = 'data-logged-in="'
    _re_log2 = '"'
    _cookies = None
    _xf_token = None
    _header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/70.0.3538.77 Safari/537.36',
    }

    def __init__(self, geckodriver_location, cache_file_name):
        """Clase principal do modulo. Responsavel por recuperar os cookies do navegador
        Firefox, salva-los em arquivo de cache e utiliza-los para realizar as requisições,
        usando o modulo requests, no fórum IGN Boards.

        É possível:
            * Postar em um tpc.
            * Editar o post.
            * reagir a um post.
        TODO:
            * Criar um tópico.
            * Enviar mensagem privada.

        Args:
            geckodriver_location (str): Caminho do Web driver.
            cache_file_name (str): Caminho do arquivo onde será salvo os cookies de sessão e token.

        """
        super().__init__()
        self._cache_file_name = cache_file_name
        self._geckodriver_location = geckodriver_location
        self.interact_session = requests.Session()
        self._load_cache_cookies()

    def _load_cache_cookies(self):
        try:
            cookies, xf_token = utils.load_cookie_file(self._cache_file_name)
            self.set_cookie(cookies)
            self.data['_xfToken'] = xf_token
            if self.check_login():
                print('cache carregado com sucesso!')
                return True
            else:
                print('[!] Cache expirado, rode o metodo ing_login() primeiro.')
                return False
        except FileNotFoundError:
            pass
        print('[!] Arquivo de cache nao encontrado, rode o metodo ing_login() primeiro.')

    def _load_from_firefox(self):
        print('[!] O arquivo cache da sessão está expirado, criando um novo usando o navegador firefox...')
        ff_ck_loader = FirefoxCookiesLoader(self._geckodriver_location, self._site)
        cookies = ff_ck_loader.get_cookies('xf_session', 'xf_csrf')
        self.set_cookie(cookies)
        xf_token = self.check_login()
        if xf_token:
            self.data['_xfToken'] = xf_token
            utils.save_cookie_file([cookies, xf_token], self._cache_file_name)
            print('cache criado com sucesso!')
            return True
        print('cookies expirados, tente relogar no firefox.')

    def check_login(self):
        try:
            req = self.interact_session.get(self._site).text
            if 'true' in utils.re_search(self._re_log1, self._re_log2, req):
                return utils.re_search(self._re_fx1, self._re_fx2, req)
        except requests.exceptions.ConnectionError:
            print('Erro IGNInteract.ign_login,check_login(): requests: erro de conexão.')
            exit(1)

    def ign_login(self):
        if not self._load_cache_cookies():
            if self._load_from_firefox():
                print('[!] O arquivo cache da sessão está expirado, criando um novo usando o navegador firefox...')
            else:
                raise Exception('Login Error.')
        print(f'[!] Cookies carregados do arquivo {self._cache_file_name}')

if __name__ == '__main__':
    driver_location = r'C:\Users\User\user\geckodriver.exe'
    cookie_file = 'cache.session'
    ign = IGNInteract(driver_location, cookie_file)
    if not ign.check_login():
        ign.ign_login()
    ign.react('1', '123456789')
    ign.comment('isso foi postado com a "API" rsrsrsrs', '123456789')
    ign.edit_comment('[EDITt] e agora foi editado usando a "API"', '123456789')
