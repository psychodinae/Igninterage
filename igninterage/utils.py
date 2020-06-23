import pickle
import re


def re_search(tag_ini, tag_fin, input_text):
    return re.search(f'{tag_ini}(.*){tag_fin}', input_text).group(1)


def save_cookie_file(content, f_name):
    pickle.dump(content, open(f_name, 'wb'))


def load_cookie_file(f_name):
    return pickle.load(open(f_name, 'rb'))
