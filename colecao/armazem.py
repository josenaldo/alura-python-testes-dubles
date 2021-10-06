class Armazem:
    def __init__(self):
        self._produtos = {}

    def add(self, produto, quantidade):
        self._produtos[produto]=quantidade

    def tem_inventario(self, produto, quantidade):
        return self._produtos[produto] >= quantidade

    def quantidade_no_inventario(self, produto):
        return self._produtos.get(produto, 0)

    def retira_produto(self, produto, quantidade):

        tem_inventario = self.tem_inventario(produto, quantidade)
        if tem_inventario:
            self._produtos[produto] = self._produtos[produto] - quantidade
        else:
            raise ValueError(f"O produto '{produto}' não tem quantidade suficiente no estoque.")

class Pedido:
    def __init__(self, produto, quantidade, servico_de_email = None):
        self._produto = produto
        self._quantidade = quantidade
        self._esta_preenchido = False
        self._servico_de_email = servico_de_email
        self._email_enviado = False

    def __repr__(self):
        return f"Pedido(produto='{self._produto}', quantidade={self._quantidade})"

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

        if(not self._esta_preenchido and not self._email_enviado and self.servico_de_email):
            self.servico_de_email.enviar(f"Pedido não enviado: {self}")
            self._email_enviado = True

    @property
    def esta_preenchido(self):
        return self._esta_preenchido

    @property
    def servico_de_email(self):
        return self._servico_de_email

    @servico_de_email.setter
    def servico_de_email(self, value):
        self._servico_de_email = value


class ServicoDeEmail:
    def enviar(self, message):
        pass