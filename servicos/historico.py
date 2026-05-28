from validacoes import Validador
from data_base import DataBase
from interface import Acessorio
from .motores import DoacaoReciclagem

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