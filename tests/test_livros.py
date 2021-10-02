from unittest.mock import patch
from unittest import skip
from colecao.livros import (
    consultar_livros,
    executar_requisicao
)


@skip("Vale quando consultar livros estiver completo")
def test_consultar_livros_retorna_resultados_formato_string():
    resultado = consultar_livros("Agatha Christie")
    assert type(resultado) == str


@skip("Resolver problema do executar")
def test_consultar_livros_chama_preparar_dados_para_requisisao_uma_vez_e_com_os_mesmos_parametros_de_consultar_livros():
    with patch("colecao.livros.preparar_dados_para_requisicao") as duble:
        consultar_livros("Agatha Christie")
        duble.assert_called_once_with("Agatha Christie")


@skip("Resolver problema do executar")
def test_consultar_livros_chama_obter_url_usando_como_parametro_o_retorno_de_preparar_dados_para_requisicao():
    with patch("colecao.livros.preparar_dados_para_requisicao") as duble_preparar:
        dados = {"author":"Agatha Christie"}
        duble_preparar.return_value = dados
        with patch("colecao.livros.obter_url") as duble:
            consultar_livros("Agatha Christie")
            duble.assert_called_once_with("https://buscador", dados)


@skip("Resolver problema do executar")
def test_consultar_livros_chama_executar_requisicao_usando_retorno_obter_url():
    with patch("colecao.livros.obter_url") as duble_obter_url:
        duble_obter_url.return_value = "https://buscador"
        with patch("colecao.livros.executar_requisicao") as duble_executar_requisicao:
            consultar_livros("Agatha Christie")
            duble_executar_requisicao.assert_called_once_with("https://buscador")


class StubHTTPResponse:

    def read(self):
        return b""

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

def duble_url_open(url, timeout):
    return StubHTTPResponse()

def test_executar_requisicao_retorna_tipo_string():
    with patch("colecao.livros.urlopen", duble_url_open):
        resultado = executar_requisicao("https://buscador?author=Jk+Rowlings")
        assert type(resultado) == str