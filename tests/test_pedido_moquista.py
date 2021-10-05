from unittest.mock import patch, MagicMock, call

from _pytest.fixtures import fixture

from colecao.armazem import Pedido


class TestPedidoMoquista:

    @fixture
    def catuaba(self):
        return "Catuaba"

    @patch("colecao.armazem.Armazem")
    def teste_preencher_pedido_remove_produto_do_estoque_quando_tem_produtos_suficientes_no_estoque(self, armazem_mock, catuaba):
        # Setup - dados
        pedido = Pedido(catuaba, 50)

        # Setup - expectativas
        armazem_mock.tem_inventario.return_value = True
        armazem_mock.retira_produto.return_value = True

        # Exercício
        pedido.preencher(armazem_mock)

        # Verifica se os métodos tem_inventario e retira_produto foram chamados apenas uma vez
        armazem_mock.tem_inventario.assert_called_once_with(catuaba, 50)
        armazem_mock.retira_produto.assert_called_once_with(catuaba, 50)

        # verifica a ordem de chamada de tem_inventario e retira_produto
        expected_calls = [call.tem_inventario(catuaba, 50), call.retira_produto(catuaba, 50)]
        assert armazem_mock.mock_calls == expected_calls

        #verifica se o produto está preenchido
        assert pedido.esta_preenchido == True

    @patch("colecao.armazem.Armazem")
    def teste_preencher_pedido_nao_remove_produto_do_estoque_quando_nao_tem_produtos_suficientes_no_estoque(self, armazem_mock, catuaba):
        # Setup - dados
        pedido = Pedido(catuaba, 51)

        # Setup - expectativas
        armazem_mock.retira_produto.side_effect = ValueError(f"O produto '{catuaba}' não tem quantidade suficiente no estoque.")

        # Exercício
        pedido.preencher(armazem_mock)

        # Verificação
        armazem_mock.retira_produto.assert_called_once_with(catuaba, 51)
        assert pedido.esta_preenchido == False

