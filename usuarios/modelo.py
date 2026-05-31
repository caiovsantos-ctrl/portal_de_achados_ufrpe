class Usuario:
    def __init__(self, nome, email, senha, Whatsapp):
        self._nome = nome
        self._email = email
        self._senha = senha
        self._Whatsapp = Whatsapp

    @property 
    def nome(self):
        return self._nome
    @nome.setter
    def nome(self, valor):
        self._nome = valor

    @property 
    def email(self):
        return self._email
    @email.setter
    def email(self, valor):
        self._email = valor

    @property 
    def senha(self):
        return self._senha
    @senha.setter
    def senha(self, valor):
        self._senha = valor

    @property 
    def Whatsapp(self):
        return self._Whatsapp
    @Whatsapp.setter
    def Whatsapp(self, valor):
        self._Whatsapp = valor

    def transformar_dicionario(self):
        return {
            "nome": self._nome,
            "email": self._email,
            "senha": self._senha,
            "Whatsapp": self._Whatsapp
        }