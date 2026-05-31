import os, json
from google import genai
from .notificacoes import Notificacoes
from collections import Counter


API_KEY = os.getenv("GEMINI_API_KEY")


class AssistenteIA:
    @staticmethod
    def _analisar_itens_json():
        caminho = 'itens.json'
        total_doacao = 0
        ultimo_item_doacao = 'Nenhum'
        local_critico = 'Nenhum'
        if os.path.exists(caminho):
            with open(caminho, 'r', encoding='utf-8') as f:
                try:
                    itens = json.load(f)
                except json.JSONDecodeError:
                    itens = []
            itens_doacao = [i for i in itens if i.get('status_final') == 'Disponível para doação/reciclagem']
            total_doacao = len(itens_doacao)
            if total_doacao > 0:
                ultimo_item_doacao = itens_doacao[-1].get('descricao', 'Não Informada')
            locais = [i.get('local') for i in itens if i.get('local')]
            if locais:
                local_critico = Counter(locais).most_common(1)[0][0]
        return total_doacao, ultimo_item_doacao, local_critico

    @staticmethod
    def boas_vindas(dono_id):
        try:
            todas = Notificacoes.buscar_notificacoes(dono_id)
            nao_lidas = [n for n in todas if not n['lida']]
            if not nao_lidas:
                return f'Olá {dono_id}, você não possui nenhuma notificação nova hoje. Seu Quadro de Avisos está atualizado!'
            texto_notif = ''
            for n in nao_lidas:
                texto_notif += f"- Tipo: {n['tipo']} | Mensagem: {n['mensagem']} | Data: {n['data_criacao']}\n"
            total_doacao, ultimo_item_doacao, local_critico = AssistenteIA._analisar_itens_json()
            prompt = f"""
            Você é a Assistente Virtual do sistema de Achados e Perdidos da UFRPE (Universidade Federal Rural de Pernambuco).
            O usuário chamado {dono_id} acabou de fazer login no sistema.
            Sua tarefa: Escreva uma mensagem de boas-vindas curta, humanizada, amigável e direta (máximo 4 linhas).
            Resuma o que aconteceu, ex: 
            1. Abaixo estão as notificações brutas que ele recebeu enquanto estava offline.
            {texto_notif}
            2. ATUALIZAÇÃO DO MURAL GERAL:
            - Existem hoje {total_doacao} itens que foram movidos para o status de 'Doação/Reciclagem' porque ninguém os buscou no prazo.
            - O item mais recente enviado para doação foi um(a) '{ultimo_item_doacao}'.
            3. ALERTA DE SEGURANÇA (MAPA DE CALOR):
            - O local com maior número de ocorrências acumuladas no momento é o "{local_critico}".
            Diga a ele para dar uma olhada no Quadro de Avisos para ver os detalhes.
            Use emojis condizentes com o ambiente universitário ou mensagens.
            """
            client = genai.Client(api_key=API_KEY)
            resposta = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt,
            )
            return f'\n🤖 [Assistente UFRPE]:\n{resposta.text}'
        except Exception as e:
            return f'\n👋 Olá, {dono_id}! Bem-vindo de volta ao Portal de Achados e Perdidos da UFRPE. Confira suas notificações no menu correspondente.'