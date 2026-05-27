import os, json, textwrap, unicodedata
from datetime import datetime
from difflib import SequenceMatcher
from validacoes import Validador
from data_base import DataBase
from interface import Acessorio


class MotorDeBusca:
    """ Gerencia a lógica de busca e comparação de itens para
        encontrar possíveis matches entre achados e perdidos """
    @staticmethod
    def calcular_similaridade(texto1, texto2):
        """
        -> Calcula a similaridade entre dois textos
        :param texto1: (str) Primeiro texto para comparação
        :param texto2: (str) Segundo texto para comparação
        :return: (float) Similaridade entre os textos, variando de 0 a 1
        """
        return SequenceMatcher(None, texto1, texto2).ratio()
    
    @staticmethod
    def remover_acentos(texto):
        """
        -> Remove acentos de um texto para facilitar a comparação
        :param texto: (str) Texto do qual os acentos serão removidos
        :return: (str) Texto sem acentos
        """
        processado = unicodedata.normalize('NFD', texto)
        return ''.join([c for c in processado if unicodedata.category(c) != 'Mn'])
    
    @staticmethod
    def buscar_matches(item_cadastrado):
        """
        -> Procura um item recomendado para dar match
        :param item_cadastrado: (dict) Dicionário que guarda as informações do item
        :return: (list/bool) Retorna matches (lista com os itens que deu match) e 
        postagem_duplicada (True se o usuário cadastrou o mesmo item e False se não)
        """
        nome_arquivo = 'itens.json'
        matches = []
        postagem_duplicada = False
        if not os.path.exists(nome_arquivo):
            return matches, postagem_duplicada
        with open(nome_arquivo, 'r', encoding='utf-8') as file:
            todos_itens = json.load(file)
        descricao = item_cadastrado.descricao
        contato = item_cadastrado.contato
        categoria = item_cadastrado.categoria
        local = item_cadastrado.local
        tipo_registro = item_cadastrado.tipo_registro
        desc_limpa = MotorDeBusca.remover_acentos(descricao.lower())
        palavras_chaves = [p for p in desc_limpa.split() if len(p) > 2]
        for item_banco in todos_itens:
            if item_banco["contato"] == contato:
                if item_banco["categoria"] == categoria and \
                item_banco["local"] == local:
                    postagem_duplicada = True
                continue
            if item_banco["tipo_registro"] != tipo_registro and not item_banco["resolvido"]:
                if item_banco["local"] == local and item_banco["categoria"] == categoria:
                    desc_banco_limpa = MotorDeBusca.remover_acentos(item_banco["descricao"].lower())
                    descricao_salva = desc_banco_limpa.split()
                    palavras_encontradas = 0
                    for palavra in palavras_chaves:
                        match_na_palavra = False
                        for palavra_salva in descricao_salva:
                            if palavra == palavra_salva or MotorDeBusca.calcular_similaridade(palavra, palavra_salva) >= 0.8:
                                match_na_palavra = True
                                break
                        if match_na_palavra:
                            palavras_encontradas += 1
                    if palavras_encontradas >= 3:
                        matches.append(item_banco)
        return matches, postagem_duplicada  
    
    
class MuralDeItens:
    """ Gerencia a exibição do mural de itens  """
    @staticmethod
    def exibir_mural():
        """ Mostra o mural de itens """
        DoacaoReciclagem.processar_temporalidade()
        Acessorio.limpar_tela()
        print('Mural de Itens:\n\n'.center(70))
        print('-' * 70)
        todos_itens = DataBase.buscar_todos_itens()
        itens_ativos = [i for i in todos_itens if not i.get("resolvido", False)]
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

    
class Historico:
    """ Gerencia a exibição do histórico do usuário e as ações de atualizar ou deletar um item """
    @staticmethod
    def menu_historico(user_logado):
        """
        -> Mostra o histórico do usuário e as opções de deletar ou atualizar status do item
        :param user_logado: (obj) Objeto que representa os dados do usuário 
        """
        while True:
            DoacaoReciclagem.processar_temporalidade()
            Acessorio.limpar_tela()
            meus_itens = Historico.exibir_historico(user_logado)
            if not meus_itens:
                return
            resposta_menu = Historico.exibir_menu_acoes_historico(meus_itens)
            if resposta_menu == '0':
                Acessorio.limpar_tela()
                return
            if resposta_menu == '1':
                Historico.atualizar_status_item(meus_itens)
            elif resposta_menu == '2':
                Historico.deletar_item(meus_itens, user_logado.Whatsapp)
    
    @staticmethod
    def exibir_historico(user_logado):    
        """
        -> Mostra o histórico do usuário
        :param user_logado: (obj) Objeto que representa os dados do usuário 
        """ 
        print('Seu Histórico:\n\n'.center(95))
        contato_user = user_logado.Whatsapp
        meus_itens = DataBase.buscar_itens_por_usuario(contato_user)
        if not meus_itens:
            print('-' * 95)
            print('\nVocê não possui nenhum item cadastrado')
            print('Cadastre um item e volte aqui novamente!\n')
            print('-' * 95)
            sair = Validador.aguardar_retorno()
            if sair:
                return
        print(f"{'ID':<4} | {'DATA':<10} | {'TIPO':<7} | {'STATUS':<10} | {'CATEGORIA':<25} | {'LOCAL'}")
        print('-' * 95)
        for item in meus_itens:
            data = item.get("data_cadastro", "00/00/00")
            tipo = "Achei" if item["tipo_registro"] == "Achado" else "Perdi"
            if item["resolvido"]:
                status_texto = 'RESOLVIDO'
            elif  item.get("liberado"):
                status_texto = 'P/ DOAÇÃO'  
            else:
                status_texto = 'ATIVO'
            print(f'{item["id"]:<4} | {data:<10} | {tipo:<7} | {status_texto:<10} | {item["categoria"]:<25} | {item["local"]}')
            print('-' * 95)
        return meus_itens   
    
    
    @staticmethod
    def exibir_menu_acoes_historico(meus_itens): 
        """ 
        Exibe o menu de ações para o histórico do usuário
        :param meus_itens: (list) Lista de itens cadastrados pelo usuário
        """
        print("\nO que deseja fazer?")
        print("1. Marcar item como resolvido")
        print("2. Deletar um item")
        print("0. Voltar")
        return Validador.verificar_resposta_menu(0, 2)

    @staticmethod
    def atualizar_status_item(meus_itens):
        """ 
        Realiza a atualização do status de um item para resolvido
        :param meus_itens: (list) Lista de itens cadastrados pelo usuário
        """
        import itens
        while True:
            escolher_id = Validador.validar_id(mensagem = 'Digite o ID do item que foi resolvido: ')
            if any(i["id"] == escolher_id for i in meus_itens):
                if itens.AtualizarStatusItem.processar_atualizacao_item(escolher_id):
                    print('\033[0;32mStatus atualizado com sucesso!\033[m')
                else:
                    print('\033[0;31mErro ao atualizar. Tente novamente mais tarde\033[m')
                voltar = input('\nDigite 0 para voltar: ')
                Acessorio.verificar_escape(voltar)
                break
            else:
                print('\033[0;31mEste ID não existe ou não pertence a você\033[m')
                tentar = Acessorio.tentar_novamente(mensagem = 'Deseja tentar novamente com outro ID?[S/N]')
                if tentar == 'S':
                    continue
                else:
                    break
                    
    @staticmethod
    def deletar_item(meus_itens, contato_user):
        """ 
        Realiza a deleção de um item
        :param meus_itens: (list) Lista de itens cadastrados pelo usuário
        :param contato_usuario: (str) N° do whatsapp do usuário
        """
        import itens
        while True:
            id_deletar = Validador.validar_id(mensagem = 'Digite o ID do item que você deseja deletar: ')            
            item_existe = any(i["id"] == id_deletar for i in meus_itens)
            if item_existe:
                print('\nAtenção! Você está prestes a deletar um item')
                tentar = Acessorio.tentar_novamente(mensagem = 'Tem certeza que deseja deletar esse item?[S/N] ')
                if tentar == 'S':
                    if itens.DeletarItem.processar_delecao_item(id_deletar, contato_user):
                        print('\033[0;32mItem removido com sucesso\033[m')
                    else:
                        print('\033[0;31mErro ao deletar item. Tente novamente mais tarde\033[m')
                    voltar = input('\nDigite 0 para voltar: ')
                    Acessorio.verificar_escape(voltar)
                    break
                else:
                    continue
            else:
                print('\033[0;31mEste ID não existe ou não pertence a você\033[m')
                tentar = Acessorio.tentar_novamente(mensagem = 'Deseja tentar novamente com outro ID?[S/N]')
                if tentar == 'S':
                    continue
                else:
                    break
                    
    
class DoacaoReciclagem:
    """ Gerencia o processo de liberar um item para doação ou reciclagem após 30 dias do cadastro """
    @staticmethod
    def processar_temporalidade():
        """
        Transforma o status do item para 'Disponível para doação/reciclagem'
        se passou de 30 dias que foi cadastrado e não foi encontrado o dono
        """
        arquivo = 'itens.json'
        if not os.path.exists(arquivo):
            return
        with open(arquivo, 'r', encoding='utf-8') as file:
            lista_itens = json.load(file)
        alterado = False
        data_hoje = datetime.now()
        for item in lista_itens:
            if not item.get("resolvido") and "data_cadastro" in item:
                try:
                    data_item = datetime.strptime(item["data_cadastro"], '%d/%m/%Y')
                    diferenca = data_hoje - data_item
                    if diferenca.days > 30 and not item.get("liberado"):
                        item["liberado"] = True
                        item["status_final"] = 'Disponível para doação/reciclagem'
                        alterado = True
                except:
                    continue
        if alterado:
            with open(arquivo, 'w', encoding='utf-8') as file:
                json.dump(lista_itens, file, indent=4, ensure_ascii=False)

    
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
                MuralDeItens.exibir_mural()
            elif resposta_menu == '2':
                print('\033[0;32mHistórico selecionado\033[m')
                Historico.menu_historico(user_logado)
            elif resposta_menu == '3':
                print('\033[0;32mMapa de Calor selecionado\033[m')
                MapaDeCalor.exibir_mapa_de_calor()