import interface, validacoes, data_base, servicos, json, os


def menu_itens():
    categorias = [
        "Eletrônicos", "Chave", "Documentos", "Carteira", 
        "Materiais acadêmicos", "Vestuários", "Itens de alimentação"
    ]
    while True:
        interface.limpar_tela()
        opcoes_formatadas = [f"[{i}] → {nome}" for i, nome in enumerate(categorias, 1)]
        opcoes_formatadas.append("[0] → Voltar")
        interface.exibir_menu_padrao('CATEGORIA DO ITEM', opcoes_formatadas)
        resposta_menu = validacoes.verificar_resposta_menu(0, len(categorias))
        if resposta_menu == '0':
            interface.verificar_escape(resposta_menu)
            interface.limpar_tela()
            return None
        return categorias[int(resposta_menu) - 1]



def menu_local():
    locais = [
        "CEGOE", "Prédio Central", "CEAGRI", "RU", 
        "Biblioteca Central", "Depto. Biologia/ Química", 
        "Depto. Ed. Física", "Vizinhança"
    ]
    while True:
        interface.limpar_tela()
        opcoes_locais = [f"[{i}] → {local}" for i, local in enumerate(locais, 1)]
        opcoes_locais.append("[0] → Voltar")
        interface.exibir_menu_padrao("LOCAIS DA UFRPE", opcoes_locais, largura=60)
        resposta_local = validacoes.verificar_resposta_menu(0, len(locais))
        if resposta_local == '0':
            interface.verificar_escape(resposta_local)
            interface.limpar_tela()
            return None
        return locais[int(resposta_local) - 1]


def descricao_item():
    while True:
        interface.limpar_tela()
        print('Detalhes do item\n')
        print('Digite uma descrição detalhada: ')
        print('Ex.: Iphone com capinha branca e tela trincada\n')
        descricao = input('=> ')
        descricao = descricao.strip().capitalize()
        if descricao == '0':
            return None
        elif descricao == "":
            print('A descrição não pode ser vazia. Tente novamente.')
            continue
        elif len(descricao) < 10:
            print('A descricao deve conter pelo menos 10 caracteres. Tente novamente.')
            continue
        elif len(descricao) > 100:
            print('A descrição deve conter no máximo 100 caracteres. Tente novamente.')
            continue
        elif descricao.isnumeric():
            print('A descrição não pode conter apenas números. Tente novamente.')
            continue
        elif descricao == descricao[0] * len(descricao):
            print('A descrição não pode conter apenas dígitos iguais. Tente novamente')
            continue
        else:
            return descricao



def achar_perder_item(status, user_logado):
    interface.limpar_tela()
    resposta_item = menu_itens()
    if resposta_item is None:
        return None
    resposta_local = menu_local()
    if resposta_local is None:
        return None
    resposta_descricao = descricao_item()
    if resposta_descricao is None:
        return None
    return {
        "tipo_registro": status,
        "categoria": resposta_item,
        "local": resposta_local,
        "descricao": resposta_descricao,
        "resolvido": False,
        "contato": user_logado['Whatsapp'],
        "autor": user_logado['nome']
    }
            


def gestao_itens(user_logado):
    while True:
        match = None
        interface.limpar_tela()
        interface.exibir_menu_padrao('SITUAÇÃO DO ITEM', [
                '[1] → Achei Item',
                '[2] → Perdi Item',
                '[0] → Voltar'
                ])
        resposta_menu = validacoes.verificar_resposta_menu(0, 2)
        if resposta_menu == '0':
            interface.limpar_tela()
            return
        status = 'Achado' if resposta_menu == '1' else 'Perdido'
        while True:
            item_cadastrado = achar_perder_item(status, user_logado)
            if not item_cadastrado:
                return
            match, foi_duplicado = servicos.motor_de_buscas(item_cadastrado) 
            if foi_duplicado:
                print('\nVocê já possui um item similar cadastrado por você')
                print('O sistema não mostra seus próprios itens no Match para evitar confusão\n')
                if interface.tentar_novamente():
                    continue
                else:
                    item_cadastrado = None
                    break
            else:
                if item_cadastrado:
                    data_base.salvar_item(item_cadastrado)
                    print('Item cadastrado com sucesso!')
                    break
        if match:
            if status == 'Perdido':
                print('\nBoas notícias! Alguém pode ter encontrado seu item:\n')
            else:
                print('Atenção! Alguém perdeu um item parecido com este:\n')
            for m in match:
                print(f'ID: {m["id"]} | {m["categoria"]} no(a) {m["local"]}')
                print(f'Descrição: {m["descricao"]}')
                print(f'Contato: {m["contato"]}  {m["autor"]}')
            if status == 'Perdido':
                print('\nChame no Whatsapp agora para combinar a retirada')
            else:
                print('\nFique atento ao seu Whatsapp, o dono pode te procurar')
            confirmar = interface.tentar_novamente(mensagem = '\nSeu problema foi resolvido?[S/N]')
            if confirmar == 'S':
                if atualizar_status_item(item_cadastrado["id"]):
                    print('Ótima notícia! Item marcado como resolvido')
                else:
                    print('Erro ao atualizar status')
            else:
                print('Entendido! Seu item continuará ativo no mural para novos matches')
            sair = input('\nDigite 0 para voltar: ')
            interface.verificar_escape(sair)
        else:
            print('Nenhum match imediato, veja o mural de itens')
            sair = input('\nDigite 0 para voltar: ')
            interface.verificar_escape(sair)
            return


def atualizar_status_item(id_item):
    nome_arquivo = 'itens.json'
    if not os.path.exists(nome_arquivo):
        return False
    with open(nome_arquivo, 'r', encoding='utf-8') as arquivo:
        meus_itens = json.load(arquivo)
    alterado = False
    for item in meus_itens:
        if item["id"] == id_item:
            item["resolvido"] = True
            alterado = True
            break
    if alterado:
        with open(nome_arquivo, 'w', encoding='utf-8') as arquivo:
            json.dump(meus_itens, arquivo, indent=4, ensure_ascii=False)
        return True
    return False


def deletar_item(id_item, contato_usuario):
    nome_arquivo = 'itens.json'
    if not os.path.exists(nome_arquivo):
        return False
    with open(nome_arquivo, 'r', encoding='utf-8') as file:
        todos_itens = json.load(file)
    nova_lista = [
        item for  item in todos_itens
        if not (int(item["id"]) == int(id_item) and item["contato"] == contato_usuario)
    ]
    if len(nova_lista) < len(todos_itens):
        with open(nome_arquivo, 'w', encoding='utf-8') as file:
            json.dump(nova_lista, file, indent=4, ensure_ascii=False)
        return True
    return False