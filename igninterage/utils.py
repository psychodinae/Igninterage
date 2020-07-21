import os
import pickle
import sqlite3


def get_ign_firefox_cookie_from_sqlite(profile_position=0):
    """Recupera dinamicamnente o xf_user cookie do navegador Firefox no windows para realizar login no forum ignboards.

            Args:
                profile_position (int): posicao do arquivo de perfil na pasta Profiles, troque o valor de acordo
                    com o perfil.
            Returns:
                (dict): o cookie como um dicionario
    """
    moz_profile = os.path.join(os.getenv('APPDATA'), r'Mozilla\Firefox\Profiles')
    ff_cookie_path = os.path.join(moz_profile, os.listdir(moz_profile)[profile_position], 'cookies.sqlite')
    con = sqlite3.connect(ff_cookie_path)
    return dict([con.execute("SELECT name, value FROM moz_cookies WHERE name='xf_user'").fetchone()])


def save_cookie_file(content, f_name):
    pickle.dump(content, open(f_name, 'wb'))


def load_cookie_file(f_name):
    return pickle.load(open(f_name, 'rb'))
