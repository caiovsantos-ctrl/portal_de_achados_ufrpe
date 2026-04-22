import json, interface, validacoes, data_base
from time import sleep


def cadastrar_user():
    print('Cadastro selecionado\n')
    interface.limpar_tela()
    print("=" * 50)
    print("=====" + " NOVO CADASTRO - UFRPE ".center(40) + "=====")
    print("=" * 50)
    print("\n  Crie sua conta para acessar o portal.")
    print("  (Digite 0 a qualquer momento para cancelar)\n")
    print("=" * 50)
    sleep(2)
    interface.limpar_tela()
    nome_cadastro = validacoes.validar_nome()
    if nome_cadastro is None:
        return
    print('Nome cadastrado!')
    while True:
        email_cadastro = validacoes.validar_email()
        if email_cadastro is None:
            return
        if validacoes.email_ja_existe(email_cadastro):
            print('Esse email já está cadastrado no sistema')
            if interface.tentar_novamente(mensagem = 'Deseja tentar com outro email?[S/N]') == 'N':
                interface.limpar_tela()
                return
            interface.limpar_tela()
            continue
        print('Email cadastrado!')
        senha_cadastro = validacoes.validar_senha()
        if senha_cadastro is None:
            return
        print('Senha cadastrada!')
        zap_cadastro = validacoes.validar_zap()
        if zap_cadastro is None:
            return
        print('N° do Whatsapp cadastrado!')
        novo_user = {
            "nome": nome_cadastro,
            "email": email_cadastro,
            "senha": senha_cadastro,
            "Whatsapp": zap_cadastro
        } 
        data_base.salvar_user(novo_user)
        print(f'\nBem-vindo ao Portal de Achados UFRPE, {nome_cadastro}!')
        sleep(1)
        interface.limpar_tela()
        break


def login_user():
    print('Login selecionado')
    while True:
        interface.limpar_tela()
        print("=" * 50)
        print("=====" + " ACESSO AO PORTAL UFRPE ".center(40) + "=====")
        print("=" * 50)
        print("\n  Por favor, preencha suas credenciais:")
        print("  (Digite 0 a qualquer momento para cancelar)\n")
        print("=" * 50)
        sleep(2)
        interface.limpar_tela()
        email_login = validacoes.validar_email()
        if email_login is None:
            return
        senha_login = validacoes.validar_senha()
        if senha_login is None:
            return
        try:
            with open('usuarios.json', 'r') as arquivo:
                usuarios_cadastrados = json.load(arquivo)
        except (FileNotFoundError, json.JSONDecodeError):
            print('Banco de dados de usuários não encontrado ou vazio. Tente novamente mais tarde')
            return
        except Exception as e:
            print('Ocorreu um erro ao acessar o banco de dados de usuários:')
        user_logado = False
        for user in usuarios_cadastrados:
            if user["email"] == email_login and user["senha"] == senha_login:
                print(f'Login bem-sucedido! \nÉ um prazer te ver novamente, {user["nome"]}!')
                user_logado = True
                return user
        if not user_logado:
            print('Email ou senha incorretos')
            continuar_login = interface.tentar_novamente(mensagem = 'Deseja tentar fazer login novamente?[S/N] ')
            if continuar_login == 'S':
                continue
            elif continuar_login == 'N':
                print('Retornando...')
                interface.limpar_tela()
                return None
            

def menu_atualizar_dados(user_logado):
    print('Atualizar dados pessoais selecionado')
    while True:
        interface.limpar_tela()
        interface.exibir_menu_padrao('ATUALIZAR DADOS PESSOAIS', [
                '[1] → Atualizar Nome',
                '[2] → Atualizar Email',
                '[3] → Atualizar Senha',
                '[4] → Atualizar Whatsapp',
                '[0] → Voltar'
                ])
        resposta_menu = validacoes.verificar_resposta_menu(0, 4)
        if resposta_menu == '0':
            interface.verificar_escape(resposta_menu)
            interface.limpar_tela()
            return
        elif resposta_menu == '1':
           processar_atualizacao(user_logado, "nome", validacoes.validar_nome)
        elif resposta_menu == '2':
            processar_atualizacao(user_logado, "email", validacoes.validar_email)
        elif resposta_menu == '3':
            processar_atualizacao(user_logado, "senha", validacoes.validar_senha)
        elif resposta_menu == '4':
            processar_atualizacao(user_logado, "Whatsapp", validacoes.validar_zap)
            

def atualizar_dados_pessoais(user_logado, campo_para_mudar, novo_valor):
    if novo_valor == user_logado[campo_para_mudar]:
        print(f'{campo_para_mudar} informado(a) é igual ao(à) atual')
        return False
    try:
        with open('usuarios.json', 'r', encoding='utf-8') as arquivo:
            lista_usuarios = json.load(arquivo)
        sucesso = False
        for usuario in lista_usuarios:
            if usuario["email"] == user_logado["email"]:
                usuario[campo_para_mudar] = novo_valor
                sucesso = True
                break
        if sucesso:
            with open('usuarios.json', 'w', encoding='utf-8') as arquivo:
                json.dump(lista_usuarios, arquivo, indent=4, ensure_ascii=False)
            print(f'{campo_para_mudar} atualizado com sucesso!')
            return True
    except Exception as e:
        print('Erro ao atualizar dados pessoais:')
        return False
            

def processar_atualizacao(user_logado, campo, funcao_validacao):
    print(f'Atualizar {campo} selecionado')
    identidade = validacoes.confirmar_identidade(user_logado)
    if identidade == True:
        while True:
            novo_valor = funcao_validacao()
            conseguiu = atualizar_dados_pessoais(user_logado, campo, novo_valor)
            if conseguiu: 
                user_logado[campo] = novo_valor
                break
            else:
                if interface.tentar_novamente(mensagem = 'Deseja tentar atualizar o {campo} novamente?[S/N] ') == 'N':
                    break
    else:
        print('Identidade não confirmada')
        interface.tentar_novamente(mensagem = 'Deseja tentar confirmar sua identidade novamente?[S/N] ')


def deletar_conta(user_logado):
    print('Deletar conta selecionado')
    interface.limpar_tela()
    print('ATENÇÃO: Essa ação é irreversível!')
    certeza = interface.tentar_novamente(mensagem = 'Deseja realmente deletar sua conta?[S/N] ')
    if certeza == 'S':
        identidade = validacoes.confirmar_identidade(user_logado)
        if identidade == True:
            try:
                with open('usuarios.json', 'r', encoding='utf-8') as arquivo:
                    lista_usuarios = json.load(arquivo)
                nova_lista = []
                for user in lista_usuarios:
                    if user["email"] != user_logado["email"]:
                        nova_lista.append(user)
                if len(nova_lista) < len(lista_usuarios):
                    with open('usuarios.json', 'w', encoding='utf-8') as arquivo:
                        json.dump(nova_lista, arquivo, indent=4, ensure_ascii=False)
                    print('\nConta deletada com sucesso. Sentiremos sua falta!')
                    return True
                return False
            except Exception as erro:
                print('Ocorreu um erro. Tente novamente mais tarde')
                return False