class Armazem:
    def __init__(self):
        self._produtos = {}

    def add(self, produto, quantidade):
        self._produtos[produto]=quantidade

    def tem_inventario(self, produto, quantidade):
        return bool(self._produtos[produto] >= quantidade)

    def retira_produto(self, produto, quantidade):

        tem_inventario = self.tem_inventario(produto, quantidade)
        if tem_inventario:
            self._produtos[produto] = self._produtos[produto] - quantidade
        else:
            raise ValueError(f"O produto '{produto}' não tem quantidade suficiente no estoque.")

class Pedido:
    def __init__(self, produto, quantidade):
        self._produto = produto
        self._quantidade = quantidade
        self._esta_preenchido = False

    def preencher(self, armazem):
        try:
            tem_inventario = armazem.tem_inventario(self._produto, self._quantidade)

            if(tem_inventario):
                armazem.retira_produto(self._produto, self._quantidade)
                self._esta_preenchido = True
            else:
                self._esta_preenchido = False
        except ValueError as e:
            self._esta_preenchido = False

    @property
    def esta_preenchido(self):
        return self._esta_preenchido