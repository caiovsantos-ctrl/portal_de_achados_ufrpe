import textwrap, time, sys
from time import sleep
from interface import Acessorio
from validacoes import Validador
from data_base import DataBase
from central_notificacoes import AssistenteIA
from .modelo import Usuario


class CadastroUsuario:
    """ Gerencia todo o processo para cadastrar o usuário """
    @staticmethod
    def executar_cadastro():
        """Coleta os dados e salva o novo usuário no arquivo json"""
        print('\033[0;32mCadastro selecionado\033[m\n')
        Acessorio.limpar_tela()
        print('=' * 50)
        print('=====' + ' NOVO CADASTRO - UFRPE '.center(40) + '=====')
        print('=' * 50)
        print('\n     Crie sua conta para acessar o portal')
        print('  (Digite 0 a qualquer momento para cancelar)\n')
        print('=' * 50)
        sleep(2)
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
            from central_notificacoes.notificacoes import Notificacoes
            Notificacoes.criar_notificacao(
                dono_id=nome_cadastro,  
                tipo="SISTEMA",       
                mensagem=f"Olá, {nome_cadastro}! Seja muito bem-vindo(a) ao Portal de Achados e Perdidos da UFRPE. Explore o sistema para cadastrar itens ou verificar correspondências!"
            )
            sleep(1)
            Acessorio.limpar_tela()
            break

    
class LoginUsuario:
    """ Gerencia todo o processo de login do usuário """
    @staticmethod
    def executar_login():
        """
        -> Realiza o login e verifica se o usuário já está cadastrado
        :return: (obj/None) Retorna os dados do usuário em específico 
                 ou None se o login falhou ou o usuário cancelou a operação
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
            email_login = Validador.validar_email()
            if email_login is None:
                return
            senha_login = Validador.validar_senha()
            if senha_login is None:
                return
            usuarios_cadastrados = DataBase.carregar_usuarios()
            for user in usuarios_cadastrados:
                if user["email"] == email_login and user["senha"] == senha_login:
                    print(f'\n\033[0;32mLogin bem-sucedido!\033[m \nÉ um prazer te ver novamente, {user["nome"]}!')
                    Acessorio.limpar_tela()
                    aviso = AssistenteIA.boas_vindas(user['nome'])
                    print('=' * 95)
                    print('Notificações:'.center(95))
                    print('=' * 95)
                    texto_formatado = textwrap.fill(
                        aviso,
                        width=85,
                        initial_indent='     ',
                        subsequent_indent='     '
                    )
                    print('\n')
                    for letra in texto_formatado:
                        sys.stdout.write(letra)
                        sys.stdout.flush()
                        time.sleep(0.01)
                    print('\n\n')
                    print('═' * 95)
                    print('\n')
                    continuar = Validador.aguardar_retorno('Digite 0 para continuar: ')
                    if continuar:
                        pass
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