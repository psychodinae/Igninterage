import os
from selenium import webdriver
from selenium.common import exceptions as ex
from selenium.webdriver.firefox.options import Options


class FirefoxCookiesLoader:

    def __init__(self, driver_location, url, profile_position=0):
        """Recupera os cookies do navegador Firefox no windows.

        Args:
            driver_location (str): Caminho completo do webdriver.
            url (str): URL do site.
            profile_position (int): posicao do arquivo de perfil na pasta Profiles, troque o valor de acordo
                com o perfil.
        """
        self.url = url
        moz_profile = os.path.join(os.getenv('APPDATA'), r'Mozilla\Firefox\Profiles')
        ff_cookie_path = os.path.join(moz_profile, os.listdir(moz_profile)[profile_position])
        options = Options()
        options.add_argument("--headless")
        profile = webdriver.FirefoxProfile(ff_cookie_path)
        self.driver = webdriver.Firefox(firefox_profile=profile, options=options,
                                        executable_path=driver_location)

    def get_cookies(self, *args):
        """Retorna uma lista de dicionarios {nome: valor} como os cookies do navegador Firefox selecionados.

        Args:
           *args (str):  Sequencia variavel de parametros com os nomes
            dos cookies a serem retornados.

        Returns:
           list: lista de {name: value} cookies, em caso de erro: None
        """
        _count = 0
        _ck_list = []
        try:
            self.driver.get(self.url)
            se_cookies = self.driver.get_cookies()
            self.driver.close()
            self.driver.quit()
            for _arg in args:
                for _se_cookie in se_cookies:
                    if all([_arg in _se_cookie['name'], _se_cookie['value']]):
                        _ck_list.append({_se_cookie['name']: _se_cookie['value']})
                        _count += 1
            if _count is not len(args):
                raise Exception('get_cookies: Error at Parsing Cookies.')
        except ex.WebDriverException as e:
            if 'executable needs to be in PATH' in str(e):
                print('geckodriver not found')
            if 'Reached error page' in str(e):
                print('get_cookies: Connection error.')
        return _ck_list

