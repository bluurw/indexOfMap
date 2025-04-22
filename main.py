import os
import sys
import requests
from bs4 import BeautifulSoup

def requisition(URL:str):
    r = requests.get(URL, timeout=25)
    if r.status_code != 200:
        return r, False
    else:
        return r, True

def get_content(purpose):
    contents = {
        'folders':[],
        'files':[],
    }
    soup = BeautifulSoup(purpose.text, "html.parser")
    table = soup.find("table")
    for td in table.find_all("td"):
        try:
            href = td.find('a')
            if 'Parent Directory' in href:
                continue
            else:
                href = href['href']
                #verify_ext = lambda href: any(href.endswith(ext) or href.endswith(ext.upper()) for ext in exts)
                if href[-1] != "/": # check the type
                    contents['files'].append(f'{purpose.url}{href}')
                else:
                    contents['folders'].append(f'{purpose.url}{href}')
        except Exception as err:
            continue
    return contents

def request_server(url):
    contents = {}
    queue = [url]  # Usando lista como fila

    while queue:
        current_url = queue.pop(0)  # Pega o primeiro da fila
        response = requisition(current_url)
        if response[1]:
            content = get_content(response[0])
        else:
            return 'Error'

        contents[current_url] = content['files']
        queue.extend(content['folders']) 

    return contents

def banner_blurred_black():
    os.system('clear')
    print('''\033[1;33m
░▀█▀░▒█▄░▒█░█▀▄░█▀▀░█░█░▒█▀▀▀█░█▀▀░▒█▀▄▀█░█▀▀▄░▄▀▀▄
░▒█░░▒█▒█▒█░█░█░█▀▀░▄▀▄░▒█░░▒█░█▀░░▒█▒█▒█░█▄▄█░█▄▄█
░▄█▄░▒█░░▀█░▀▀░░▀▀▀░▀░▀░▒█▄▄▄█░▀░░░▒█░░▒█░▀░░▀░█░░░
                \033[m t.me/mk_Directory
''')

def main():
    banner_blurred_black()
    target = sys.argv[1]
    request = request_server(target)
    if request_server == 'Error':
        print('Erro ao requisitar o alvo.')
    else:
        for k, list_ in request.items():
            print(f'[+]{k}')
            for v in list_:
                print(f'{" "*3} [-]{v}')
            print()

if __name__ == '__main__':
    main()


# Exemplo de uso
# python main.py 'https://entropy.soldierx.com/~kayin/archive/'
