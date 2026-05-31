import os, json, unicodedata
from datetime import datetime
from difflib import SequenceMatcher


class MotorDeBusca:
    """ Gerencia a lógica de busca e comparação de itens para
        encontrar possíveis matches entre achados e perdidos """
    @staticmethod
    def calcular_similaridade(texto1, texto2):
        """
        -> Calcula a similaridade entre dois textos
        :param texto1: (str) Primeiro texto para comparação
        :param texto2: (str) Segundo texto para comparação
        :return: (float) Similaridade entre os textos, variando de 0 a 1
        """
        return SequenceMatcher(None, texto1, texto2).ratio()
    
    @staticmethod
    def remover_acentos(texto):
        """
        -> Remove acentos de um texto para facilitar a comparação
        :param texto: (str) Texto do qual os acentos serão removidos
        :return: (str) Texto sem acentos
        """
        processado = unicodedata.normalize('NFD', texto)
        return ''.join([c for c in processado if unicodedata.category(c) != 'Mn'])
    
    @staticmethod
    def buscar_matches(item_cadastrado):
        """
        -> Procura um item recomendado para dar match
        :param item_cadastrado: (dict) Dicionário que guarda as informações do item
        :return: (list/bool) Retorna matches (lista com os itens que deu match) e 
        postagem_duplicada (True se o usuário cadastrou o mesmo item e False se não)
        """
        nome_arquivo = 'itens.json'
        matches = []
        postagem_duplicada = False
        if not os.path.exists(nome_arquivo):
            return matches, postagem_duplicada
        with open(nome_arquivo, 'r', encoding='utf-8') as file:
            todos_itens = json.load(file)
        descricao = item_cadastrado.descricao
        contato = item_cadastrado.contato
        categoria = item_cadastrado.categoria
        local = item_cadastrado.local
        tipo_registro = item_cadastrado.tipo_registro
        desc_limpa = MotorDeBusca.remover_acentos(descricao.lower())
        palavras_chaves = [p for p in desc_limpa.split() if len(p) > 2]
        for item_banco in todos_itens:
            if item_banco["contato"] == contato:
                if item_banco["categoria"] == categoria and \
                item_banco["local"] == local:
                    postagem_duplicada = True
                continue
            if item_banco["tipo_registro"] != tipo_registro and not item_banco["resolvido"]:
                if item_banco["local"] == local and item_banco["categoria"] == categoria:
                    desc_banco_limpa = MotorDeBusca.remover_acentos(item_banco["descricao"].lower())
                    descricao_salva = desc_banco_limpa.split()
                    palavras_encontradas = 0
                    for palavra in palavras_chaves:
                        match_na_palavra = False
                        for palavra_salva in descricao_salva:
                            if palavra == palavra_salva or MotorDeBusca.calcular_similaridade(palavra, palavra_salva) >= 0.8:
                                match_na_palavra = True
                                break
                        if match_na_palavra:
                            palavras_encontradas += 1
                    if palavras_encontradas >= 3:
                        matches.append(item_banco)
        return matches, postagem_duplicada  
    

class DoacaoReciclagem:
    """ Gerencia o processo de liberar um item para doação ou reciclagem após 30 dias do cadastro """
    @staticmethod
    def processar_temporalidade():
        """
        Transforma o status do item para 'Disponível para doação/reciclagem'
        se passou de 30 dias que foi cadastrado e não foi encontrado o dono
        """
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
                        from central_notificacoes.notificacoes import Notificacoes
                        Notificacoes.criar_notificacao(
                        dono_id=item["autor"],
                        tipo="PRAZO",
                        mensagem=f"O prazo de 30 dias para recuperar o seu item '{item['descricao']}' expirou. Ele foi encaminhado para doação/reciclagem da UFRPE."
                        )
                except:
                    continue
        if alterado:
            with open(arquivo, 'w', encoding='utf-8') as file:
                json.dump(lista_itens, file, indent=4, ensure_ascii=False)