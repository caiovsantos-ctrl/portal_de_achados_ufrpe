import json, os
from interface import Acessorio
from validacoes import Validador
from data_base import DataBase
from servicos import GerenciadorServicos


class Item:
    def __init__(self, tipo_registro, categoria, local, descricao, contato, resolvido, autor, id_item=None):
        self._id_item = id_item
        self._tipo_registro = tipo_registro
        self._categoria = categoria
        self._local = local
        self._descricao = descricao
        self._contato = contato
        self._resolvido = resolvido
        self._autor = autor

    @property
    def tipo_registro(self):
        return self._tipo_registro

    @property
    def categoria(self):
        return self._categoria

    @property
    def local(self):
        return self._local

    @property
    def descricao(self):
        return self._descricao

    @property
    def contato(self):
        return self._contato

    @property
    def resolvido(self):
        return self._resolvido
    @resolvido.setter
    def resolvido(self, valor):
        self._resolvido = valor

    @property
    def autor(self): 
        return self._autor

    @property
    def id_item(self):
        return self._id_item
    @id_item.setter
    def id_item(self, valor):
        self._id_item = valor

    def transformar_dicionario(self):
        dados = {
            "tipo_registro": self._tipo_registro,
            "categoria": self._categoria,
            "local": self._local,
            "descricao": self._descricao,
            "resolvido": self._resolvido,
            "contato": self._contato,
            "autor": self._autor
        }
        if self._id_item is not None:
            dados["id_item"] = self.id_item
        return dados 
    

class GerenciadorItens:
    def __init__(self):
        pass

    def menu_itens(self):
        """
        -> Mostra o menu da categoria do item
        :return: (int/None) Retorna a opção digitada pelo usuário ou None se digitou '0'
        """
        categorias = [
            "Eletrônicos", "Chave", "Documentos", "Carteira", 
            "Materiais acadêmicos", "Vestuários", "Itens de alimentação"
        ]
        while True:
            Acessorio.limpar_tela()
            opcoes_formatadas = [f"[{i}] → {nome}" for i, nome in enumerate(categorias, 1)]
            opcoes_formatadas.append("[0] → Voltar")
            Acessorio.exibir_menu_padrao('CATEGORIA DO ITEM', opcoes_formatadas)
            resposta_menu = Validador.verificar_resposta_menu(0, len(categorias))
            if resposta_menu == '0':
                Acessorio.verificar_escape(resposta_menu)
                Acessorio.limpar_tela()
                return None
            return categorias[int(resposta_menu) - 1]
        
    def menu_local(self):
        """
        -> Mostra o menu dos locais do item
        :return: (int/None) Retorna a opção digitada pelo usuário ou None se digitou '0'
        """
        locais = [
            "CEGOE", "Prédio Central", "CEAGRI", "RU", 
            "Biblioteca Central", "Depto. Biologia/ Química", 
            "Depto. Ed. Física", "Vizinhança"
        ]
        while True:
            Acessorio.limpar_tela()
            opcoes_locais = [f"[{i}] → {local}" for i, local in enumerate(locais, 1)]
            opcoes_locais.append("[0] → Voltar")
            Acessorio.exibir_menu_padrao("LOCAIS DA UFRPE", opcoes_locais, largura=60)
            resposta_local = Validador.verificar_resposta_menu(0, len(locais))
            if resposta_local == '0':
                Acessorio.verificar_escape(resposta_local)
                Acessorio.limpar_tela()
                return None
            return locais[int(resposta_local) - 1]
        
    def descricao_item(self):
        """
        -> Valida a descrição digitada pelo usuário
        :return: (str/None) Retorna a descrição digitada pelo usuário ou None se digitou '0'
        """
        while True:
            Acessorio.limpar_tela()
            print('-' * 50)
            print('Detalhes do item'.center(50))
            print('-' * 50)
            print('\nDigite uma descrição objetiva: ')
            print('Ex.: Iphone com capinha branca e tela trincada\n')
            descricao = input('=> ')
            descricao = descricao.strip().capitalize()
            if descricao == '0':
                return None
            elif descricao == "":
                print('\033[0;31mA descrição não pode ser vazia. Tente novamente.\033[m')
                continue
            elif len(descricao) < 20:
                print('\033[0;31mA descricao deve conter pelo menos 20 caracteres. Tente novamente\033[m')
                continue
            elif len(descricao) > 100:
                print('\033[0;31mA descrição deve conter no máximo 100 caracteres. Tente novamente\033[m')
                continue
            elif descricao.isnumeric():
                print('\033[0;31mA descrição não pode conter apenas números. Tente novamente\033[m')
                continue
            elif descricao == descricao[0] * len(descricao):
                print('\033[0;31mA descrição não pode conter apenas dígitos iguais. Tente novamente\033[m')
                continue
            else:
                return descricao

    def achar_perder_item(self, status, user_logado):
        """
        -> Armazena no JSON os dados dos itens cadastrados
        :param status: (str) Define o tipo de registro do item(achado ou perdido)
        :param user_logado: (dict) Dicionário que guarda os dados do usuário 
        :return: (dict/None)  Retorna um dicionário com os dados do item ou 
        None se o usuário desistiu em alguma parte
        """
        Acessorio.limpar_tela()
        resposta_item = self.menu_itens()
        if resposta_item is None:
            return None
        resposta_local = self.menu_local()
        if resposta_local is None:
            return None
        resposta_descricao = self.descricao_item()
        if resposta_descricao is None:
            return None
        contato_user = user_logado.Whatsapp
        autor_user = user_logado.nome
        return Item(
            tipo_registro=status,
            categoria=resposta_item,
            local=resposta_local,
            descricao=resposta_descricao,
            resolvido=False,
            contato=contato_user,
            autor=autor_user
        )
    
    def gestao_itens(self, user_logado):
        """
        -> Reúne todos os processos em relação ao item, desde o cadastro até o match
        :param user_logado: (dict) Dicionário que guarda os dados do usuário 
        """
        while True:
            match = None
            Acessorio.limpar_tela()
            Acessorio.exibir_menu_padrao('SITUAÇÃO DO ITEM', [
                    '[1] → Achei Item',
                    '[2] → Perdi Item',
                    '[0] → Voltar'
                    ])
            resposta_menu = Validador.verificar_resposta_menu(0, 2)
            if resposta_menu == '0':
                Acessorio.limpar_tela()
                return
            status = 'Achado' if resposta_menu == '1' else 'Perdido'
            while True:
                item_cadastrado = self.achar_perder_item(status, user_logado)
                if not item_cadastrado:
                    return
                match, foi_duplicado = GerenciadorServicos.motor_de_buscas(item_cadastrado)
                if foi_duplicado:
                    print('\n\033[0;31mVocê já possui um item similar cadastrado por você\033[m')
                    print('O sistema não mostra seus próprios itens no Match para evitar confusão\n')
                    if Acessorio.tentar_novamente():
                        continue
                    else:
                        item_cadastrado = None
                        break
                else:
                    if item_cadastrado:
                        dict_retorno = DataBase.salvar_item(item_cadastrado)
                        item_cadastrado.id_item = dict_retorno["id"]
                        print('\033[0;32mItem cadastrado com sucesso!\033[m')
                        break
            if item_cadastrado and match:
                if status == 'Perdido':
                    print('\n\033[0;32mBoas notícias! Alguém pode ter encontrado seu item:\033[m\n')
                else:
                    print('\033[0;32mAtenção! Alguém perdeu um item parecido com este:\033[m\n')
                for m in match:
                    print(f'ID: {m["id"]} | {m["categoria"]} no(a) {m["local"]}')
                    print(f'Descrição: {m["descricao"]}')
                    print(f'Contato: {m["contato"]}  {m["autor"]}')
                if status == 'Perdido':
                    print('\nChame no Whatsapp agora para combinar a retirada')
                else:
                    print('\nChame no Whatsapp agora para combinar a retirada')
                confirmar = Acessorio.tentar_novamente(mensagem = '\nSeu problema foi resolvido?[S/N]')
                if confirmar == 'S':
                    id_match = int(m["id_item"])
                    id_meu = item_cadastrado.id_item
                    if self.atualizar_status_item(id_match):
                        self.atualizar_status_item(id_meu)
                        print('\033[0;32mÓtima notícia! Item marcado como resolvido\033[m')
                    else:
                        print('\033[0;31mErro ao atualizar status\033[m')
                else:
                    print('Entendido! Seu item continuará ativo no mural para novos matches')
                sair = input('\nDigite 0 para voltar: ')
                Acessorio.verificar_escape(sair)
            else:
                if item_cadastrado:
                    print('Nenhum match imediato, veja o mural de itens')
                    sair = input('\nDigite 0 para voltar: ')
                    Acessorio.verificar_escape(sair)
                return
            
    def atualizar_status_item(id_item):
        """
        -> Faz o processo para atualizar o status do item
        :param id_item: (int) Id específico do item 
        :return: (bool) Retorna True se atualizou o status ou False se não 
        """
        nome_arquivo = 'itens.json'
        if not os.path.exists(nome_arquivo):
            return False
        with open(nome_arquivo, 'r', encoding='utf-8') as arquivo:
            meus_itens = json.load(arquivo)
        alterado = False
        for item in meus_itens:
            if item["id"] == id_item:
                item["resolvido"] = True
                alterado = True
                break
        if alterado:
            with open(nome_arquivo, 'w', encoding='utf-8') as arquivo:
                json.dump(meus_itens, arquivo, indent=4, ensure_ascii=False)
            return True
        return False
    
    def deletar_item(id_item, contato_usuario):
        """
        -> Faz o processo para deletar o item
        :param id_item: (int) Id específico do item 
        :param contato_usuario: (str) N° do whatsapp do usuário
        :return: (bool) Retorna True se deletou o item ou False se não 
        """
        nome_arquivo = 'itens.json'
        if not os.path.exists(nome_arquivo):
            return False
        with open(nome_arquivo, 'r', encoding='utf-8') as file:
            todos_itens = json.load(file)
        nova_lista = [
            item for  item in todos_itens
            if not (int(item["id"]) == int(id_item) and item["contato"] == contato_usuario)
        ]
        if len(nova_lista) < len(todos_itens):
            with open(nome_arquivo, 'w', encoding='utf-8') as file:
                json.dump(nova_lista, file, indent=4, ensure_ascii=False)
            return True
        return False