import requests
import json
import os
import re


def get_livros_from_json():
    livros = []
    json_path = os.path.join('livros', 'livros.json')

    with open(json_path, 'r') as file:
        json_data = json.load(file)

    abbrev_list = [item["abbrev"] for item in json_data]

    for elem in abbrev_list:
        livros.append(elem['pt'])

    return livros


def salvar_capitulo(livro, cap, response):
    pasta_capitulos = "capitulos"
    pasta_livro = f'{livro}'

    arquivo = f"{livro}_cap{cap}.json"
    capitulo_path = os.path.join(
        pasta_capitulos, pasta_livro, arquivo)
    with open(capitulo_path, 'w') as file:
        json.dump(response.json(), file, indent=2)
        print(f'escreveu capitulo {cap} em {capitulo_path}')


def criar_pasta_capitulo():
    if not os.path.exists('capitulos'):
        os.makedirs('capitulos')
        print('criou pasta capitulos')


def criar_pasta_livro(livro):
    if not os.path.exists(os.path.join('capitulos', livro)):
        os.makedirs(os.path.join(
            'capitulos', livro))
        print(f'criou pasta {livro}')


def verificar_ultimo_capitulo(livro):
    caminho_pasta = os.path.join('capitulos', livro)
    padrao = re.compile(r'{}_cap(\d+)'.format(livro))
    maior_numero = 0
    nome_arquivo_maior_numero = None

    for nome_arquivo in os.listdir(caminho_pasta):
        correspondencia = padrao.match(nome_arquivo)
        if correspondencia:
            numero_capitulo = int(correspondencia.group(1))
            if numero_capitulo > maior_numero:
                maior_numero = numero_capitulo
                nome_arquivo_maior_numero = nome_arquivo

    return nome_arquivo_maior_numero, maior_numero


def maximo_de_capitulos_do_livro(livro, cap):
    global capitulos_completos
    capitulos_completos[f'{livro}'] = cap - 1
    with open('capitulos_completos.json', 'w') as file:
        json.dump(capitulos_completos, file, indent=2)


def capitulos_request(version):
    livros = get_livros_from_json()

    if (os.path.exists('capitulos') == False):
        criar_pasta_capitulo()

    for livro in livros:
        global capitulos_completos
        if livro in capitulos_completos.keys():
            print(f'livro {livro} já completo')
            continue

        if os.path.exists(os.path.join('capitulos', livro)):
            _, maior_numero = verificar_ultimo_capitulo(livro)
            if maior_numero:
                cap = maior_numero + 1
        else:
            cap = 1

        while True:
            try:
                print('na url', livro, cap)
                url = f"https://www.abibliadigital.com.br/api/verses/{version}/{livro}/{cap}"
                response = requests.get(url)
                print(response.status_code)
                if response.status_code == 404:
                    maximo_de_capitulos_do_livro(livro, cap)
                    break
                elif response.status_code == 200:
                    criar_pasta_livro(livro)
                    salvar_capitulo(livro, cap, response)
                    cap += 1
                else:
                    break
            except requests.RequestException as e:
                print(f"Erro na requisição: {e}")


if __name__ == "__main__":
    capitulos_completos = {}
    if not os.path.exists('capitulos_completos.json'):
        with open('capitulos_completos.json', 'w') as file:
            json.dump(capitulos_completos, file, indent=2)

    with open('capitulos_completos.json', 'r') as file:
        capitulos_completos = json.load(file)
    capitulos_request('nvi')
