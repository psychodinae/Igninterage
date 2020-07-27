# -*- coding: utf-8 -*-
import requests
import lxml.html as parser
from igninterage.exceptions import LoginError, NotXenforoPage


def decorator_check_login(f):
    def wrapper(ins, *args, **kwargs):
        if ins.check_login():
            print('[!] Logado ok!')
            f(ins, *args, **kwargs)
            return True
    return wrapper


class Interage(object):
    """Clase que realiza as requisições web"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/70.0.3538.77 Safari/537.36'
    }
    interact_session = requests.Session()
    data = {}

    def __init__(self, url: str, header=None, ):
        if header is None:
            header = self.headers
        self.url = url
        self.interact_session.headers.update(header)

    def set_cookie(self, cookie: dict):
        self.interact_session.cookies.update(cookie)
        self.check_login()

    def set_xf_token(self, token: str):
        self.data = {'_xfToken': token}

    def check_login(self):
        self.data.clear()
        try:
            req = self.interact_session.get(self.url)
            tree = parser.fromstring(req.text)
            try:
                is_logged = tree.get_element_by_id('XF').get('data-logged-in')
            except (IndexError, KeyError):
                raise NotXenforoPage(f'Erro: "{self.url}" nao e um forum Xenforo, voce digitou a url corretamente no '
                                     f'construtor da classe?')
            if is_logged == 'true':
                csrf_token = tree.find('.//input[@name="_xfToken"]').value
                self.data = {'_xfToken': csrf_token}
                return True
            elif is_logged == 'false':
                raise LoginError('Erro ao logar, cookie inexistente, expirado ou Usuario/senha invalidos.')
            else:
                raise LoginError('Erro desconhecido ao checar se esta logado.')

        except requests.exceptions.ConnectionError:
            raise ConnectionError('Erro Interage,check_login(): requests: erro de conexão.')

    def _xenforo2_login(self, username: str, password: str) -> dict:
        """Realiza Login padrao em foruns Xenforo 2.x.

                Args:
                    username (str): nome de usuario ou e-mail.
                    password (str): senha do usuario.

                Returns:
                    dict:

                Raises:
                    LoginError: Erro ao logar, cookie inexistente, expirado ou Usuario/senha invalidos.
                    NotXenforoPage: Nao e um forum Xenforo
                    ConnectionError: Erro de conexao
        """
        _data_login = {
            "login": username,
            "password": password,
            'remember': '1'
        }
        self.interact_session.post(f'{self.url}index.php?login/login/', data=_data_login)
        self.check_login()
        return self.interact_session.cookies.get_dict()

    @decorator_check_login
    def novo_topico(self, title: str, text: str, board_uri, prefix_id='0') -> None:
        """Cria um tópico.

        Args:
            title (str): Titulo da Mensagem.
            text (str): Mensagem a ser enviada.
            board_uri (str): endpoint O forum especifo a ser criado o tpc ex: vale-tudo.80331/.
            prefix_id (str): prefixo para o topico: 17=resolved, 63=spoiler, default: sem prefixo..

        Returns:
                None

            Raises:
                LoginError: Erro ao logar, cookie inexistente, expirado ou Usuario/senha invalidos.
                NotXenforoPage: Nao e um forum Xenforo
                ConnectionError: Erro de conexao
        """
        self.data.update({
            "title": title,
            "message": text,
            "prefix_id": prefix_id
        })
        self.interact_session.post(f'{self.url}forums/{board_uri}/post-thread', data=self.data)
        print(f'[!] Criou tópico na sessão {board_uri} com sucesso!')

    @decorator_check_login
    def editar_topico(self, title: str, text: str, post_id: str, prefix_id='0') -> None:
        """Edita um tópico.

        Args:
            title (str): Titulo da Mensagem.
            text (str): Mensagem a ser enviada.
            post_id (str): id do primeiro post.
            prefix_id (str): prefixo para o topico: 17=resolved, 63=spoiler, default: sem prefixo..

        Returns:
                None

            Raises:
                LoginError: Erro ao logar, cookie inexistente, expirado ou Usuario/senha invalidos.
                NotXenforoPage: Nao e um forum Xenforo
                ConnectionError: Erro de conexao
        """

        self.data.update({
            "title": title,
            "message": text,
            "prefix_id": prefix_id
        })
        self.interact_session.post(f'{self.url}posts/{post_id}/edit', data=self.data)
        print(f'[!] Tópico editado com sucesso!')

    @decorator_check_login
    def comentar(self, text: str, thread: str) -> None:
        """Insere um comentário no fórum.
             Para enviar uma imagem, por exemplo use as tags BBcode [IMG]imagem.jpg[/IMG],
             video do youtube [MEDIA=youtube]<ID>[/MEDIA]
         Args:
            text (str): Mensagem a ser enviada.
            thread (str): ID do tópico.

        Returns:
                None

            Raises:
                LoginError: Erro ao logar, cookie inexistente, expirado ou Usuario/senha invalidos.
                NotXenforoPage: Nao e um forum Xenforo
                ConnectionError: Erro de conexao
        """
        self.data["message"] = text
        self.interact_session.post(f'{self.url}threads/{thread}/add-reply', data=self.data)
        print(f'[!] postou no tópico {thread} com sucesso!')

    @decorator_check_login
    def editar_comentario(self, text: str, post_id: str) -> None:
        """Edita um comentário no fórum.

        Args:
            text (str): Mensagem a ser enviada.
            post_id (str): id do post.

        Returns:
                None

        Raises:
            LoginError: Erro ao logar, cookie inexistente, expirado ou Usuario/senha invalidos.
            NotXenforoPage: Nao e um forum Xenforo
            ConnectionError: Erro de conexao
        """
        self.data["message"] = text
        self.interact_session.post(f'{self.url}posts/{post_id}/edit', data=self.data)
        print(f'[!] Post {post_id} editado com sucesso!')

    @decorator_check_login
    def react(self, react_id: str, post_id: str) -> None:

        """Insere um react em um post.

                    react IDs:

                    1 = like

                    2 = Love

                    3 = Haha

                    4 = Wow

                    5 = Sad

                    6 = Angry

                    7 = Thinking

                    Args:
                        react_id (str): React ID numero de 1 a 7.
                        post_id (str): id do post.

                    Returns:
                        None

                    Raises:
                        LoginError: Erro ao logar, cookie inexistente, expirado ou Usuario/senha invalidos.
                        NotXenforoPage: Nao e um forum Xenforo
                        ConnectionError: Erro de conexao
        """
        self.data["reaction_id"] = react_id
        self.interact_session.post(f'{self.url}posts/{post_id}/react', data=self.data)
        print(f'[!] reagiu ao post {post_id}!')

    @decorator_check_login
    def msg_privada(self, title: str, text: str, *user_nick) -> None:
        """Envia mensagem privada a um ou mais usuarios.

            Args:
                title (str): Titulo da Mensagem.
                text (str): Mensagem a ser enviada.
                *user_nick(str): lista variavel de nick do(s) destinatario(s).


            Returns:
                None

            Raises:
                LoginError: Erro ao logar, cookie inexistente, expirado ou Usuario/senha invalidos.
                NotXenforoPage: Nao e um forum Xenforo
                ConnectionError: Erro de conexao
        """
        users = ', '.join(map(str, user_nick))
        self.data.update({
            "title": title,
            "message": text,
            "recipients": users
        })
        self.interact_session.post(f'{self.url}conversations/add', data=self.data)
        print(f'[!] Mensagem privada enviada para: {users} com sucesso!')
