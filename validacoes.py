import json
import interface


def verificar_resposta_menu(inicio_range, fim_range):
    while True:
        resposta_menu = input('=> ')
        resposta_menu = resposta_menu.strip()
        if resposta_menu == "":
            print('A resposta não pode ser vazia. Tente novamente.')
            continue
        elif resposta_menu.startswith('-'):
            print(f'A resposta deve ser entre {inicio_range} e {fim_range}. Tente novamente.')
            continue
        elif '.' in resposta_menu or ',' in resposta_menu:
            print('A resposta deve ser um número inteiro. Tente novamente.')
            continue
        elif not resposta_menu.isnumeric():
            print('A resposta deve ser um número. Tente novamente.')
            continue
        resposta_menu_int = int(resposta_menu)
        if resposta_menu_int < inicio_range or resposta_menu_int > fim_range:
            print(f'A resposta deve ser entre {inicio_range} e {fim_range}. Tente novamente.')
            continue
        return resposta_menu
    

def validar_nome():
    while True:
        interface.limpar_tela()
        nome = input('Nome: ')
        nome = nome.strip().capitalize()
        if interface.verificar_escape(nome):
            interface.limpar_tela()
            return None
        if nome == "":
            print('O nome não pode ser vazio. Tente novamente.')
            continue
        elif len(nome) < 3:
            print('O nome deve conter pelo menos 3 caracteres. Tente novamente.')
            continue
        elif len(nome) > 15:
            print('O nome deve conter no máximo 15 caracteres. Tente novamente.')
            continue
        elif nome.isnumeric():
            print('O nome não pode conter números. Tente novamente.')
            continue
        elif not nome.replace(' ', '').isalpha():
            print('O nome não pode conter números ou caracteres especiais. Tente novamente.')
            continue
        elif len(nome.split(' ')[0]) < 3:
            print('O primeiro nome deve ter pelo menos 3 letras')
            continue
        else:
            return nome


def validar_email():
    while True:
        interface.limpar_tela()
        email = input('\nEmail institucional: ')
        email = email.strip().lower()
        email_cortado = email.split('@')[0]
        if interface.verificar_escape(email):
            interface.limpar_tela()
            return None
        if email == "":
            print('O email não pode ser vazio. Tente novamente.')
            continue
        elif ' ' in email:
            print('O email não pode conter espaços. Tente novamente.')
            continue
        elif email_cortado.isnumeric():
            print('O email não pode conter apenas números. Tente novamente.')
            continue
        elif not email_cortado.replace('.', '').replace('_', '').isalnum():
            print('O email deve conter letras e/ou números. Tente novamente.')
            continue
        elif not email.endswith('@ufrpe.br'):
            print('O email deve ser institucional (deve terminar com @ufrpe.br). Tente novamente.')
            continue
        elif len(email) < 15:
            print('O email deve conter pelo menos 15 caracteres. Tente novamente.')
            continue
        elif len(email) > 30:
            print('O email deve conter no máximo 30 caracteres. Tente novamente.')
            continue
        else:
            return email


def validar_senha():
    while True:
        interface.limpar_tela()
        senha = input('\nSenha (6-8 caracteres numéricos): ')
        senha = senha.strip()
        if interface.verificar_escape(senha):
            interface.limpar_tela()
            return None
        if senha == '':
            print('A senha não pode ser vazia. Tente novamente.')
            continue
        elif ' ' in senha:
            print('A senha não pode conter espaços. Tente novamente.')
            continue
        elif not senha.isnumeric():
            print('A senha deve conter apenas números. Tente novamente.')
            continue
        elif len(senha) < 6 or len(senha) > 8:
            print('A senha deve conter entre 6 a 8 caracteres. Tente novamente.')
            continue
        elif senha == '123456' or senha == '1234567' or senha == '12345678':
            print('Digite uma senha mais segura.')
            continue
        elif senha == senha[0] * len(senha):
            print('A senha não deve conter todos os dígitos iguais. Tente novamente')
            continue
        else:
            return senha
        

def validar_zap():
    while True:
        interface.limpar_tela()
        zap = input('\nWhatsapp (ex.: 81912345678): ')
        zap = zap.strip()
        if interface.verificar_escape(zap):
            interface.limpar_tela()
            return None
        if zap == '':
            print('O n° do Whatsapp não pode ser vazio. Tente novamente')
            continue
        elif ' ' in zap:
            print('O n° do Whatsapp não pode conter espaços. Tente novamente')
            continue
        elif not zap.isnumeric():
            print('O n° do Whatsapp deve conter apenas números. Tente novamente')
            continue
        elif len(zap) != 11:
            print('O n° do Whatsapp deve conter 11 caracteres. Tente novamente')
            continue
        elif zap[2] != '9':
            print('Após o DDD deve conter o 9. Tente novamente')
            continue
        elif zap == zap[0] * len(zap):
            print('O n° do Whatsapp não deve conter todos os dígitos iguais. Tente novamente')
            continue
        elif int(zap[:2]) > 98 or int(zap[:2]) < 11:
            print('DDD inválido. Tente novamente')
            continue
        else:
            return zap



def email_ja_existe(email_digitado):
    try:
        with open('usuarios.json', 'r', encoding='utf-8') as arquivo:
            usuarios = json.load(arquivo)
        for user in usuarios:
            if user["email"] == email_digitado:
                return True
        return False
    except (FileNotFoundError, json.JSONDecodeError):
        return False
    

def confirmar_identidade(user_logado):
    interface.limpar_tela()
    print('Para confirmar sua identidade, digite sua senha novamente: ')
    while True:
        interface.limpar_tela()
        confirmar_senha = validar_senha()
        if confirmar_senha == user_logado["senha"]:
            print('Identidade confirmada')
            return True
        else:
            print('Senha incorreta')
            deseja_continuar = interface.tentar_novamente(mensagem = 'Deseja tentar confirmar sua identidade novamente?[S/N] ')
            if deseja_continuar == 'S':
                continue
            elif deseja_continuar == 'N':
                return False
            

def validar_id(mensagem = 'Digite o ID do item que foi resolvido: '):
    while True:
        id_escolhido = input(mensagem).strip()
        if id_escolhido == '':
            print('O ID não pode ser vazio. Tente novamente.')
            continue
        elif ' ' in id_escolhido:
            print('O ID não pode conter espaços. Tente novamente.')
            continue
        elif id_escolhido.startswith('-'):
            print(f'O ID deve ser um número positivo. Tente novamente.')
            continue
        elif '.' in id_escolhido or ',' in id_escolhido:
            print('O ID deve ser um número inteiro. Tente novamente.')
            continue
        elif not id_escolhido.isnumeric():
            print('O ID deve conter apenas números. Tente novamente.')
            continue
        else:
            return int(id_escolhido)