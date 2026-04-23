import json, os
from datetime import datetime


def salvar_user(novo_user): 
    with open('usuarios.json', 'r', encoding='utf-8') as arquivo:
        lista_user = json.load(arquivo)
        lista_user.append(novo_user)
    with open('usuarios.json', 'w') as arquivo:
        json.dump(lista_user, arquivo, indent=4, ensure_ascii=False)
    print('\033[0;32mCadastro concluído com sucesso!\033[m')


def salvar_item(item_cadastrado):
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


def buscar_itens_por_usuario(contato_usuario):
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
    if not os.path.exists('itens.json'):
        return []
    with open('itens.json', 'r', encoding='utf-8') as arquivo:
        return json.load(arquivo)





