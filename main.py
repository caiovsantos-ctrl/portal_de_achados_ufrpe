import interface, validacoes, usuarios, itens, servicos
print('\n')
print('PORTAL DE ACHADOS UFRPPE'.center(50))
print('\n')
while True:
    interface.exibir_menu_padrao('MENU INICIAL', [
                '[1] → Cadastro',
                '[2] → Login'
                ])
    resposta_menu = validacoes.verificar_resposta_menu(1, 2)
    if resposta_menu == '1':
        usuarios.cadastrar_user()
    if resposta_menu == '2':
        user_logado = usuarios.login_user()
        if user_logado:
            while True:
                interface.limpar_tela()
                interface.exibir_menu_padrao('MENU 2', [
                '[1] → Gestão de itens',
                '[2] → Mural e Relatórios',
                '[3] → Configurações da conta',
                '[0] → Voltar'
                ])
                resposta_menu = validacoes.verificar_resposta_menu(0,3)
                if resposta_menu == '0':
                    interface.verificar_escape(resposta_menu)
                    interface.limpar_tela()
                    break
                elif resposta_menu == '1':
                    print('\033[0;32mGestão de itens selecionado\033[m')
                    itens.gestao_itens(user_logado)
                elif resposta_menu == '2':
                    print('\033[0;32mMural e relatório selecionado\033[m')
                    servicos.mural_historico(user_logado)
                elif resposta_menu == '3':
                    print('\033[0;32mConfigurações da conta selecionado\033[m')
                    interface.limpar_tela()
                    interface.exibir_menu_padrao('CONFIGURAÇÕES DA CONTA', [
                    '[1] → Atualizar Dados da Conta',
                    '[2] → Deletar Conta',
                    '[0] → Voltar'
                    ])
                    resposta_menu = validacoes.verificar_resposta_menu(0, 2)
                    if resposta_menu == '0':
                        interface.verificar_escape(resposta_menu)
                        interface.limpar_tela()
                    elif resposta_menu == '1':
                        usuarios.menu_atualizar_dados(user_logado)
                    elif resposta_menu == '2':
                        if usuarios.deletar_conta(user_logado):
                            user_logado = None
                            break
                if user_logado is None:
                    break


                    
    