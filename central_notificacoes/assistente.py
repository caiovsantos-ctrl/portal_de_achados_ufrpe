import os, json
from google import genai
from .notificacoes import Notificacoes
from collections import Counter
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")


class AssistenteIA:
    """ Gerencia o processo de criação e exibição da mensagem customizada pela API do Gemini"""
    @staticmethod
    def _analisar_itens_json():
        """
        -> Analisa o arquivo de itens para gerar estatísticas de doações e locais críticos
        :return: (tuple) Retorna uma tupla contendo as informações analisadas pela IA
        """
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
        """
        -> Gera uma mensagem de boas-vindas utilizando a API do Gemini
        :param dono_id: (str) Nome do usuário
        :return: (str) Retorna o texto formatado da assistente virtual
        """
        try:
            todas = Notificacoes.buscar_notificacoes(dono_id)
            nao_lidas = [n for n in todas if not n['lida']]
            qtd_matches = len([n for n in nao_lidas if n['tipo'] == 'MATCH'])
            qtd_sucesso = len([n for n in nao_lidas if n['tipo'] == 'SUCESSO'])
            qtd_outras = len(nao_lidas) - (qtd_matches + qtd_sucesso)
            primeiro_login = len(todas) == 1 and todas[0]['tipo'] == 'SISTEMA'
            status_login = "ESTE É O PRIMEIRO LOGIN DO USUÁRIO NO SISTEMA!" if primeiro_login else "Este é um usuário recorrente."
            texto_notif = ''
            for n in nao_lidas:
                texto_notif += f"- Tipo: {n['tipo']} | Mensagem: {n['mensagem']} | Data: {n['data_criacao']}\n"
            total_doacao, ultimo_item_doacao, local_critico = AssistenteIA._analisar_itens_json()
            prompt = f"""
            Você é a Assistente Virtual do Portal de Achados e Perdidos da UFRPE.
            STATUS DO USUÁRIO: {status_login}
            O usuário {dono_id} acabou de entrar no sistema.
            === O QUE ACONTECEU ENQUANTO ELE ESTAVA OFFLINE ===
            Total de {len(nao_lidas)} notificações novas.
            Resumo: {qtd_matches} novos Matches, {qtd_sucesso} itens resolvidos e {qtd_outras} avisos de sistema.
            Detalhes brutos para seu contexto:
            {texto_notif}
            === MURAL GERAL DA UNIVERSIDADE ===
            - Ponto de atenção: O local com mais itens perdidos ultimamente é o(a) "{local_critico}".
            - {total_doacao} itens foram para doação por falta de busca (último: {ultimo_item_doacao}).
            === REGRAS DE RESPOSTA ===
            - PRIORIDADE 1 (PRIMEIRO LOGIN): Se o status indicar que é o PRIMEIRO LOGIN dele, ignore os outros dados. Dê boas-vindas calorosas, explique brevemente a
              MISSÃO DO PORTAL (que é ajudar a comunidade acadêmica da UFRPE a recuperar pertences perdidos através da solidariedade) e incentive-o a dar uma olhada no menu
            Crie uma mensagem amigável, acolhedora e conversacional (1 a 2 parágrafos curtos).
            - PRIORIDADE 2: Se ele tiver novos "Matches" ou "Sucessos", comemore isso e mande ele olhar o Quadro de Avisos urgente!
            - PRIORIDADE 3: Se forem apenas notificações de sistema/confirmação, foque em dar uma dica de segurança sobre o local crítico ({local_critico}).
            - PRIORIDADE 4 (TUDO LIDO/NADA NOVO): Se o total de notificações novas for 0, dê as boas vindas de volta, confirme que o quadro dele está em dia e atualize-o 
            sobre o que está rolando no MURAL GERAL (doações ou local crítico).
            - Não faça listas com marcadores repetindo o que está acima, aja como uma secretária de campus batendo um papo rápido.
            - Use emojis universitários.
            """
            client = genai.Client(api_key=API_KEY)
            try:
                resposta = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=prompt,
                )
            except Exception:
                resposta = client.models.generate_content(
                    model='gemini-1.5-flash',
                    contents=prompt,
                )
            return f'\n🤖 [Assistente UFRPE]:\n{resposta.text}'
        except Exception as e:
            return f'\n👋{e} Olá, {dono_id}! Bem-vindo de volta ao Portal de Achados e Perdidos da UFRPE. Confira suas notificações no menu correspondente.'