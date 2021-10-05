class Armazem:
    def __init__(self):
        self._produtos = {}

    def add(self, produto, quantidade):
        self._produtos[produto]=quantidade

    def verifica_inventario(self, produto):
        return self._produtos[produto]

    def retira_produto(self, produto, quantidade):
        quantidade_registrada = self.verifica_inventario(produto)

        if quantidade_registrada >= quantidade:
            self._produtos[produto] = quantidade_registrada - quantidade
        else:
            raise ValueError(f"O produto '{produto}' não tem quantidade suficiente no estoque.")

class Pedido:
    def __init__(self, produto, quantidade):
        self._produto = produto
        self._quantidade = quantidade
        self._esta_preenchido = False

    def preencher(self, armazem):
        try:
            armazem.retira_produto(self._produto, self._quantidade)
            self._esta_preenchido = True
        except ValueError as e:
            self._esta_preenchido = False

    @property
    def esta_preenchido(self):
        return self._esta_preenchido