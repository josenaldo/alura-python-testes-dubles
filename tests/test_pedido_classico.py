from _pytest.fixtures import fixture

from colecao.armazem import Armazem, Pedido


class TestePedidoClassico:

    """
    Parte da fase de setup do testes é implementada através dos fixtures
    """
    @fixture
    def catuaba(self):
        return "Catuaba"

    @fixture
    def corote(self):
        return "Corote"

    @fixture
    def armazem(self, catuaba, corote):
        armazem = Armazem()
        armazem.add(catuaba, 50);
        armazem.add(corote, 25);
        return armazem

    def teste_pedido_eh_preenchido_se_armazem_tem_suficiente(self, armazem, catuaba):
        # Fase de Setup
        pedido = Pedido(catuaba, 50)

        # Fase de Exercitar
        pedido.preencher(armazem)

        # Fase de asserções
        assert pedido.esta_preenchido
        assert 0 == armazem.tem_inventario(catuaba)

    def teste_pedido_nao_remove_nada_do_armazem_se_nao_tem_o_suficiente(self, armazem, catuaba):
        # Fase de Setup
        pedido = Pedido(catuaba, 51)

        # Fase de Exercitar
        pedido.preencher(armazem)

        # Fase de asserções
        assert not pedido.esta_preenchido
        assert 50 == armazem.tem_inventario(catuaba)
