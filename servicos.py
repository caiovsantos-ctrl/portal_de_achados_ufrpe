import os, json, interface, itens, textwrap, validacoes, data_base
from datetime import datetime


def motor_de_buscas(item_cadastrado):
    nome_arquivo = 'itens.json'
    matches = []
    postagem_duplicada = False
    if not os.path.exists(nome_arquivo):
        return matches, postagem_duplicada
    with open(nome_arquivo, 'r', encoding='utf-8') as file:
        todos_itens = json.load(file)
    palavras_chaves = [p for p in item_cadastrado["descricao"].lower().split() if len(p) > 2]
    for item_banco in todos_itens:
        if item_banco["contato"] == item_cadastrado["contato"]:
            if item_banco["categoria"] == item_cadastrado["categoria"] and \
               item_banco["local"] == item_cadastrado["local"]:
                postagem_duplicada = True
            continue
        if item_banco["tipo_registro"] != item_cadastrado["tipo_registro"] and not item_cadastrado["resolvido"]:
            if item_banco["local"] == item_cadastrado["local"] and item_banco["categoria"] == item_cadastrado["categoria"]:
                descricao_salva = item_banco["descricao"].lower()
                palavras_encontradas = 0
                for palavra in palavras_chaves:
                    if palavra in descricao_salva:
                        palavras_encontradas += 1
                if len(palavra) > 2 and palavra in descricao_salva:
                    if palavras_encontradas >= 3:
                        matches.append(item_banco)
    return matches, postagem_duplicada     


def mural_historico(user_logado):
    while True:
        interface.limpar_tela()
        interface.exibir_menu_padrao('MURAL E RELATÓRIOS', [
                '[1] → Mural Geral (Itens Ativos)',
                '[2] → Histórico (Meus Itens)',
                '[3] → Mapa de Calor (Estatística)',
                '[0] → Voltar'
                ])
        resposta_menu = validacoes.verificar_resposta_menu(0, 3)
        if resposta_menu == '0':
            interface.verificar_escape(resposta_menu)
            return
        elif resposta_menu == '1':
            print('Mural Geral selecionado')
            mural_de_itens()
        elif resposta_menu == '2':
            print('Histórico selecionado')
            historico(user_logado)
        elif resposta_menu == '3':
            print('Mapa de Calor selecionado')
            mapa_de_calor()


def mural_de_itens():
    doacao_reciclagem()
    while True:
        interface.limpar_tela()
        print('Mural de Itens \n\n')
        todos_itens = data_base.buscar_todos_itens()
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
        sair = input('\nDigite 0 para voltar: ')
        if interface.verificar_escape(sair):
            break


def historico(user_logado):
    while True:
        doacao_reciclagem
        interface.limpar_tela()
        print('Seu Histórico:\n\n')
        meus_itens = data_base.buscar_itens_por_usuario(user_logado["Whatsapp"])
        if not meus_itens:
            print('Você não possui nenhum item cadastrado')
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
        print("\nO que deseja fazer?")
        print("1. Marcar item como resolvido")
        print("2. Deletar um item")
        print("0. Voltar")
        resposta_menu = validacoes.verificar_resposta_menu(0, 2)
        if resposta_menu == '0':
            interface.verificar_escape(resposta_menu)
            return
        if resposta_menu == '1':
            escolher_id = validacoes.validar_id(mensagem = 'Digite o ID do item que foi resolvido: ')
            if any(i["id"] == escolher_id for i in meus_itens):
                if itens.atualizar_status_item(escolher_id):
                    print('Status atualizado com sucesso!')
                else:
                    print('Erro ao atualizar. Tente novamente mais tarde')
                voltar = input('\nDigite 0 para voltar: ')
                interface.verificar_escape(voltar)
                return
            else:
                print('Este ID não existe ou não pertence a você')
                tentar = interface.tentar_novamente(mensagem = 'Deseja tentar novamente com outro ID?[S/N]')
                if tentar == 'S':
                    continue
                else:
                    return
        if resposta_menu == '2':
            id_deletar = validacoes.validar_id(mensagem = 'Digite o ID do item que você deseja deletar: ')            
            item_existe = any(i["id"] == id_deletar for i in meus_itens)
            if item_existe:
                print('\nAtenção! Você está prestes a deletar um item')
                tentar = interface.tentar_novamente(mensagem = 'Tem certeza que deseja deletar esse item?[S/N] ')
                if tentar == 'S':
                    if itens.deletar_item(id_deletar, user_logado["Whatsapp"]):
                        print('Item removido com sucesso')
                    else:
                        print('Erro ao deletar item. Tente novamente mais tarde')
                    voltar = input('\nDigite 0 para voltar: ')
                    interface.verificar_escape(voltar)
                    return
                else:
                    continue
            else:
                print('Este ID não existe ou não pertence a você')
                tentar = interface.tentar_novamente(mensagem = 'Deseja tentar novamente com outro ID?[S/N]')
                if tentar == 'S':
                    continue
                else:
                    return


def doacao_reciclagem():
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


def mapa_de_calor():
    interface.limpar_tela()
    print('Mapa de Calor: \n\n')
    todos_itens = data_base.buscar_todos_itens()
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
    sair = input('\nDigite 0 para voltar: ')
    if interface.verificar_escape(sair):
        return







