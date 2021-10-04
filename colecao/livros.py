import logging
import os
from urllib.error import HTTPError
from urllib.request import urlopen


def consultar_livros(autor):
    dados = preparar_dados_para_requisicao(autor)
    url = obter_url("https://buscador", dados)
    ret = executar_requisicao(url)

    return ret


def preparar_dados_para_requisicao(autor):
    pass


def obter_url(url, dados):
    pass


def executar_requisicao(url):
    resultado = ""
    try:
        with urlopen(url, timeout=10) as resposta:
            resultado = resposta.read().decode("utf-8")
    except HTTPError as e:
        logging.exception(f"Ao acessar '{url}': {e}")
    else:
        return resultado

def escrever_em_arquivo(arquivo, conteudo):
    diretorio = os.path.dirname(arquivo)

    try:
        os.makedirs(diretorio)
    except OSError:
        logging.exception(f"Não foi possível criar diretório '{diretorio}'")

    try:
        with open(arquivo, "w") as fp:
            fp.write(conteudo)
    except OSError as e:
        logging.exception(f"Não foi possível criar arquivo '{arquivo}'")