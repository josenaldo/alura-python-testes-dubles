from unittest.mock import patch
from colecao.livros import (
    consultar_livros
)

def test_consultar_livros_retorna_resultados_formato_string():
    resultado = consultar_livros("Agatha Christie")
    assert type(resultado) == str

def test_consultar_livros_chama_preparar_dados_para_requisisao_uma_vez_e_com_os_mesmos_parametros_de_consultar_livros():
    with patch("colecao.livros.preparar_dados_para_requisicao") as duble:
        consultar_livros("Agatha Christie")
        duble.assert_called_once_with("Agatha Christie")

def test_consultar_livros_chama_obter_url_usando_como_parametro_o_retorno_de_preparar_dados_para_requisicao():
    with patch("colecao.livros.preparar_dados_para_requisicao") as duble_preparar:
        dados = {"author":"Agatha Christie"}
        duble_preparar.return_value = dados
        with patch("colecao.livros.obter_url") as duble:
            consultar_livros("Agatha Christie")
            duble.assert_called_once_with("https://buscador", dados)