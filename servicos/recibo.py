import os, platform, subprocess
from fpdf import FPDF
from interface import Acessorio


class Recibo:
    """ Gerencia a criação e exibição do recibo"""
    @staticmethod
    def gerar_pdf(item_id, dados_match):
        """ Cria o recibo em formato PDF e, se o usuário quiser, exibe-o """
        if not os.path.exists('recibos'):
            os.makedirs('recibos')
        caminho_salvar = f'recibos/recibo_match_{item_id}.pdf'
        pdf = FPDF(orientation='P', unit='mm', format='A4')
        pdf.set_margins(20, 20, 20)
        pdf.add_page()
        pdf.set_fill_color(0, 102, 51)
        pdf.rect(20, 20, 170, 25, style='F')
        pdf.set_font('Helvetica', 'B', 18)
        pdf.set_text_color(255, 255, 255)
        pdf.set_y(24)
        pdf.cell(170, 8, 'UFRPE', ln=True, align='C')
        pdf.set_font('Helvetica', '', 10)
        pdf.cell(170, 5, 'PORTAL DE ACHADOS UFRPE - COMPROVANTE DE MATCH', ln=True, align='C')
        pdf.set_y(50)
        pdf.set_text_color(51, 51, 51)
        pdf.set_font('Helvetica', 'B', 12)
        pdf.set_text_color(0, 102, 51)
        pdf.cell(170, 6, 'INFORMAÇÕES DO ITEM', ln=True)
        pdf.line(20, pdf.get_y() + 1, 190, pdf.get_y() + 1)
        pdf.ln(4)
        pdf.set_text_color(51, 51, 51)
        pdf.set_font('Helvetica', 'B', 10)
        pdf.cell(40, 7, 'Código do Item:')
        pdf.set_font('Helvetica', '', 10)
        pdf.cell(130, 7, f'#{item_id}', ln=True)
        pdf.set_font('Helvetica', 'B', 10)
        pdf.cell(40, 7, 'Categoria:')
        pdf.set_font('Helvetica', '', 10)
        pdf.cell(130, 7, dados_match.get('categoria', 'Não Informada'), ln=True)
        pdf.set_font('Helvetica', 'B', 10)
        pdf.cell(40, 7, 'Descrição:')
        pdf.set_font('Helvetica', '', 10)
        pdf.cell(130, 7, dados_match.get('descricao', 'Não Informada'), ln=True)
        pdf.set_font('Helvetica', 'B', 10)
        pdf.cell(40, 7, 'Local:')
        pdf.set_font('Helvetica', '', 10)
        pdf.cell(130, 7, dados_match.get('local', 'Não Informado'), ln=True)
        pdf.ln(6)
        pdf.set_font('Helvetica', 'B', 12)
        pdf.set_text_color(0, 102, 51)
        pdf.cell(170, 6, 'DADOS DE RETIRADA E CONTATO', ln=True)
        pdf.line(20, pdf.get_y() + 1, 190, pdf.get_y() + 1)
        pdf.ln(4)
        pdf.set_text_color(51, 51, 51)
        pdf.set_font('Helvetica', 'B', 10)
        pdf.cell(40, 7, 'Data de Cadastro:')
        pdf.set_font('Helvetica', '', 10)
        pdf.cell(130, 7, dados_match.get('data_cadastro', 'Não Informada'), ln=True)
        pdf.set_font('Helvetica', 'B', 10)
        pdf.cell(40, 7, 'Quem Encontrou:')
        pdf.set_font('Helvetica', '', 10)
        pdf.cell(130, 7, dados_match.get('autor', 'Anônimo'), ln=True)
        pdf.set_font('Helvetica', 'B', 10)
        pdf.cell(40, 7, 'Contato para Retirada:')
        pdf.set_font('Helvetica', '', 10)
        pdf.cell(130, 7, dados_match.get('contato', 'Não Informado'), ln=True)
        pdf.ln(10)
        pdf.set_fill_color(242, 248, 242)
        pdf.rect(20, pdf.get_y(), 170, 22, style='F')
        pdf.set_fill_color(0, 102, 51)
        pdf.rect(20, pdf.get_y(), 1.5, 22, style='F')
        pdf.set_y(pdf.get_y() + 3)
        pdf.set_x(25)
        pdf.set_font('Helvetica', 'B', 9.5)
        pdf.set_text_color(35, 82, 37)
        pdf.cell(160, 5, 'Instruções para Retirada:', ln=True)
        pdf.set_x(25)
        pdf.set_font('Helvetica', '', 9)
        pdf.multi_cell(155, 4.5, 'Apresente este documento no local combinado para liberação oficial do item')
        pdf.set_y(240)
        pdf.set_font('Helvetica', '', 8)
        pdf.set_text_color(119, 119, 119)
        pdf.cell(170, 4, 'CÓDIGO DE AUTENTICAÇÃO INTERNA:', ln=True, align='C')
        pdf.set_font('Courier', 'B', 11)
        pdf.set_text_color(68, 68, 68)
        pdf.cell(170, 6, f'MATCH-UFRPE-{item_id:04d}-A9F4', ln=True, align='C')
        pdf.output(caminho_salvar)
        caminho_completo = os.path.abspath(caminho_salvar)
        diretorio = os.path.dirname(caminho_completo)
        print(f'\n\033[0;32m[+] Recibo PDF gerado com sucesso\033[m')
        certeza = Acessorio.tentar_novamente('Deseja visualizá-lo?[S/N] ')
        if certeza == 'S':
            print("Abrindo a pasta com o arquivo selecionado para você...")
            try:
                if platform.system() == 'Windows':
                    subprocess.run(f'explorer /select,"{caminho_completo}"')
                elif platform.system() == "Darwin":
                    subprocess.run(["open", "-R", caminho_completo])
                else:
                    subprocess.run("xdg-open", diretorio)
                from central_notificacoes import Notificacoes
                categoria_item = dados_match.get('categoria', 'Item')
                parceiro_match = dados_match.get('autor', 'outro usuário')
                Notificacoes.criar_notificacao(
                    dono_id=parceiro_match, 
                    tipo="HISTORICO",
                    mensagem=f"Você visualizou e abriu com sucesso o recibo em PDF do Match da categoria '{categoria_item}'."
                )
            except Exception:
                print(f"O PDF está salvo na pasta: {caminho_completo}")
        else:
            print(f"O PDF está salvo na pasta: {caminho_completo}")


