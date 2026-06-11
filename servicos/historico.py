from validacoes import Validador
from data_base import DataBase
from interface import Acessorio
from .motores import DoacaoReciclagem
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.align import Align
from rich import box

console = Console()

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
                Historico.atualizar_status_item(meus_itens, user_logado)
            elif resposta_menu == '2':
                Historico.deletar_item(meus_itens, user_logado.Whatsapp, user_logado)
    
    @staticmethod
    def exibir_historico(user_logado):    
        """
        -> Mostra o histórico do usuário
        :param user_logado: (obj) Objeto que representa os dados do usuário 
        """ 
        Acessorio.limpar_tela()
        contato_user = user_logado.Whatsapp
        meus_itens = DataBase.buscar_itens_por_usuario(contato_user)
        if not meus_itens:
            conteudo_vazio = (
                "[bold]Você não possui nenhum item cadastrado.[/bold]\n\n"
                "Cadastre um item e volte aqui novamente!"
            )
            painel_vazio = Panel(
                conteudo_vazio,
                title="[bold]SEU HISTÓRICO[/bold]",
                border_style="dim",
                width=70,
                justify="center"
            )
            console.print(Align.center(painel_vazio))
            print()
            sair = Validador.aguardar_retorno()
            if sair:
                return
            return           
        tabela = Table(
            title="[bold]SEU HISTÓRICO DE CADASTROS[/bold]",
            box=box.ROUNDED,
            width=85,
            show_header=True,
            header_style="bold",
            show_lines=True  
        )
        tabela.add_column("ID", justify="center", width=6)
        tabela.add_column("Data", justify="center", width=12)
        tabela.add_column("Tipo", justify="center", width=10)
        tabela.add_column("Status", justify="center", width=14)
        tabela.add_column("Categoria", justify="left")
        tabela.add_column("Local", justify="left")
        for item in meus_itens:
            data = item.get("data_cadastro", "00/00/00")
            tipo = "Achei" if item["tipo_registro"] == "Achado" else "Perdi"          
            if item["resolvido"]:
                status_texto = 'RESOLVIDO'
            elif item.get("liberado"):
                status_texto = 'P/ DOAÇÃO'  
            else:
                status_texto = 'ATIVO'              
            id_formatado = f"{item['id']:02d}"           
            tabela.add_row(
                id_formatado, 
                data, 
                tipo, 
                status_texto, 
                item["categoria"], 
                item["local"]
            )
        console.print(Align.center(tabela))
        print("\n") 
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
    def atualizar_status_item(meus_itens, user_logado):
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
                    item_selecionado = next((i for i in meus_itens if i["id"] == escolher_id), None)
                    categoria_nome = item_selecionado.get("categoria", "Item")
                    from central_notificacoes.notificacoes import Notificacoes
                    Notificacoes.criar_notificacao(
                        dono_id=user_logado.nome, 
                        tipo="HISTORICO",         
                        mensagem=f"Você marcou com sucesso o item da categoria '{categoria_nome}' (ID: #{escolher_id}) como RESOLVIDO."
                    )
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
    def deletar_item(meus_itens, contato_usuario, user_logado):
        """ 
        -> Gerencia a deleção de um item 
        :param meus_itens: (list) Lista de itens cadastrados pelo usuário
        :param contato_usuario: (str) Contato (WhatsApp) do usuário
        """
        import itens
        while True:
            certeza = Acessorio.tentar_novamente(mensagem = 'Deseja realmente deletar seu item?[S/N] ')
            if certeza == 'S':
                identidade = Validador.confirmar_identidade(user_logado)
                if identidade == True:
                    escolher_id = Validador.validar_id(mensagem='Digite o ID do item que deseja deletar: ')
                    if any(i["id"] == escolher_id for i in meus_itens):
                        item_selecionado = next(i for i in meus_itens if i["id"] == escolher_id)
                        categoria_nome = item_selecionado.get("categoria", "Item")
                        if itens.DeletarItem.processar_delecao_item(escolher_id, contato_usuario):
                            print('\033[0;32mItem deletado com sucesso!\033[m')
                            from central_notificacoes import Notificacoes
                            Notificacoes.criar_notificacao(
                                dono_id=user_logado.nome,  
                                tipo="HISTORICO",
                                mensagem=f"Você removeu com sucesso o item da categoria {categoria_nome} (ID: #{escolher_id}) do sistema."
                                )
                            sair = Validador.aguardar_retorno()
                            if sair:
                                return
                        else:
                            print('\033[0;31mErro ao deletar. Tente novamente mais tarde.\033[m')
                        voltar = input('\nDigite 0 para voltar: ')
                        Acessorio.verificar_escape(voltar)
                        break
                    else:
                        print('\033[0;31mEste ID não existe ou não pertence a você.\033[m')
                        tentar = Acessorio.tentar_novamente(mensagem='Deseja tentar novamente com outro ID?[S/N] ')
                        if tentar == 'S':
                            continue
                        else:
                            break
                else:
                    print('\033[0;31mIdentidade não confirmada.\033[m')
                    continuar = Acessorio.tentar_novamente(mensagem='Deseja tentar confirmar sua identidade novamente?[S/N] ')
                    if continuar == 'S':
                        continue
                    elif continuar == 'N':
                        Acessorio.limpar_tela()
                        return None