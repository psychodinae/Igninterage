URL = 'https://www.ignboards.com/'


class Interage:
    """Clase que realiza as requisições web"""
    def __init__(self):
        self.interact_session = None
        self.header = {}
        self.data = {}

    def set_cookie(self, cookies: list):
        for cookie in cookies:
            self.interact_session.cookies.update(cookie)

    def comentar(self, text: str, thread: str):
        """Insere um comentário no fórum.::

             Para enviar uma imagem, por exemplo use as tags BBcode [IMG]imagem.jpg[/IMG],

             video do youtube [MEDIA=youtube]<ID>[/MEDIA]

         Args:
            text (str): Mensagem a ser enviada.

            thread (str): ID do tópico.
         """
        self.data["message"] = text
        self.interact_session.post(f'{URL}threads/{thread}/add-reply', data=self.data, headers=self.header)
        print(f'[!] postou no tópico {thread} com sucesso!')

    def editar_comentario(self, text: str, post_id: str):
        """Edita um comentário no fórum.
           obs: Os posts podem ser editados por um tempo limitado.

        Args:
            text (str): Mensagem a ser enviada.
            post_id (str): id do post.
        """
        self.data["message"] = text
        self.interact_session.post(f'{URL}posts/{post_id}/edit', data=self.data, headers=self.header)
        print(f'[!] Post {post_id} editado com sucesso!')

    def react(self, react_id: str, post_id: str):
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
         """
        self.data["reaction_id"] = react_id
        self.interact_session.post(f'{URL}posts/{post_id}/react', data=self.data, headers=self.header)
        print(f'[!] reagiu ao post {post_id}!')
