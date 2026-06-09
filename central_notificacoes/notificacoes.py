import json, os, textwrap
from datetime import datetime
from interface import Acessorio
from validacoes import Validador


class Notificacoes:
    """ Gerencia o processamento e criação das notificações """
    arquivo = 'notificacoes.json'
    @staticmethod
    def _carregar_arquivo():
        """
        -> Carrega os dados do arquivo JSON de notificações e cria o arquivo se não existir
        :return: (dict) Retorna o dicionário com a lista de notificações
        """
        if not os.path.exists(Notificacoes.arquivo):
            with open(Notificacoes.arquivo, 'w', encoding='utf-8') as f:
                json.dump({'notificacoes': []}, f, indent=4)
        with open(Notificacoes.arquivo, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    @staticmethod
    def _salvar_arquivo(dados):
        """
        -> Salva os dados no arquivo JSON de notificações
        :param dados: (dict) Dicionário com os dados atualizados
        """
        with open(Notificacoes.arquivo, 'w', encoding='utf-8') as f:
            json.dump(dados, f, indent=4, ensure_ascii=False)

    @staticmethod
    def criar_notificacao(dono_id, tipo, mensagem):
        """
        -> Cria uma nova notificação para um determinado usuário
        :param dono_id: (str) Nome do usuário 
        :param tipo: (str) A categoria da notificação 
        :param mensagem: (str) O texto completo do aviso
        """
        dados = Notificacoes._carregar_arquivo()
        novo_id = max([i["id_notificacao"] for i in dados["notificacoes"]], default=0) + 1
        data_atual = datetime.now().strftime('%d/%m/%Y')
        nova_notificacao = {
            "id_notificacao": novo_id,
            "dono_id": dono_id,
            "tipo": tipo,
            "mensagem": mensagem,
            "lida": False,
            "data_criacao": data_atual
        }
        dados["notificacoes"].append(nova_notificacao)
        Notificacoes._salvar_arquivo(dados)

    @staticmethod
    def buscar_notificacoes(dono_id):
        """
        -> Busca todas as notificações de um determinado usuário
        :param dono_id: (str) Nome do usuário 
        :return: (list) Uma lista com os dicionários de cada notificação
        """
        dados = Notificacoes._carregar_arquivo()
        mensagens = [n for n in dados["notificacoes"] if n["dono_id"] == dono_id]
        return mensagens
    
    @staticmethod
    def marcar_lida(id_notificacao):
        """
        -> Altera o status de uma notificação para lida
        :param id_notificacao: (int) O ID da notificação que deve ser atualizada
        """
        dados = Notificacoes._carregar_arquivo()
        for notif in dados["notificacoes"]:
            if notif["id_notificacao"] == id_notificacao:
                notif["lida"] = True
                break
        Notificacoes._salvar_arquivo(dados)

    @staticmethod
    def deletar_notificacao(id_notificacao):
        """
        -> Exclui a notificação desejada pelo usuário
        :param id_notificacao: (int) O ID da notificação que será excluída
        """
        dados = Notificacoes._carregar_arquivo()
        dados['notificacoes'] = [n for n in dados['notificacoes'] if n['id_notificacao'] != id_notificacao]
        Notificacoes._salvar_arquivo(dados)

    @staticmethod
    def ler_notificacoes(notificacao):
        """
        -> Exibe a notificação e a marca como lida se ainda não estiver
        :param notificacao: (dict) O dicionário da notificação selecionada pelo usuário
        """
        Acessorio.limpar_tela()
        texto_formatado = textwrap.fill(
            notificacao['mensagem'],
            width = 54,
            initial_indent='   ',
            subsequent_indent='   '
        )
        print('\n')
        print('═'*60)
        print(f'MENSAGEM: {notificacao["tipo"]} | DATA: {notificacao["data_criacao"]}'.center(60))
        print('═'*60)
        print('\n')
        print(f'{texto_formatado}\n')
        print('═'*60)
        if not notificacao["lida"]:
            Notificacoes.marcar_lida(notificacao['id_notificacao'])


class QuadroDeAvisos:
    """ Gerencia a exibição e as ações do Quadro de Avisos """
    @staticmethod
    def exibir_menu(dono_id):
        """
        -> Exibe o Quadro de Avisos com a lista de notificações do usuário
        :param dono_id: (str) Nome do usuário
        """
        while True:
            notificacoes = Notificacoes.buscar_notificacoes(dono_id)
            Acessorio.limpar_tela()
            print('\n')
            print('=' * 60)
            print(f'QUADRO DE AVISOS - {dono_id}'.center(60))
            print('=' * 60)
            if not notificacoes:
                print('\n\n     Seu Quadro está vazio\n')
                print('-' * 60)
                sair = Validador.aguardar_retorno()
                if sair:
                    return
            else:
                for i, notif in enumerate(notificacoes, 1):
                    icone = '📖' if notif['lida'] else '📘' 
                    data_notif = notif.get('data_criacao', '##/##/####')
                    resumo = textwrap.shorten(
                        notif['mensagem'],
                        width = 24,
                        placeholder = '...'
                    )
                    print(f' [{notif["id_notificacao"]}] [{data_notif}] {icone} - {notif["tipo"]}: {resumo}')
                print('\n')
                print('─'*60)
                print("\nO que deseja fazer?")
                print("1. Ler notificação")
                print("2. Deletar notificação")
                print("0. Voltar")
                resposta = Validador.verificar_resposta_menu(0,2)
                if resposta == '0':
                    Acessorio.verificar_escape(resposta)
                    return
                elif resposta == '1':
                    QuadroDeAvisos._acao_notificacao(notificacoes, 'ler')
                else:
                    QuadroDeAvisos._acao_notificacao(notificacoes, 'deletar') 

    @staticmethod
    def _acao_notificacao(notificacoes, acao):
        """
        -> Permite o usuário ler ou deletar a notificaçãoo
        :param notificacoes: (list) Lista com as notificações do usuário
        :param acao: (str) Ação desejada pelo usuário
        """
        while True:
            mensagem = 'Digite o ID da notificação que você deseja ler: ' if acao == 'ler' else 'Digite o ID da notificação que você deseja deletar: '
            escolher_id = Validador.validar_id(mensagem)
            if any(n['id_notificacao'] == escolher_id for n in notificacoes):
                if acao == 'ler':
                    notif_escolhida = next(n for n in notificacoes if n['id_notificacao'] == escolher_id)
                    Notificacoes.ler_notificacoes(notif_escolhida)
                else:
                    Notificacoes.deletar_notificacao(escolher_id)
                    print('\033[0;32mNotificação deletada com sucesso!\033[m')
            else:
                print('\033[0;31mEste ID não existe ou não pertence a você.\033[m')
                tentar = Acessorio.tentar_novamente('Deseja tentar novamente com outro ID?[S/N] ')
                if tentar == 'S':
                    continue
                else: 
                    break
            sair = Validador.aguardar_retorno()
            if sair:
                return
            
    
        

