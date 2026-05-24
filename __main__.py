from interface import Acessorio
from validacoes import Validador
from usuarios import GerenciadorUsuario
from itens import GerenciadorItens
from servicos import GerenciadorServicos


class SistemaPortal:
    def __init__(self):
        self.gerenciador_usuario = GerenciadorUsuario()
    def executar(self):
        print('\n')
        print('PORTAL DE ACHADOS UFRPPE'.center(50))
        print('\n')
        while True:
            Acessorio.exibir_menu_padrao('MENU INICIAL', [
                    '[1] → Cadastro',
                    '[2] → Login'
                    ])
            resposta_menu = Validador.verificar_resposta_menu(1, 2)
            if resposta_menu == '1':
                self.gerenciador_usuario.cadastrar_user()
            if resposta_menu == '2':
                user_logado = self.gerenciador_usuario.login_user()
                if user_logado:
                    self.menu_principal(user_logado)

    def menu_principal(self, user_logado):
        gerenciador_itens = GerenciadorItens()
        while True:
            Acessorio.limpar_tela()
            Acessorio.exibir_menu_padrao('MENU 2', [
            '[1] → Gestão de itens',
            '[2] → Mural e Relatórios',
            '[3] → Configurações da conta',
            '[0] → Voltar'
            ])
            resposta_menu = Validador.verificar_resposta_menu(0,3)
            if resposta_menu == '0':
                Acessorio.verificar_escape(resposta_menu)
                Acessorio.limpar_tela()
                break
            elif resposta_menu == '1':
                print('\033[0;32mGestão de itens selecionado\033[m')
                gerenciador_itens.gestao_itens(user_logado)
            elif resposta_menu == '2':
                print('\033[0;32mMural e relatório selecionado\033[m')
                GerenciadorServicos.mural_historico(user_logado)
            elif resposta_menu == '3':
                print('\033[0;32mConfigurações da conta selecionado\033[m')
                Acessorio.limpar_tela()
                Acessorio.exibir_menu_padrao('CONFIGURAÇÕES DA CONTA', [
                '[1] → Atualizar Dados da Conta',
                '[2] → Deletar Conta',
                '[0] → Voltar'
                ])
                resposta_menu = Validador.verificar_resposta_menu(0, 2)
                if resposta_menu == '0':
                    Acessorio.verificar_escape(resposta_menu)
                    Acessorio.limpar_tela()
                elif resposta_menu == '1':
                    self.gerenciador_usuario.menu_atualizar_dados(user_logado)
                elif resposta_menu == '2':
                    if self.gerenciador_usuario.deletar_conta(user_logado):
                        user_logado = None
                        break
            if user_logado is None:
                break


if __name__ == "__main__":
    sistema = SistemaPortal()
    sistema.executar()