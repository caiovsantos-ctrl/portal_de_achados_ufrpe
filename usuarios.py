import json
from time import sleep
from interface import Acessorio
from validacoes import Validador
from data_base import DataBase


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
    

class GerenciadorUsuario:
    def __init__(self):
        pass

    def cadastrar_user(self):
        """ Realiza todo o processo para cadastrar o usuário """
        print('\033[0;32mCadastro selecionado\033[m\n')
        Acessorio.limpar_tela()
        print('=' * 50)
        print('=====' + ' NOVO CADASTRO - UFRPE '.center(40) + '=====')
        print('=' * 50)
        print('\n     Crie sua conta para acessar o portal')
        print('  (Digite 0 a qualquer momento para cancelar)\n')
        print('=' * 50)
        sleep(2)
        Acessorio.limpar_tela()
        nome_cadastro = Validador.validar_nome()
        if nome_cadastro is None:
            return
        print('\033[0;32mNome cadastrado!\033[m')
        while True:
            email_cadastro = Validador.validar_email()
            if email_cadastro is None:
                return
            if Validador.email_ja_existe(email_cadastro):
                print('\033[0;31mEsse email já está cadastrado no sistema\033[m')
                if Acessorio.tentar_novamente(mensagem = 'Deseja tentar com outro email?[S/N]') == 'N':
                    Acessorio.limpar_tela()
                    return
                Acessorio.limpar_tela()
                continue
            print('\033[0;32mEmail cadastrado!\033[m')
            senha_cadastro = Validador.validar_senha()
            if senha_cadastro is None:
                return
            print('\033[0;32mSenha cadastrada!\033[m')
            zap_cadastro = Validador.validar_zap()
            if zap_cadastro is None:
                return
            print('\033[0;32mN° do Whatsapp cadastrado!\033[m')
            novo_user = Usuario(
                nome=nome_cadastro,
                email=email_cadastro,
                senha=senha_cadastro,
                Whatsapp=zap_cadastro
            ) 
            DataBase.salvar_user(novo_user)
            print(f'\nBem-vindo ao Portal de Achados UFRPE, {nome_cadastro}!')
            sleep(1)
            Acessorio.limpar_tela()
            break

    def login_user(self):
        """
        -> Realiza todo o processo de login do usuário
        :return: (dict) Retorna os dados do usuário em específico
        """
        print('\033[0;32mLogin selecionado\033[m')
        while True:
            Acessorio.limpar_tela()
            print('-' * 50)
            print('=====' + ' ACESSO AO PORTAL UFRPE '.center(40) + '=====')
            print('=' * 50)
            print('\n     Por favor, preencha suas credenciais:')
            print('  (Digite 0 a qualquer momento para cancelar)\n')
            print('-' * 50)
            sleep(2)
            Acessorio.limpar_tela()
            email_login = Validador.validar_email()
            if email_login is None:
                return
            senha_login = Validador.validar_senha()
            if senha_login is None:
                return
            try:
                with open('usuarios.json', 'r') as arquivo:
                    usuarios_cadastrados = json.load(arquivo)
            except (FileNotFoundError, json.JSONDecodeError):
                print('\033[0;31mBanco de dados de usuários não encontrado ou vazio. Tente novamente mais tarde\033[m')
                return
            except Exception as e:
                print('\033[0;31mOcorreu um erro ao acessar o banco de dados de usuários:\033[m')
            user_logado = False
            for user in usuarios_cadastrados:
                if user["email"] == email_login and user["senha"] == senha_login:
                    print(f'\033[0;32mLogin bem-sucedido!\033[m \nÉ um prazer te ver novamente, {user["nome"]}!')
                    user_logado = True
                    return Usuario(
                        nome=user["nome"],
                        email=user["email"],
                        senha=user["senha"],
                        Whatsapp=user["Whatsapp"]
                    )
            if not user_logado:
                print('\033[0;31mEmail ou senha incorretos\033[m')
                continuar_login = Acessorio.tentar_novamente(mensagem = 'Deseja tentar fazer login novamente?[S/N] ')
                if continuar_login == 'S':
                    continue
                elif continuar_login == 'N':
                    print('Retornando...')
                    Acessorio.limpar_tela()
                    return None
            
    def menu_atualizar_dados(self, user_logado):
        """
        -> Mostra o menu de atualizar dados e direciona o usuário de acordo com a opção
        :param user_logado: (dict) Dicionário que guarda os dados do usuário
        """
        print('\033[0;32mAtualizar dados pessoais selecionado\033[m')
        while True:
            Acessorio.limpar_tela()
            Acessorio.exibir_menu_padrao('ATUALIZAR DADOS PESSOAIS', [
                    '[1] → Atualizar Nome',
                    '[2] → Atualizar Email',
                    '[3] → Atualizar Senha',
                    '[4] → Atualizar Whatsapp',
                    '[0] → Voltar'
                    ])
            resposta_menu = Validador.verificar_resposta_menu(0, 4)
            if resposta_menu == '0':
                Acessorio.verificar_escape(resposta_menu)
                Acessorio.limpar_tela()
                return
            elif resposta_menu == '1':
                self.processar_atualizacao(user_logado, "nome", Validador.validar_nome)
            elif resposta_menu == '2':
                self.processar_atualizacao(user_logado, "email", Validador.validar_email)
            elif resposta_menu == '3':
                self.processar_atualizacao(user_logado, "senha", Validador.validar_senha)
            elif resposta_menu == '4':
                self.processar_atualizacao(user_logado, "Whatsapp", Validador.validar_zap)

    def atualizar_dados_pessoais(self, user_logado, campo_para_mudar, novo_valor):
        """
        -> Verifica se o dado atualizado é igual ao antigo, caso não efetua a mudança
        :param user_logado: (dict) Dicionário que guarda os dados do usuário
        :param campo_para_mudar: (str) O dado que o usuário deseja atualizar
        :param novo_valor: (str) O dado atualizado pelo usuário
        :return: (bool) Retorna True se ocorreu a atualização e False se deu errado 
        """
        if novo_valor == getattr(user_logado, campo_para_mudar):
            print(f'{campo_para_mudar} informado(a) é igual ao(à) atual')
            return False
        try:
            with open('usuarios.json', 'r', encoding='utf-8') as arquivo:
                lista_usuarios = json.load(arquivo)
            sucesso = False
            for usuario in lista_usuarios:
                if usuario["email"] == user_logado.email:
                    usuario[campo_para_mudar] = novo_valor
                    sucesso = True
                    break
            if sucesso:
                with open('usuarios.json', 'w', encoding='utf-8') as arquivo:
                    json.dump(lista_usuarios, arquivo, indent=4, ensure_ascii=False)
                print(f'\033[0;32m{campo_para_mudar} atualizado com sucesso!\033[m')
                return True
        except Exception as e:
            print('\033[0;31mErro ao atualizar dados pessoais:\033[m')
            return False
        
    
    def processar_atualizacao(self, user_logado, campo, funcao_validacao):
        """
        -> Muda o dado no JSON
        :param user_logado: (dict) Dicionário que guarda os dados do usuário
        :param campo: (str) Mensagem que mostra o campo que o usuário escolheu
        :param funcao_validar: (function) Função que será substituída pelo campo desejado
        """
        print(f'\033[0;32mAtualizar {campo} selecionado\033[m')
        identidade = Validador.confirmar_identidade(user_logado.transformar_dicionario())
        if identidade == True:
            while True:
                novo_valor = funcao_validacao()
                conseguiu = self.atualizar_dados_pessoais(user_logado, campo, novo_valor)
                if conseguiu: 
                    setattr(user_logado, campo, novo_valor)
                    break
                else:
                    if Acessorio.tentar_novamente(mensagem = f'Deseja tentar atualizar o {campo} novamente?[S/N] ') == 'N':
                        break
        else:
            print('Identidade não confirmada')
            Acessorio.tentar_novamente(mensagem = 'Deseja tentar confirmar sua identidade novamente?[S/N] ')

    def deletar_conta(self, user_logado):
        """
        -> Realiza todo o processo de deletar conta
        :param user_logado: (dict) Dicionário que guarda os dados do usuário
        :return: (bool) Retorna True se ocorreu a conta foi deletada e False se deu errado 
        """
        print('\033[0;32mDeletar conta selecionado\033[m')
        Acessorio.limpar_tela()
        print('ATENÇÃO: Essa ação é irreversível!')
        certeza = Acessorio.tentar_novamente(mensagem = 'Deseja realmente deletar sua conta?[S/N] ')
        if certeza == 'S':
            identidade = Validador.confirmar_identidade(user_logado)
            if identidade == True:
                try:
                    with open('usuarios.json', 'r', encoding='utf-8') as arquivo:
                        lista_usuarios = json.load(arquivo)
                    nova_lista = []
                    for user in lista_usuarios:
                        if user["email"] != user_logado.email:
                            nova_lista.append(user)
                    if len(nova_lista) < len(lista_usuarios):
                        with open('usuarios.json', 'w', encoding='utf-8') as arquivo:
                            json.dump(nova_lista, arquivo, indent=4, ensure_ascii=False)
                        print('\n\033[0;32mConta deletada com sucesso. Sentiremos sua falta!\033[m')
                        sleep(1)
                        Acessorio.limpar_tela()
                        return True
                    return False
                except Exception as erro:
                    print('\033[0;31mOcorreu um erro. Tente novamente mais tarde\033[m')
                    return False


    
        