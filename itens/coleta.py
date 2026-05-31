from interface import Acessorio
from validacoes import Validador


class ColetarDadosItens:
    """ Gerencia a coleta de todos os dados necessários para o cadastro do item """
    @staticmethod
    def menu_categoria_itens():
        """
        -> Mostra o menu da categoria do item
        :return: (str/None) Retorna a opção que representa a categoria escolhida
                 pelo usuário ou None se digitou '0'
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
        
    @staticmethod
    def menu_local_itens():
        """
        -> Mostra o menu dos locais do item
        :return: (str/None) Retorna a opção que representa o local escolhido
                 pelo usuário ou None se digitou '0'
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
        
    @staticmethod
    def descricao_item():
        """
        -> Recebe valida a descrição digitada pelo usuário
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