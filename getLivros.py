import os
import requests
import json


def fazer_requisicao_e_salvar_json():
    url = "https://www.abibliadigital.com.br/api/books"
    pasta = "livros"
    arquivo = "livros.json"

    if not os.path.exists(pasta):
        os.makedirs(pasta)

    try:
        resposta = requests.get(url)
        if resposta.status_code == 200:
            dados_json = resposta.json()
            with open(os.path.join(pasta, arquivo), 'w') as arquivo_json:
                json.dump(dados_json, arquivo_json, indent=2)

            print(f"Resposta salva em {os.path.join(pasta, arquivo)}")
        else:
            print(
                f"Erro na requisição. Código de resposta: {resposta.status_code}")
    except requests.RequestException as e:
        print(f"Erro na requisição: {e}")


if __name__ == "__main__":
    fazer_requisicao_e_salvar_json()
