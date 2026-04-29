import json, os
from datetime import datetime


def salvar_user(novo_user): 
    """
    -> Salva no JSON as informações cadastradas pelo usuário
    :param novo_user: (dict) Dicionário que guarda as informações realizadas pelo usuário no cadastro 
    """
    with open('usuarios.json', 'r', encoding='utf-8') as arquivo:
        lista_user = json.load(arquivo)
        lista_user.append(novo_user)
    with open('usuarios.json', 'w') as arquivo:
        json.dump(lista_user, arquivo, indent=4, ensure_ascii=False)
    print('\033[0;32mCadastro concluído com sucesso!\033[m')


def salvar_item(item_cadastrado):
    """
    -> Salva no JSON as informações dos itens e adiciona seu id e data
    :param item_cadastrado: (dict) Dicionário que guarda as informações dos itens
    :return: (dict) Retorna o id e a data de cadastro do item
    """
    arquivo = 'itens.json'
    if os.path.exists(arquivo):
        with open(arquivo, 'r', encoding='utf-8') as file:
            lista_itens = json.load(file)
    else:
        lista_itens = []
    id_item = max([i['id'] for i in lista_itens], default=0) + 1
    data_hoje = datetime.now().strftime('%d/%m/%Y')
    item_atualizado = {
        "id": id_item,
        "data_cadastro": data_hoje
    }
    item_atualizado.update(item_cadastrado)
    lista_itens.append(item_atualizado)
    with open (arquivo, 'w', encoding='utf-8') as file:
        json.dump(lista_itens, file, indent=4, ensure_ascii=False)
        return item_atualizado


def buscar_itens_por_usuario(contato_usuario):
    """
    -> Busca todos os itens que estão no JSON de um usuário em específico
    :param contato_usuario: (str) N° do whatsapp do usuário
    :return: (list) Retorna uma lista com as informações de todos os itens do
    usuário ou uma lista vazia se der erro ou se não tiver nenhum 
    """
    nome_arquivo = 'itens.json'
    if not os.path.exists(nome_arquivo):
        return []
    try:
        with open(nome_arquivo, 'r', encoding='utf-8') as file:
            todos_itens = json.load(file)
    except (json.JSONDecodeError, FileNotFoundError):
        return []
    itens_pessoais = [item for item in todos_itens if item["contato"] == contato_usuario]
    return itens_pessoais


def buscar_todos_itens():
    """
    -> Busca todos os itens que estão no JSON 
    :return: (JSON) Retorna todos os itens do JSON
    """
    if not os.path.exists('itens.json'):
        return []
    with open('itens.json', 'r', encoding='utf-8') as arquivo:
        return json.load(arquivo)





