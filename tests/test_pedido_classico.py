from _pytest.fixtures import fixture

from colecao.armazem import Armazem, Pedido


class ServicoDeEmailStub:
    """
    A classe ServicoDeEmailStub funciona como um stub para um serviço de email, que seria usado pela classe Pedido para
    enviar mensagens. Nessa implementação de um, Stub, ele apenas armazena as mensagens enviadas, para posterior
    verificação do número de mensagens.
    """
    def __init__(self):
        self._mensagens = []

    def enviar(self, message):
        print(message)
        self._mensagens.append(message)

    @property
    def numero_de_mensagens_enviadas(self):
        return len(self._mensagens)


class TestePedidoClassico:
    """
    Implementa testes da maneira classeioca, com verificação dos estados após a fase de exercício.
    """

    # Parte da fase de setup do testes é implementada através dos fixtures
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
        assert armazem.quantidade_no_inventario(catuaba) == 0

    def teste_pedido_nao_remove_nada_do_armazem_se_nao_tem_o_suficiente(self, armazem, catuaba):
        # Fase de Setup
        pedido = Pedido(catuaba, 51)

        # Fase de Exercitar
        pedido.preencher(armazem)

        # Fase de asserções
        assert not pedido.esta_preenchido
        assert armazem.quantidade_no_inventario(catuaba) == 50

    def teste_envio_do_pedido_envia_email_se_o_pedido_nao_for_enviado_pela_primeira_vez(self, armazem, catuaba):

        pedido = Pedido(catuaba, 51)
        servico_de_email = ServicoDeEmailStub()

        pedido.servico_de_email = servico_de_email
        pedido.preencher(armazem)

        assert servico_de_email.numero_de_mensagens_enviadas == 1