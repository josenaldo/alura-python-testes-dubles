def consultar_livros(autor):
    dados = preparar_dados_para_requisicao(autor)
    url = "https://buscador"
    obter_url(url, dados)
    return ""


def preparar_dados_para_requisicao(autor):
    pass

def obter_url(url, dados):
    pass