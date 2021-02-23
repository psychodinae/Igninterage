import base64
import json
import os
import pickle
import platform
import sqlite3

import secretstorage

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from igninterage.exceptions import CookiesNotFound, DatabaseNotBeRead

test = platform.uname()[0]


def get_cookies_from_firefox(cookie_path=None, profile_position=None):
    try:
        if test == "Linux":
            if profile_position is None:
                profile_position = 2
            moz_profile = os.path.join(os.getenv('HOME'), r'.mozilla/firefox')
        elif test == "Windows":
            if profile_position is None:
                profile_position = 0
            moz_profile = os.path.join(os.getenv('APPDATA'), r'Mozilla/Firefox/Profiles')
        else:
            raise OSError('Sistema Operacional nao suportado')
        if cookie_path is None:
            cookie_path = os.path.join(moz_profile, os.listdir(moz_profile)[profile_position], 'cookies.sqlite')
        con = sqlite3.connect(cookie_path)
        try:
            ff_cookie = con.execute(
                "SELECT name, value FROM moz_cookies WHERE name='xf_user' order by lastAccessed desc limit 1").fetchone()
            con.close()
            return dict([ff_cookie])
        except sqlite3.OperationalError:
            raise DatabaseNotBeRead('Database esta bloqueado/aberto, feche seu navegador.')
    except TypeError:
        raise CookiesNotFound('Cookies do navegador Firefox nao encontrados')


def clean(x):
    return x[:-x[-1]].decode()


def get_cookies_from_chrome(cookie_path=None):
    if test == "Linux":
        """credits https://stackoverflow.com/a/44808566"""
        bus = secretstorage.dbus_init()
        collection = secretstorage.get_default_collection(bus)
        my_pass = [item.get_secret() for item in collection.get_all_items() if
                   item.get_label() == 'Chrome Safe Storage']
        if not my_pass:
            raise ValueError('Cookies do Chrome nao encontrado, Chrome nao instalado ou versao incompativel.')
        if cookie_path is None:
            cookie_path = os.path.join(os.getenv('HOME'), r'.config/google-chrome/Default/Cookies')
        con = sqlite3.connect(cookie_path)
        try:
            encrypted_value = con.execute(
                "SELECT encrypted_value FROM cookies WHERE name='xf_user'order by creation_utc desc limit 1").fetchone()
            con.close()
        except sqlite3.OperationalError:
            raise DatabaseNotBeRead('Database esta bloqueado/aberto, feche seu navegador.')
        try:
            encrypted_value = encrypted_value[0]
        except TypeError:
            raise CookiesNotFound('Cookies do navegador Chrome nao encontrados, tente atualizar a pagina.')

        encrypted_value = encrypted_value[3:]
        salt = b'saltysalt'
        iv = b' ' * 16

        kdf = PBKDF2HMAC(algorithm=hashes.SHA1(), length=16, salt=salt, iterations=1, )
        key = kdf.derive(my_pass[0])

        cipher2 = Cipher(algorithms.AES(key), modes.CBC(iv))
        decryptor = cipher2.decryptor()
        decrypted = decryptor.update(encrypted_value)
        return {'xf_user': clean(decrypted)}

    elif test == "Windows":
        import win32crypt
        local_state_path = os.path.join(os.getenv('LOCALAPPDATA'), r'Google/Chrome/User Data/Local State')
        file = open(local_state_path, "r", encoding="utf-8")
        local_state = json.load(file)["os_crypt"]["encrypted_key"]
        file.close()
        ckey = base64.b64decode(local_state)[5:]
        key = win32crypt.CryptUnprotectData(ckey, None, None, None, 0)[1]
        if not key:
            raise ValueError('Cookies do Chrome nao encontrado, Chrome nao instalado ou versao incompativel.')
        if cookie_path is None:
            cookie_path = os.path.join(os.getenv('LOCALAPPDATA'), r'Google/Chrome/User Data/Default/Cookies')
        con = sqlite3.connect(cookie_path)
        encrypted_value = con.execute(
            "SELECT encrypted_value FROM cookies WHERE name='xf_user' order by creation_utc desc limit 1").fetchone()
        con.close()
        try:
            encrypted_value = encrypted_value[0]
        except TypeError:
            raise CookiesNotFound('Cookies do navegador Chrome nao encontrados, tente atualizar a pagina.')

        iv = encrypted_value[3:15]
        encrypted_value = encrypted_value[15:]
        try:
            cipher2 = Cipher(algorithms.AES(key), modes.GCM(iv))
            decryptor = cipher2.decryptor()
            decrypted = decryptor.update(encrypted_value)
            return {'xf_user': decrypted[:-16].decode()}
        except Exception:
            raise

    raise OSError('Sistema Operacional nao suportado')


def get_cookies_do_navegador(navegador='firefox', caminho_db=None, profile=None):
    """Recupera dinamicamnente o xf_user cookie dos navegadores  para realizar login no forum ignboards.
               Args:
                   navegador (str): navegador usado para recuperar os cookies: firefox ou chrome, default=firefox.
                   caminho_db (str): (OPCIONAL) caminho completo do local do database.
                   profile(int): posicao do arquivo de perfil na pasta Profiles, troque o valor de acordo
                       com o perfil.
               Returns:
                   (dict): o cookie como um dicionario

       """
    if navegador == 'firefox':
        return get_cookies_from_firefox(caminho_db, profile)
    elif navegador == 'chrome':
        return get_cookies_from_chrome(caminho_db)
    else:
        raise NotImplemented('Navegador nao implementado.')


def save_cookie_file(content, f_name):
    pickle.dump(content, open(f_name, 'wb'))


def load_cookie_file(f_name):
    return pickle.load(open(f_name, 'rb'))
