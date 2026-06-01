import json, os
from datetime import datetime


class DataBase:
    """ Gerencia a persistência de dados, realizando a leitura e escrita nos arquivos JSON """
    @staticmethod
    def salvar_user(novo_user): 
        """
        -> Salva no JSON as informações cadastradas pelo usuário
        :param novo_user: (obj) Objeto que representa as informações realizadas pelo usuário no cadastro 
        """
        user_dict = novo_user.transformar_dicionario() if hasattr(novo_user, 'transformar_dicionario') else novo_user
        with open('usuarios.json', 'r', encoding='utf-8') as arquivo:
            lista_user = json.load(arquivo)
            lista_user.append(user_dict)
        with open('usuarios.json', 'w', encoding='utf-8') as arquivo:
            json.dump(lista_user, arquivo, indent=4, ensure_ascii=False)
        print('\033[0;32mCadastro concluído com sucesso!\033[m')

    @staticmethod
    def salvar_item(item_cadastrado):
        """
        -> Salva no JSON as informações dos itens e adiciona seu id e data
        :param item_cadastrado: (obj) Objeto que representa as informações dos itens
        :return: (obj) Retorna o id e a data de cadastro do item
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
        item_dict = item_cadastrado.transformar_dicionario() if hasattr(item_cadastrado, 'transformar_dicionario') else item_cadastrado
        item_atualizado.update(item_dict)
        lista_itens.append(item_atualizado)
        with open (arquivo, 'w', encoding='utf-8') as file:
            json.dump(lista_itens, file, indent=4, ensure_ascii=False)
            return item_atualizado

    @staticmethod
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
    
    @staticmethod
    def buscar_todos_itens():
        """
        -> Busca todos os itens que estão no JSON 
        :return: (JSON) Retorna todos os itens do JSON
        """
        if not os.path.exists('itens.json'):
            return []
        with open('itens.json', 'r', encoding='utf-8') as arquivo:
            return json.load(arquivo)

    @staticmethod
    def carregar_usuarios():
        """ 
        Carrega os usuários do arquivo JSON
        :return: (list) Retorna uma lista com os dados dos usuários ou 
                 uma lista vazia se o arquivo não existir ou acontecer um erro
        """
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
        
    @staticmethod
    def salvar_no_json(email_atual, campo, novo_valor):
        """
        -> Localiza o usuário pelo e-mail e atualiza o campo no arquivo JSON
        :param user_logado: (obj) Objeto que representa o usuário logado
        :param campo: (str) O dado que o usuário deseja atualizar
        :param novo_valor: (str) O dado atualizado pelo usuário
        :return: (bool) Retorna True se o dado foi atualizado ou False se deu algum erro
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
        
    @staticmethod   
    def deletar_no_json(user_logado):
        """
        -> Deleta a conta do usuário no JSON
        :return: (bool) True se deletou ou False se ocorreu um erro
        """
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
                    return True
            return False
        except Exception:
            return False