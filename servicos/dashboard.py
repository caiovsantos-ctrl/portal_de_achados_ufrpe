import textwrap
from validacoes import Validador
from data_base import DataBase
from interface import Acessorio
from .motores import DoacaoReciclagem
from .historico import Historico


class MenuServicos:
    """ Gerencia a exibição do menu de serviços (mural, histórico e mapa de calor) """
    @staticmethod
    def exibir_menu_servicos(user_logado):
        """
        -> Mostra o menu e direciona o usuário de acordo com sua opção
        :param user_logado: (obj) Objeto que representa os dados do usuário 
        """
        while True:
            Acessorio.limpar_tela()
            Acessorio.exibir_menu_padrao('MURAL E RELATÓRIOS', [
                    '[1] → Mural Geral (Itens Ativos)',
                    '[2] → Histórico (Meus Itens)',
                    '[3] → Mapa de Calor (Estatística)',
                    '[0] → Voltar'
                    ])
            resposta_menu = Validador.verificar_resposta_menu(0, 3)
            if resposta_menu == '0':
                Acessorio.verificar_escape(resposta_menu)
                return
            elif resposta_menu == '1':
                print('\033[0;32mMural Geral selecionado\033[m')
                MuralDeItens.menu_mural()
            elif resposta_menu == '2':
                print('\033[0;32mHistórico selecionado\033[m')
                Historico.menu_historico(user_logado)
            elif resposta_menu == '3':
                print('\033[0;32mMapa de Calor selecionado\033[m')
                MapaDeCalor.exibir_mapa_de_calor()


class MuralDeItens:
    """ Gerencia a exibição do mural de itens  """
    @staticmethod
    def menu_mural():
        from itens import ColetarDadosItens
        while True:
            Acessorio.limpar_tela()
            Acessorio.exibir_menu_padrao('FILTROS', [
                        '[1] → Ver Tudo',
                        '[2] → P/ Categoria',
                        '[3] → P/ Local',
                        '[0] → Voltar'
                        ])
            resposta_menu = Validador.verificar_resposta_menu(0, 3)   
            if resposta_menu == '0':
                Acessorio.verificar_escape(resposta_menu)
                return
            elif resposta_menu == '1':
                MuralDeItens.exibir_mural()     
            elif resposta_menu == '2':
                categoria = ColetarDadosItens.menu_categoria_itens()
                if categoria:
                    MuralDeItens.exibir_mural(filtro_cat=categoria) 
            elif resposta_menu == '3':
                local = ColetarDadosItens.menu_local_itens()
                if local:
                    MuralDeItens.exibir_mural(filtro_loc=local) 


    @staticmethod
    def exibir_mural(filtro_cat=None, filtro_loc=None):
        """ Mostra o mural de itens """
        DoacaoReciclagem.processar_temporalidade()
        Acessorio.limpar_tela()
        #print('Mural de Itens:\n\n'.center(70))
        titulo = 'Mural de Itens'
        if filtro_cat:
            titulo += f' - Categoria: {filtro_cat}'
        if filtro_loc:
            titulo += f' - Categoria: {filtro_loc}'
        print(f'{titulo}:\n\n'.center(70))
        print('-' * 70)
        todos_itens = DataBase.buscar_todos_itens()
        itens_ativos = [i for i in todos_itens if not i.get("resolvido", False)]
        if filtro_cat:
            itens_ativos = [i for i in itens_ativos if i.get("categoria") == filtro_cat]
        if filtro_loc:
            itens_ativos = [i for i in itens_ativos if i.get("local") == filtro_loc]
        if not itens_ativos:
            print('\nO Mural está vazio no momento')
        else:
            for item in itens_ativos:
                tipo_bruto = item["tipo_registro"]
                liberado = item.get("liberado", False)
                tipo = 'Achei' if item["tipo_registro"] == 'Achado' else 'Perdi'
                data = item.get("data_cadastro", '00/00/0000')
                print(f'ID: {item["id"]:02d} | {tipo} | {data} | {item["local"]}')
                print(f'Postado por: {item.get("autor", "Usuário")}')
                print(f'Categoria: {item["categoria"]}')
                if tipo_bruto == 'Achado':
                    if liberado:
                        texto_desc = f'Item liberado para doação/reciclagem: {item["descricao"]}'
                    else:
                        texto_desc = 'Para manter a transparência, a descrição está oculta'
                else:
                    texto_desc = item["descricao"]
                descricao_formatada = textwrap.fill(
                    texto_desc,
                    width=65,
                    initial_indent= 'Descrição: ',
                    subsequent_indent='           '
                )
                print(descricao_formatada)
                print(f'Contato: {item["contato"]}\n')
                print('-' * 70)
            sair = Validador.aguardar_retorno()
            if sair:
                return


class MapaDeCalor:
    """ Gerencia a exibição do mapa de calor dos locais onde mais ocorrem registros """
    @staticmethod
    def exibir_mapa_de_calor():
        """ Mostra o mapa de calor dos itens """
        Acessorio.limpar_tela()
        print('Mapa de Calor: \n\n'.center(60))
        todos_itens = DataBase.buscar_todos_itens()
        if not todos_itens:
            print('Não há dados suficientes para gerar o Mapa de Calor')
        else:
            contagem = {}
            for item in todos_itens:
                local = item.get("local", "Desconhecido")
                contagem[local] = contagem.get(local, 0) + 1
            locais_ordenados = sorted(contagem.items(), key=lambda x: x[1], reverse=True)
            print(f"\n{'LOCAL':<25} | {'INTENSIDADE':<20} | {'TOTAL'}")
            print("-" * 60)
            for local, total in locais_ordenados:
                barra = '■' * total
                print(f"{local:<25} | {barra:<20} | {total} itens")
            print("\n" + "="*60)
        sair = Validador.aguardar_retorno()
        if sair:
            return