from time import sleep
from interface import Acessorio
from validacoes import Validador
from data_base import DataBase


class AtualizarDadosUsuario:
    """ Gerencia todo o processo de atualização de dados do usuário """
    @staticmethod
    def menu_atualizar_dados(user_logado):
        """
        -> Mostra o menu de atualizar dados e direciona o usuário de acordo com a opção
        :param user_logado: (obj) Objeto que representa o usuário logado
        """ 
        print('\033[0;32mAtualizar dados pessoais selecionado\033[m')
        while True:
            Acessorio.limpar_tela()
            Acessorio.exibir_menu_padrao('ATUALIZAR DADOS PESSOAIS', [
                    '[1] → Atualizar Nome',
                    '[2] → Atualizar Email',
                    '[3] → Atualizar Senha',
                    '[4] → Atualizar Whatsapp',
                    '[0] → Voltar'
                    ])
            resposta_menu = Validador.verificar_resposta_menu(0, 4)
            if resposta_menu == '0':
                Acessorio.verificar_escape(resposta_menu)
                Acessorio.limpar_tela()
                return
            elif resposta_menu == '1':
                AtualizarDadosUsuario._processar_mudanca(user_logado, "nome", Validador.validar_nome)
            elif resposta_menu == '2':
                AtualizarDadosUsuario._processar_mudanca(user_logado, "email", Validador.validar_email)
            elif resposta_menu == '3':
                AtualizarDadosUsuario._processar_mudanca(user_logado, "senha", Validador.validar_senha)
            elif resposta_menu == '4':
                AtualizarDadosUsuario._processar_mudanca(user_logado, "Whatsapp", Validador.validar_zap)

    @staticmethod
    def _processar_mudanca(user_logado, campo, funcao_validacao):
        """
        Valida a identidade e altera o campo escolhido no objeto
        :param user_logado: (obj) Objeto que representa o usuário logado
        :param campo: (str) O dado que o usuário deseja atualizar
        :param funcao_validacao: (function) Função que será substituída pelo campo desejado
        """
        print(f'\033[0;32mAtualizar {campo} selecionado\033[m')
        while True:
            if Validador.confirmar_identidade(user_logado):
                    novo_valor = funcao_validacao()
                    if novo_valor == getattr(user_logado, campo):
                        print(f'{campo} informado(a) é igual ao(à) atual')
                        tentar_atualizar = Acessorio.tentar_novamente(mensagem=f'Deseja tentar atualizar o {campo} novamente?[S/N] ')
                        if tentar_atualizar == 'N':
                            break
                        else:
                            continue
                    if DataBase.salvar_no_json(user_logado.email, campo, novo_valor):
                        setattr(user_logado, campo, novo_valor)
                        from central_notificacoes.notificacoes import Notificacoes
                        Notificacoes.criar_notificacao(
                            dono_id=user_logado.nome,  
                            tipo="HISTORICO",
                            mensagem=f"Você alterou com sucesso o seu dado de perfil: '{campo}' no sistema."
                        )
                        break
                    else:
                        tentar = Acessorio.tentar_novamente(mensagem=f'Deseja tentar atualizar o {campo} novamente?[S/N] ')
                        if tentar == 'N':
                            break
                        else:
                            continue
            else:
                print('Identidade não confirmada')
                continuar = Acessorio.tentar_novamente(mensagem='Deseja tentar confirmar sua identidade novamente?[S/N] ')
                if continuar == 'S':
                    continue
                elif continuar == 'N':
                    Acessorio.limpar_tela()
                    return None

    
class DeletarContaUsuario:
    """ Gerencia todo o processo de deletar conta do usuário """
    @staticmethod
    def executar_delecao(user_logado):
        """
        -> Realiza a deleção da conta
        :param user_logado: (obj) Objeto que representa o usuário logado
        :return: (bool) Retorna True se ocorreu a conta foi deletada ou False se deu errado 
        """
        print('\033[0;32mDeletar conta selecionado\033[m')
        while True:
            Acessorio.limpar_tela()
            print('ATENÇÃO: Essa ação é irreversível!')
            certeza = Acessorio.tentar_novamente(mensagem = 'Deseja realmente deletar sua conta?[S/N] ')
            if certeza == 'S':
                identidade = Validador.confirmar_identidade(user_logado)
                if identidade == True:
                    sucesso = DataBase.deletar_no_json(user_logado)
                    if sucesso:
                        print('\n\033[0;32mConta deletada com sucesso. Sentiremos sua falta!\033[m')
                        sleep(1)
                        Acessorio.limpar_tela()
                        return True
                    else:
                        print('\033[0;31mOcorreu um erro. Tente novamente mais tarde\033[m')
                        return False
                else:
                    print('\033[0;31mIdentidade não confirmada.\033[m')
                    continuar = Acessorio.tentar_novamente(mensagem='Deseja tentar confirmar sua identidade novamente?[S/N] ')
                    if continuar == 'S':
                        continue
                    elif continuar == 'N':
                        Acessorio.limpar_tela()
                        return False