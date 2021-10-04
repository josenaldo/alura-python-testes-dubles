from unittest.mock import patch, mock_open, Mock
from unittest import skip
from urllib.error import HTTPError

import pytest

from colecao.livros import (
    consultar_livros,
    executar_requisicao
)

class StubHTTPResponse:

    # noinspection PyMethodMayBeStatic
    def read(self):
        return b""

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


# noinspection PyUnusedLocal
def stub_url_open(url, timeout):
    return StubHTTPResponse()


@patch("colecao.livros.urlopen", return_value=StubHTTPResponse())
def test_consultar_livros_retorna_resultados_formato_string(stub_urlopen):
    resultado = consultar_livros("Agatha Christie")
    assert type(resultado) == str


@patch("colecao.livros.urlopen", return_value=StubHTTPResponse())
def test_consultar_livros_chama_preparar_dados_para_requisisao_uma_vez_e_com_os_mesmos_parametros_de_consultar_livros(stub_urlopen):
    with patch("colecao.livros.preparar_dados_para_requisicao") as spy_preparar_dados:
        consultar_livros("Agatha Christie")
        spy_preparar_dados.assert_called_once_with("Agatha Christie")


@patch("colecao.livros.urlopen", return_value=StubHTTPResponse())
def test_consultar_livros_chama_obter_url_usando_como_parametro_o_retorno_de_preparar_dados_para_requisicao(stub_urlopen):
    with patch("colecao.livros.preparar_dados_para_requisicao") as stub_preparar:
        dados = {"author": "Agatha Christie"}
        stub_preparar.return_value = dados
        with patch("colecao.livros.obter_url") as stub:
            consultar_livros("Agatha Christie")
            stub.assert_called_once_with("https://buscador", dados)


@patch("colecao.livros.urlopen", return_value=StubHTTPResponse())
def test_consultar_livros_chama_executar_requisicao_usando_retorno_obter_url(stub_urlopen):
    with patch("colecao.livros.obter_url") as spy_obter_url:
        spy_obter_url.return_value = "https://buscador"
        with patch("colecao.livros.executar_requisicao") as spy_executar_requisicao:
            consultar_livros("Agatha Christie")
            spy_executar_requisicao.assert_called_once_with("https://buscador")


def test_executar_requisicao_retorna_tipo_string_test_com_stub_function():

    with patch("colecao.livros.urlopen", stub_url_open):
        resultado = executar_requisicao("https://buscador?author=Jk+Rowlings")
        assert type(resultado) == str


def test_executar_requisicao_retorna_tipo_string_test_com_stub_mock():
    with patch("colecao.livros.urlopen") as stub_do_url_open:
        stub_do_url_open.return_value = StubHTTPResponse()
        resultado = executar_requisicao("https://buscarlivros?author=Jk+Rowlings")
        assert type(resultado) == str


def test_executar_requisicao_retorna_tipo_string_test_com_stub_return_value():
    with patch("colecao.livros.urlopen", return_value=StubHTTPResponse()):
        resultado = executar_requisicao("https://buscarlivros?author=Jk+Rowlings")
        assert type(resultado) == str


@patch("colecao.livros.urlopen", return_value=StubHTTPResponse())
def test_executar_requisicao_retorna_tipo_string_test_com_decorador(stub_de_urlopen):
    resultado = executar_requisicao("https://buscarlivros?author=Jk+Rowlings")
    assert type(resultado) == str


@patch("colecao.livros.urlopen")
def test_executar_requisicao_retorna_tipo_string_test_com_decorador_uso_da_variavel(stub_de_urlopen):
    stub_de_urlopen.return_value = StubHTTPResponse()
    resultado = executar_requisicao("https://buscarlivros?author=Jk+Rowlings")
    assert type(resultado) == str


class Dummy:
    pass


def stub_url_open_que_levanta_excecao_http_error(url, timeout):
    fp = mock_open
    fp.close = Dummy()
    raise HTTPError(Dummy(), Dummy(), "mensagem de erro", Dummy(), fp)

"""
def test_executar_requisicao_loga_mensagem_de_erro_de_http_error(caplog):
    with patch("colecao.livros.urlopen", stub_url_open_que_levanta_excecao_http_error):
        resultado = executar_requisicao("http://")
        mensagem_de_erro = "mensagem de erro"
        assert len(caplog.records) == 1

        for registro in caplog.records:
            assert mensagem_de_erro in registro.message


def test_executar_requisicao_levanta_excecao_do_tipo_http_error():
    with patch("colecao.livros.urlopen", stub_url_open_que_levanta_excecao_http_error):
        with pytest.raises(HTTPError) as excecao:
            executar_requisicao("https://buscarlivros?author=Jk+Rowlings")

        assert "mensagem de erro" in str(excecao.value)


@patch("colecao.livros.urlopen")
def test_executar_requisicao_levanta_excecao_do_tipo_http_error_com_anotacao(stub_de_urlopen):
    fp = mock_open
    fp.close = Dummy()
    stub_de_urlopen.side_effect = HTTPError(Dummy(), Dummy(), "mensagem de erro", Dummy(), fp)
    with pytest.raises(HTTPError) as excecao:
        executar_requisicao("https://buscarlivros?author=Jk+Rowlings")
        assert "mensagem de erro" in str(excecao.value)

@patch("colecao.livros.urlopen")
def test_executar_requisicao_levanta_excecao_do_tipo_http_error_com_anotacaoe_mock(stub_de_urlopen):

    fp = mock_open
    fp.close = Mock()
    stub_de_urlopen.side_effect = HTTPError(Mock(), Mock(), "mensagem de erro", Mock(), fp)
    with pytest.raises(HTTPError) as excecao:
        executar_requisicao("https://buscarlivros?author=Jk+Rowlings")
        assert "mensagem de erro" in str(excecao.value)
"""
@patch("colecao.livros.urlopen")
def test_executar_requisicao_loga_mensagem_de_erro_de_http_error(stub_de_urlopen, caplog):
    fp = mock_open
    fp.close = Mock()
    stub_de_urlopen.side_effect = HTTPError(Mock(), Mock(), "mensagem de erro", Mock(), fp)

    executar_requisicao("http://")
    assert len(caplog.records) == 1
    for registro in caplog.records:
        assert "mensagem de erro" in registro.message





