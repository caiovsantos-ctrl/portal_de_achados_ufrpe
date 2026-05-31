class Item:
    def __init__(self, tipo_registro, categoria, local, descricao, contato, resolvido, autor, id_item=None):
        self._id_item = id_item
        self._tipo_registro = tipo_registro
        self._categoria = categoria
        self._local = local
        self._descricao = descricao
        self._contato = contato
        self._resolvido = resolvido
        self._autor = autor

    @property
    def tipo_registro(self):
        return self._tipo_registro

    @property
    def categoria(self):
        return self._categoria

    @property
    def local(self):
        return self._local

    @property
    def descricao(self):
        return self._descricao

    @property
    def contato(self):
        return self._contato

    @property
    def resolvido(self):
        return self._resolvido
    @resolvido.setter
    def resolvido(self, valor):
        self._resolvido = valor

    @property
    def autor(self): 
        return self._autor

    @property
    def id_item(self):
        return self._id_item
    @id_item.setter
    def id_item(self, valor):
        self._id_item = valor

    def transformar_dicionario(self):
        dados = {
            "tipo_registro": self._tipo_registro,
            "categoria": self._categoria,
            "local": self._local,
            "descricao": self._descricao,
            "resolvido": self._resolvido,
            "contato": self._contato,
            "autor": self._autor
        }
        if self._id_item is not None:
            dados["id_item"] = self.id_item
        return dados 