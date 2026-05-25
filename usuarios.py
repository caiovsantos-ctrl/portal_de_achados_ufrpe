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
    

class CadastroUsuario:
    @staticmethod
    def executar_cadastro():
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

    
class LoginUsuario:
    @staticmethod
    def executar_login():
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
            usuarios_cadastrados = LoginUsuario._carregar_usuarios()
            for user in usuarios_cadastrados:
                if user["email"] == email_login and user["senha"] == senha_login:
                    print(f'\033[0;32mLogin bem-sucedido!\033[m \nÉ um prazer te ver novamente, {user["nome"]}!')
                    return Usuario(
                        nome=user["nome"],
                        email=user["email"],
                        senha=user["senha"],
                        Whatsapp=user["Whatsapp"]
                    )
            print('\033[0;31mEmail ou senha incorretos\033[m')
            continuar_login = Acessorio.tentar_novamente(mensagem = 'Deseja tentar fazer login novamente?[S/N] ')
            if continuar_login == 'S':
                continue
            elif continuar_login == 'N':
                Acessorio.limpar_tela()
                return None
                
    @staticmethod
    def _carregar_usuarios():
        try:
            with open('usuarios.json', 'r', encoding='utf-8') as arquivo:
                usuarios_cadastrados = json.load(arquivo)
                return usuarios_cadastrados
        except (FileNotFoundError, json.JSONDecodeError):
            print('\033[0;31mBanco de dados de usuários não encontrado ou vazio. Tente novamente mais tarde\033[m')
            return []
        except Exception as e:
            print('\033[0;31mOcorreu um erro ao acessar o banco de dados de usuários:\033[m')
            return []
            

class AtualizarDadosUsuario:
    @staticmethod
    def menu_atualizar_dados(user_logado):
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
                AtualizarDadosUsuario._processar_mudanca(user_logado, "nome", Validador.validar_nome)
            elif resposta_menu == '2':
                AtualizarDadosUsuario._processar_mudanca(user_logado, "email", Validador.validar_email)
            elif resposta_menu == '3':
                AtualizarDadosUsuario._processar_mudanca(user_logado, "senha", Validador.validar_senha)
            elif resposta_menu == '4':
                AtualizarDadosUsuario._processar_mudanca(user_logado, "Whatsapp", Validador.validar_zap)

    @staticmethod
    def _processar_mudanca(user_logado, campo, funcao_validacao):
        """
        -> Verifica se o dado atualizado é igual ao antigo, caso não efetua a mudança
        :param user_logado: (dict) Dicionário que guarda os dados do usuário
        :param campo_para_mudar: (str) O dado que o usuário deseja atualizar
        :param novo_valor: (str) O dado atualizado pelo usuário
        :return: (bool) Retorna True se ocorreu a atualização e False se deu errado 
        """
        print(f'\033[0;32mAtualizar {campo} selecionado\033[m')
        while True:
            if Validador.confirmar_identidade(user_logado.transformar_dicionario()):
                    novo_valor = funcao_validacao()
                    if novo_valor == getattr(user_logado, campo):
                        print(f'{campo} informado(a) é igual ao(à) atual')
                        tentar_atualizar = Acessorio.tentar_novamente(mensagem=f'Deseja tentar atualizar o {campo} novamente?[S/N] ')
                        if tentar_atualizar == 'N':
                            break
                        else:
                            continue
                    if AtualizarDadosUsuario._salvar_no_json(user_logado.email, campo, novo_valor):
                        setattr(user_logado, campo, novo_valor)
                        break
                    else:
                        tentar = Acessorio.tentar_novamente(mensagem=f'Deseja tentar atualizar o {campo} novamente?[S/N] ')
                        if tentar == 'N':
                            break
                        else:
                            continue
            else:
                print('Identidade não confirmada')
                continuar = Acessorio.tentar_novamente(mensagem='Deseja tentar confirmar sua identidade novamente?[S/N] ')
                if continuar == 'S':
                    continue
                elif continuar == 'N':
                    Acessorio.limpar_tela()
                    return None
        
    @staticmethod
    def _salvar_no_json(email_atual, campo, novo_valor):
        """
        -> Muda o dado no JSON
        :param user_logado: (dict) Dicionário que guarda os dados do usuário
        :param campo: (str) Mensagem que mostra o campo que o usuário escolheu
        :param funcao_validar: (function) Função que será substituída pelo campo desejado
        """
        try:
            with open('usuarios.json', 'r', encoding='utf-8') as arquivo:
                lista_usuarios = json.load(arquivo)
            sucesso = False
            for usuario in lista_usuarios:
                if usuario["email"] == email_atual:
                    usuario[campo] = novo_valor
                    sucesso = True
                    break
            if sucesso:
                with open('usuarios.json', 'w', encoding='utf-8') as arquivo:
                    json.dump(lista_usuarios, arquivo, indent=4, ensure_ascii=False)
                print(f'\033[0;32m{campo} atualizado com sucesso!\033[m')
                return True
            return False
        except Exception:
            print('\033[0;31mErro ao atualizar dados pessoais no arquivo.\033[m')
            return False

    
class DeletarContaUsuario:
    @staticmethod
    def executar_delecao(user_logado):
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


    
        