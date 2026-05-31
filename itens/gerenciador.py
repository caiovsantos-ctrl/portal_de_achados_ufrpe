import json, os, textwrap
from interface import Acessorio
from validacoes import Validador
from data_base import DataBase
from servicos import MotorDeBusca, Recibo
from .coleta import ColetarDadosItens
from .modelo import Item


class CadastrarItem:
    @staticmethod
    def menu_cadastro_itens(user_logado):
         """
         -> Mostra o menu para cadastrar o item 
        :param user_logado: (obj) Objeto que representa o usuário logado 
         """
         while True:
            match = None
            Acessorio.limpar_tela()
            Acessorio.exibir_menu_padrao('SITUAÇÃO DO ITEM', [
                    '[1] → Achei Item',
                    '[2] → Perdi Item',
                    '[0] → Voltar'
                    ])
            resposta_menu = Validador.verificar_resposta_menu(0, 2)
            if resposta_menu == '0':
                Acessorio.limpar_tela()
                return
            status = 'Achado' if resposta_menu == '1' else 'Perdido'
            CadastrarItem._processar_cadastro_item(status, user_logado)

    @staticmethod
    def _processar_cadastro_item(status, user_logado):
        """
        -> Centraliza o processo de cadastrar o item, verifica se o item
           é duplicado e processa os matches encontrados
        :param user_logado: (obj) Objeto que representa o usuário logado 
        :param status: (str) Define o tipo de registro do item(achado ou perdido)
        """
        while True:
            item_cadastrado = CadastrarItem._coletar_item_completo(status, user_logado)
            if not item_cadastrado:
                return
            match, foi_duplicado = MotorDeBusca.buscar_matches(item_cadastrado)
            if foi_duplicado:
                print('\n\033[0;31mVocê já possui um item similar cadastrado por você\033[m')
                print('O sistema não mostra seus próprios itens no Match para evitar confusão\n')
                if Acessorio.tentar_novamente():
                    continue
                else:
                    item_cadastrado = None
                    break
            else:
                if item_cadastrado:
                    from central_notificacoes import Notificacoes
                    dict_retorno = DataBase.salvar_item(item_cadastrado)
                    item_cadastrado.id_item = dict_retorno["id"]
                    print('\033[0;32mItem cadastrado com sucesso!\033[m')
                    Notificacoes.criar_notificacao(
                        dono_id=item_cadastrado.autor,  
                        tipo="CONFIRMAÇÃO",
                        mensagem=f'Você cadastrou um item ({item_cadastrado.categoria}) no(a) {item_cadastrado.local}'
                    )
                    break
        if item_cadastrado and match:
            from central_notificacoes import Notificacoes 
            for m in match:
                Notificacoes.criar_notificacao(
                    dono_id=m["autor"],
                    tipo="MATCH",
                    mensagem=f"O usuário {item_cadastrado.autor} cadastrou um item ({item_cadastrado.categoria}) no(a) {item_cadastrado.local} que coincide com o seu!"
                )
            CadastrarItem._processar_matches_encontrados(match, status, item_cadastrado)
        else:
            if item_cadastrado:
                print('Nenhum match imediato, veja o mural de itens')
                sair = input('\nDigite 0 para voltar: ')
                Acessorio.verificar_escape(sair)
            return


    @staticmethod
    def _coletar_item_completo(status, user_logado):
        """
        -> Armazena no JSON os dados dos itens cadastrados
        :param status: (str) Define o tipo de registro do item(achado ou perdido)
        :param user_logado: (obj) Objeto que representa o usuário logado
        :return: (obj/None)  Retorna o objeto que representa o item ou
                 None se o usuário desistiu em alguma parte
        """
        Acessorio.limpar_tela()
        resposta_item = ColetarDadosItens.menu_categoria_itens()
        if resposta_item is None:
            return None
        resposta_local = ColetarDadosItens.menu_local_itens()
        if resposta_local is None:
            return None
        resposta_descricao = ColetarDadosItens.descricao_item()
        if resposta_descricao is None:
            return None
        contato_user = user_logado.Whatsapp
        autor_user = user_logado.nome
        return Item(
            tipo_registro=status,
            categoria=resposta_item,
            local=resposta_local,
            descricao=resposta_descricao,
            resolvido=False,
            contato=contato_user,
            autor=autor_user
        )
    
    @staticmethod
    def _processar_matches_encontrados(match, status, item_cadastrado):
        """
        -> Mostra os matches encontrados para o item cadastrado e pergunta se o problema foi
           resolvido para atualizar o status do item
        :param match: (list) Lista de dicionários com os dados dos matches encontrados
        :param status: (str) Define o tipo de registro do item(achado ou perdido)
        :param item_cadastrado: (obj) Objeto que representa o item cadastrado
        """
        if status == 'Perdido':
            print('\n\033[0;32mBoas notícias! Alguém pode ter encontrado seu item:\033[m\n\n')
        else:
            print('\033[0;32mAtenção! Alguém perdeu um item parecido com este:\033[m\n\n')          
        for m in match:
            contato_formatado = m.get("contato") or "Não informado"
            autor_formatado = m.get("autor") or "Anônimo"
            desc_formatada = m.get("descricao") or "Sem descrição adicional."
            texto_desc = desc_formatada
            desc_formatar = textwrap.fill(
                        texto_desc,
                        width=46,
                        subsequent_indent='                '
                    )
            print('=' * 60)
            print(f'\033[1mMATCH ENCONTRADO - ID: {m["id"]:02d}\033[m'.center(60))
            print('─' * 60)
            print(f'    \033[1mItem:\033[m      {m["categoria"]} no(a) {m["local"]}')
            print(f'    \033[1mDescrição:\033[m {desc_formatar}')
            print(f'    \033[1mAutor:\033[m     {autor_formatado}')
            print(f'    \033[1mContato:\033[m   {contato_formatado}')
            print('─' * 60)
            print('    \033[3mChame no Whatsapp agora para combinar a retirada!\033[m')
            print('=' * 60)
            confirmar = Acessorio.tentar_novamente(mensagem='\nEste item resolveu seu problema? [S/N] ')
            if confirmar == 'S':
                id_match = int(m["id"])
                id_meu = item_cadastrado.id_item
                if AtualizarStatusItem.processar_atualizacao_item(id_match):
                    AtualizarStatusItem.processar_atualizacao_item(id_meu)
                    print('\033[0;32mÓtima notícia! Os itens foram marcados como resolvidos.\033[m')
                    from central_notificacoes import Notificacoes
                    Notificacoes.criar_notificacao(
                        dono_id=m["autor"],
                        tipo="SUCESSO",
                        mensagem=f"Seu item ({m['categoria']}) foi marcado como devolvido/resolvido com sucesso em conjunto com {item_cadastrado.autor}!"
                    )
                    dados_do_recibo = {
                        "categoria": m.get("categoria", "Não informada"),
                        "local": m.get("local", "Não informado"),
                        "descricao": desc_formatada,
                        "data_cadastro": m.get("data_cadastro", "00/00/0000"),
                        "autor": autor_formatado,
                        "contato": contato_formatado
                    }
                    Recibo.gerar_pdf(id_match, dados_do_recibo)
                else:
                    print('\033[0;31mErro ao atualizar status dos itens.\033[m')
                sai = Validador.aguardar_retorno()
                if sai:
                    return
            else:
                print('\nEntendido! Vamos verificar o próximo item (se houver)...\n')
        print('\nSeu item continuará ativo no mural para novos matches.')
        sair = Validador.aguardar_retorno()
        if sair:
            return
    

class AtualizarStatusItem:
    """ Gerencia o processo de atualizar o status do item para resolvido """
    @staticmethod      
    def processar_atualizacao_item(id_item):
        """
        -> Realiza a atualização do status do item
        :param id_item: (int) Id específico do item 
        :return: (bool) Retorna True se atualizou o status ou False se não 
        """
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
    

class DeletarItem:
    """ Gerencia o processo de deletar um item """
    @staticmethod
    def processar_delecao_item(id_item, contato_usuario):
        """
        -> Realiza a deleção do item
        :param id_item: (int) Id específico do item 
        :param contato_usuario: (str) N° do whatsapp do usuário
        :return: (bool) Retorna True se deletou o item ou False se não 
        """
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