import json, interface


def verificar_resposta_menu(inicio_range, fim_range):
    """
    -> Valida a resposta de todos menus do projeto
    :param inicio_range: (str) Primeira opção do menu
    :param fim_range: (str) Última opção do menu
    :return: (str) Retorna a opção do menu
    """
    while True:
        resposta_menu = input('=> ')
        resposta_menu = resposta_menu.strip()
        if resposta_menu == "":
            print('\033[0;31mA resposta não pode ser vazia. Tente novamente\033[m')
            continue
        elif resposta_menu.startswith('-'):
            print(f'\033[0;31mA resposta deve ser entre {inicio_range} e {fim_range}. Tente novamente\033[m')
            continue
        elif '.' in resposta_menu or ',' in resposta_menu:
            print('\033[0;31mA resposta deve ser um número inteiro. Tente novamente\033[m')
            continue
        elif not resposta_menu.isnumeric():
            print('\033[0;31mA resposta deve ser um número. Tente novamente\033[m')
            continue
        resposta_menu_int = int(resposta_menu)
        if resposta_menu_int < inicio_range or resposta_menu_int > fim_range:
            print(f'\033[0;31mA resposta deve ser entre {inicio_range} e {fim_range}. Tente novamente\033[m')
            continue
        return resposta_menu
    

def validar_nome():
    """
    -> Valida o nome digitado pelo usuário
    :return: (str/None) Retorna o nome digitado pelo usuario ou None caso digite '0'
    """
    while True:
        interface.limpar_tela()
        print('-' * 50)
        nome = input('\nNome: ')
        nome = nome.strip().capitalize()
        if interface.verificar_escape(nome):
            interface.limpar_tela()
            return None
        if nome == "":
            print('\033[0;31mO nome não pode ser vazio. Tente novamente\033[m')
            continue
        elif len(nome) < 3:
            print('\033[0;31mO nome deve conter pelo menos 3 caracteres. Tente novamente\033[m')
            continue
        elif len(nome) > 15:
            print('\033[0;31mO nome deve conter no máximo 15 caracteres. Tente novamente\033[m')
            continue
        elif nome.isnumeric():
            print('\033[0;31mO nome não pode conter números. Tente novamente\033[m')
            continue
        elif not nome.replace(' ', '').isalpha():
            print('\033[0;31mO nome não pode conter números ou caracteres especiais. Tente novamente\033[m')
            continue
        elif len(nome.split(' ')[0]) < 3:
            print('\033[0;31mO primeiro nome deve ter pelo menos 3 letras\033[m')
            continue
        else:
            print('\n', '-' * 50)
            return nome


def validar_email():
    """
    -> Valida o email digitado pelo usuário
    :return: (str/None) Retorna o email digitado pelo usuario ou None caso digite '0'
    """
    while True:
        interface.limpar_tela()
        print('-' * 50)
        email = input('\nEmail institucional: ')
        email = email.strip().lower()
        email_cortado = email.split('@')[0]
        if interface.verificar_escape(email):
            interface.limpar_tela()
            return None
        if email == "":
            print('\033[0;31mO email não pode ser vazio. Tente novamente\033[m')
            continue
        elif ' ' in email:
            print('\033[0;31mO email não pode conter espaços. Tente novamente\033[m')
            continue
        elif email_cortado.isnumeric():
            print('\033[0;31mO email não pode conter apenas números. Tente novamente\033[m')
            continue
        elif not email_cortado.replace('.', '').replace('_', '').isalnum():
            print('\033[0;31mO email deve conter letras e/ou números. Tente novamente\033[m')
            continue
        elif not email.endswith('@ufrpe.br'):
            print('\033[0;31mO email deve ser institucional (deve terminar com @ufrpe.br). Tente novamente\033[m')
            continue
        elif len(email) < 15:
            print('\033[0;31mO email deve conter pelo menos 15 caracteres. Tente novamente\033[m')
            continue
        elif len(email) > 30:
            print('\033[0;31mO email deve conter no máximo 30 caracteres. Tente novamente\033[m')
            continue
        else:
            print('\n', '-' * 50)
            return email


def validar_senha():
    """
    -> Valida a senha digitada pelo usuário
    :return: (str/None) Retorna a senha digitada pelo usuario ou None caso digite '0'
    """
    while True:
        interface.limpar_tela()
        print('-' * 50)
        senha = input('\nSenha (6-8 caracteres numéricos): ')
        senha = senha.strip()
        if interface.verificar_escape(senha):
            interface.limpar_tela()
            return None
        if senha == '':
            print('\033[0;31mA senha não pode ser vazia. Tente novamente\033[m')
            continue
        elif ' ' in senha:
            print('\033[0;31mA senha não pode conter espaços. Tente novamente\033[m')
            continue
        elif not senha.isnumeric():
            print('\033[0;31mA senha deve conter apenas números. Tente novamente\033[m')
            continue
        elif len(senha) < 6 or len(senha) > 8:
            print('\033[0;31mA senha deve conter entre 6 a 8 caracteres. Tente novamente\033[m')
            continue
        elif senha == '123456' or senha == '1234567' or senha == '12345678':
            print('\033[0;31mDigite uma senha mais segura\033[m')
            continue
        elif senha == senha[0] * len(senha):
            print('\033[0;31mA senha não deve conter todos os dígitos iguais. Tente novamente\033[m')
            continue
        else:
            print('\n', '-' * 50)
            return senha
        

def validar_zap():
    """
    -> Valida o n° do whatsapp digitado pelo usuário
    :return: (str/None) Retorna o n° do whatsapp digitado pelo usuario ou None caso digite '0'
    """
    while True:
        interface.limpar_tela()
        print('-' * 50)
        zap = input('\nWhatsapp (ex.: 81912345678): ')
        zap = zap.strip()
        if interface.verificar_escape(zap):
            interface.limpar_tela()
            return None
        if zap == '':
            print('\033[0;31mO n° do Whatsapp não pode ser vazio. Tente novamente\033[m')
            continue
        elif ' ' in zap:
            print('\033[0;31mO n° do Whatsapp não pode conter espaços. Tente novamente\033[m')
            continue
        elif not zap.isnumeric():
            print('\033[0;31mO n° do Whatsapp deve conter apenas números. Tente novamente\033[m')
            continue
        elif len(zap) != 11:
            print('\033[0;31mO n° do Whatsapp deve conter 11 caracteres. Tente novamente\033[m')
            continue
        elif zap[2] != '9':
            print('\033[0;31mApós o DDD deve conter o 9. Tente novamente\033[m')
            continue
        elif zap == zap[0] * len(zap):
            print('\033[0;31mO n° do Whatsapp não deve conter todos os dígitos iguais. Tente novamente\033[m')
            continue
        elif int(zap[:2]) > 98 or int(zap[:2]) < 11:
            print('\033[0;31mDDD inválido. Tente novamente\033[m')
            continue
        else:
            print('\n', '-' * 50)
            return zap



def email_ja_existe(email_digitado):
    """
    -> Verifica se o email digitado pelo usuário já está cadastrado
    :param email_digitado: (str) Email digitado pelo usuário 
    :return: (bool/None) Retorna True se já está cadastrado, False se não estiver ou None se deu erro 
    """
    try:
        with open('usuarios.json', 'r', encoding='utf-8') as arquivo:
            usuarios = json.load(arquivo)
        for user in usuarios:
            if user["email"] == email_digitado:
                return True
        return False
    except (FileNotFoundError, json.JSONDecodeError):
        return None
    

def confirmar_identidade(user_logado):
    """
    -> Verifica a identidade do usuário pela sua senha
    :param user_logado: (dict) Dicionário que guarda os dados do usuário 
    :return: (bool) Retorna True se a senha está correta ou False se não quer tentar novamente 
    """
    interface.limpar_tela()
    print('Para confirmar sua identidade, digite sua senha novamente: ')
    while True:
        interface.limpar_tela()
        confirmar_senha = validar_senha()
        if confirmar_senha == user_logado["senha"]:
            print('\033[0;32mIdentidade confirmada\033[m')
            return True
        else:
            print('\033[0;31mSenha incorreta\033[m')
            deseja_continuar = interface.tentar_novamente(mensagem = 'Deseja tentar confirmar sua identidade novamente?[S/N] ')
            if deseja_continuar == 'S':
                continue
            elif deseja_continuar == 'N':
                return False
            

def validar_id(mensagem = 'Digite o ID do item que foi resolvido: '):
    """
    -> Valida o id do item digitado pelo usuário
    :param mensagem: (str) Mostra uma mensagem personalizada dependendo da situação
    :return: (int) Retorna o id digitado pelo usuário
    """
    while True:
        id_escolhido = input(mensagem).strip()
        if id_escolhido == '':
            print('\033[0;31mO ID não pode ser vazio. Tente novamente\033[m')
            continue
        elif ' ' in id_escolhido:
            print('\033[0;31mO ID não pode conter espaços. Tente novamente\033[m')
            continue
        elif id_escolhido.startswith('-'):
            print(f'\033[0;31mO ID deve ser um número positivo. Tente novamente\033[m')
            continue
        elif '.' in id_escolhido or ',' in id_escolhido:
            print('\033[0;31mO ID deve ser um número inteiro. Tente novamente\033[m')
            continue
        elif not id_escolhido.isnumeric():
            print('\033[0;31mO ID deve conter apenas números. Tente novamente\033[m')
            continue
        else:
            return int(id_escolhido)