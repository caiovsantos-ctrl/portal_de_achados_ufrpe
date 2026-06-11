import os, json
from validacoes import Validador
from data_base import DataBase
from interface import Acessorio
from .motores import DoacaoReciclagem
from .historico import Historico
from datetime import datetime, timedelta
from rich.console import Console, Group
from rich.panel import Panel
from rich.table import Table
from rich import box
from rich.align import Align
from rich.rule import Rule

console = Console()


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
                    '[2] → Mapa de Calor (Foco de Alerta)',
                    '[3] → Painel de Impacto (Estatísticas)', 
                    '[4] → Histórico (Meus Itens)',
                    '[0] → Voltar'
                    ])
            resposta_menu = Validador.verificar_resposta_menu(0, 4)
            if resposta_menu == '0':
                Acessorio.verificar_escape(resposta_menu)
                return
            elif resposta_menu == '1':
                print('\033[0;32mMural Geral selecionado\033[m')
                MuralDeItens.menu_mural()
            elif resposta_menu == '2':
                print('\033[0;32mMapa de Calor selecionado\033[m')
                MapaDeCalor.exibir_mapa_de_calor()
            elif resposta_menu == '3':
                print('\033[0;32mPainel de Impacto selecionado\033[m')
                PainelImpacto.exibir_painel()
            elif resposta_menu == '4':
                print('\033[0;32mHistórico selecionado\033[m')
                Historico.menu_historico(user_logado)


class MuralDeItens:
    """ Gerencia a exibição do mural de itens  """
    @staticmethod
    def menu_mural():
        """ Mostra os filtros do mural e direciona o usuário de acordo com sua opção"""
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
        titulo = 'MURAL DE ITENS'
        if filtro_cat:
            titulo += f' - Categoria: {filtro_cat}'
        if filtro_loc:
            titulo += f' - Local: {filtro_loc}'
        console.rule(f"[bold]{titulo}[/bold]", characters="=")
        print()
        todos_itens = DataBase.buscar_todos_itens()
        itens_ativos = [i for i in todos_itens if not i.get("resolvido", False)]
        if filtro_cat:
            itens_ativos = [i for i in itens_ativos if i.get("categoria") == filtro_cat]
        if filtro_loc:
            itens_ativos = [i for i in itens_ativos if i.get("local") == filtro_loc]
        if not itens_ativos:
            painel_vazio = Panel("O Mural está vazio no momento.", border_style="dim", width=70)
            console.print(painel_vazio)
        else:
            for item in itens_ativos:
                tipo_bruto = item["tipo_registro"]
                liberado = item.get("liberado", False)
                tipo = 'Achei' if tipo_bruto == 'Achado' else 'Perdi'
                data = item.get("data_cadastro", '00/00/0000')
                if tipo_bruto == 'Achado':
                    if liberado:
                        texto_desc = f'Item liberado para doação/reciclagem: {item["descricao"]}'
                    else:
                        texto_desc = 'Para manter a transparência, a descrição está oculta'
                else:
                    texto_desc = item["descricao"]
                tabela_info = Table.grid(padding=(0, 1))
                tabela_info.add_column("Chave", style="bold", justify="right")
                tabela_info.add_column("Valor", justify="left", overflow="fold")               
                tabela_info.add_row("Postado por:", item.get("autor", "Usuário"))
                tabela_info.add_row("Categoria:", item["categoria"])
                tabela_info.add_row("Descrição:", texto_desc)
                tabela_info.add_row("Contato:", item["contato"])
                cabecalho = f"ID: {item['id']:02d} | {tipo} | {data} | {item['local']}"
                cartao = Panel(
                    tabela_info,
                    title=f"[bold]{cabecalho}[/bold]",
                    title_align="left",
                    box=box.ROUNDED,
                    width=70
                )
                console.print(cartao)
                print()         
        sair = Validador.aguardar_retorno()
        if sair:
            return


class MapaDeCalor:
    """ Gerencia a exibição do mapa de calor dos locais onde mais ocorrem registros """
    @staticmethod
    def exibir_mapa_de_calor():
        """ Mostra o mapa de calor dos itens """
        Acessorio.limpar_tela()
        todos_itens = DataBase.buscar_todos_itens()
        
        if not todos_itens:
            painel_vazio = Panel(
                "Não há dados suficientes para gerar o Mapa de Calor.", 
                border_style="dim", 
                width=70
            )
            console.print(Align.center(painel_vazio))
        else:
            tabela = Table(
                title="[bold]MAPA DE CALOR - INCIDÊNCIA POR LOCAL[/bold]",
                box=box.ROUNDED,
                width=70,
                show_header=True,
                header_style="bold"
            )
            tabela.add_column("Local", justify="left", style="bold")
            tabela.add_column("Intensidade (Frequência)", justify="left")
            tabela.add_column("Total", justify="right")
            contagem = {}
            for item in todos_itens:
                local = item.get("local", "Desconhecido")
                contagem[local] = contagem.get(local, 0) + 1                
            locais_ordenados = sorted(contagem.items(), key=lambda x: x[1], reverse=True)
            for local, total in locais_ordenados:
                barra = '■' * total
                tabela.add_row(local, barra, f"{total} itens")
            console.print(Align.center(tabela))           
        print()
        sair = Validador.aguardar_retorno()
        if sair:
            return
        

class PainelImpacto:
    """ 
    -> Gerencia o processo de criação e exibição do Painel de Impacto
    :return: (dict) Informações do Painel de Impacto
    """
    @staticmethod
    def obter_estatisticas():
        """ Realiza o cálculo das informações necessárias para exibir o mural"""
        arquivo = 'itens.json'
        relatorio = {
        "resolvidos_semana": 0,
        "resolvidos_mes": 0,
        "resolvidos_ano": 0,
        "geral_total": 0,
        "geral_devolvidos": 0,
        "geral_sustentaveis": 0,
        "geral_taxa_sucesso": 0.0,
        "geral_taxa_ecologica": 0.0,
        "total_cadastrados": 0
        }
        if not os.path.exists(arquivo):
            return relatorio
        try:
            with open(arquivo, 'r', encoding='utf-8') as file:
                itens = json.load(file)
            hoje = datetime.now().date()
            for item in itens:
                relatorio['total_cadastrados'] += 1
                e_devolvido = item.get('resolvido', False) and not item.get('liberado', False)
                e_sustentavel = item.get('liberado', False)
                if not (e_sustentavel or e_devolvido):
                    continue
                data_item = item.get('data_cadastro', '00/00/0000')
                try:
                    data_res = datetime.strptime(data_item, '%d/%m/%Y').date()
                except ValueError:
                    continue
                if hoje - timedelta(days=7) <= data_res <= hoje:
                    relatorio['resolvidos_semana'] += 1
                if data_res.month == hoje.month and data_res.year == hoje.year:
                    relatorio['resolvidos_mes'] += 1
                if data_res.year == hoje.year:
                    relatorio['resolvidos_ano'] += 1
                relatorio['geral_total'] += 1
                if e_sustentavel:
                    relatorio['geral_sustentaveis'] += 1
                else:
                    relatorio['geral_devolvidos'] += 1
            total_geral = relatorio['total_cadastrados']
            if total_geral > 0:
                relatorio['geral_taxa_sucesso'] = (relatorio['geral_devolvidos'] / total_geral) * 100
                relatorio['geral_taxa_ecologica'] = (relatorio['geral_sustentaveis'] / total_geral) * 100
            return relatorio
        except Exception:
            return relatorio

    @staticmethod    
    def exibir_painel():
        """ Exibe o Painel de Impacto"""
        Acessorio.limpar_tela()
        estatisticas = PainelImpacto.obter_estatisticas()
        def criar_sub_grid():
            grid = Table.grid(expand=True)
            grid.add_column("Rótulo", width=32, justify="left")
            grid.add_column("Dados", width=40, justify="right")
            return grid
        g1 = criar_sub_grid()
        g1.add_row("[bold dim]CASOS SOLUCIONADOS POR PERÍODO:[/bold dim]", "")
        g1.add_row("  ↳ Esta Semana", f"{estatisticas['resolvidos_semana']} itens")
        g1.add_row("  ↳ Este Mês", f"{estatisticas['resolvidos_mes']} itens")
        g1.add_row("  ↳ Este Ano", f"{estatisticas['resolvidos_ano']} itens")
        g2 = criar_sub_grid()
        g2.add_row("[bold dim]IMPACTO ACUMULADO DO PORTAL:[/bold dim]", "")
        g2.add_row("  ↳ Total de Itens Cadastrados", str(estatisticas['total_cadastrados']))
        g2.add_row("  ↳ Total de Itens Resolvidos", str(estatisticas['geral_total']))
        g3 = criar_sub_grid()
        g3.add_row("[bold dim]TAXAS DE SUCESSO E ECOLOGIA:[/bold dim]", "")        
        b_sucesso = '█' * int(estatisticas["geral_taxa_sucesso"] / 5)
        str_sucesso = f"Total: {estatisticas['geral_devolvidos']} | [{b_sucesso:<20}] {estatisticas['geral_taxa_sucesso']:.1f}%"
        g3.add_row("  ↳ Devoluções (Sucesso)", str_sucesso)        
        b_eco = '░' * int(estatisticas["geral_taxa_ecologica"] / 5)
        str_eco = f"Total: {estatisticas['geral_sustentaveis']} | [{b_eco:<20}] {estatisticas['geral_taxa_ecologica']:.1f}%"
        g3.add_row("  ↳ Doações/Reciclagem", str_eco)
        conteudo_painel = Group(
            g1,
            Rule(style="dim"),
            g2,
            Rule(style="dim"),
            g3
        )
        dashboard = Panel(
            conteudo_painel,
            title="[bold]PAINEL DE IMPACTO SOCIOAMBIENTAL[/bold]",
            box=box.ROUNDED,
            width=76
        )
        console.print(Align.center(dashboard))
        print()
        console.print(Align.center("[dim]Pequenas ações, grandes impactos no nosso campus![/dim]"))
        print("\n\n")       
        sair = Validador.aguardar_retorno()
        if sair:
            return







