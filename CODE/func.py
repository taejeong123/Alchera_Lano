import urllib.request

def get_cdn():
    with urllib.request.urlopen('http://duuboo.net/cdn/cm.py') as response:
        code = response.read()
        return code

def get_keyword(txt_root):
    f = open(txt_root, 'r', encoding='utf-8')
    txt_list = f.read().split('\n')
    f.close()
    return txt_list

def err_msg(msg):
    print('[ERROR]: ' + msg)