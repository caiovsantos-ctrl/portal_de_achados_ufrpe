# PORTAL DE ACHADOS UFRPE


   É um projeto colaborativo para tratamento e centralização de achados e perdidos na UFRPE, desenvolvido no terminal do Python.
   Para a primeira Release foi desenvolvido os seguintes pontos:
## Funcionalidades:
•	CRUD Usuário

Essa funcionalidade é responsável pela parte de cadastro, atualizar dados pessoais e deletar conta.

•	CRUD Item

Funcionalidade que cuida do cadastro, da atualização de status e da deleção de itens.

•	Motor de buscas

Essa funcionalidade dinamiza o projeto: quando um item é cadastrado o sistema percorre todos os itens que já foram cadastrados e que tenham o status diferente do cadastrado para dar matching, por meio da descrição. Com isso, promove maior agilidade e facilidade no processo de encontrar os itens perdidos.

•	Protocolo sustentável de temporalidade

Após 30 dias que o item foi cadastrado e o dono não foi encontrado, o item fica disponível para doação/reciclagem. Essa funcionalidade contribui com a sustentabilidade e com a economia circular do item.

•	Mapa de calor das perdas

Mostra um ranking dos locais da UFRPE que foram perdidos mais itens. Através dele, o projeto fica mais interativo e gera curiosidade e engajamento, além de alertar os estudantes para terem mais cuidado nesses locais. 

•	Mural de itens

Mostra todos os itens que ainda estão ativos, especificando seus detalhes. Importante para quem perdeu um item e não deu matching. 

•	Histórico do usuário

Mostra todos os itens cadastrados pelo usuário e possibilita alterar o status do item ou deletá-lo.

•	Privacidade de dados

A descrição de um item com o status achado é ocultada no mural de itens, o que possibilita maior segurança no ciclo do item e evita falsos donos. 

•	Quadro de avisos

Irá aparecer um quadro que mostrará todas as notifiações das principais atividades do usuário, além dele poder ler ou deletar as notificações.

•	Recibo

Quando o usuário cadastra o item e acontece o match, após ele dizer que a situação foi resolvida o sistema gera um recibo para a retirada.

•	Painel de Impacto

Irá aparecer um relatório para o usuário mostrando informações importantes do andamento e da situção do sistema.

•	Sistema de Boas-vindas com uso de API do Gemini

Após o login irá aparecer uma mensagem personalizada com uso da API do Gemini informando as principais novidades que aconteceram enquanto ele estava fora.



## Bibliotecas:
•	Os, Subprocess

•	Json:
Persistência dos dados

•	Textwrap:
Organizar as notificações, evitando que o conteúdo não quebre a formatação.

•	Time, Datetime:
Responsável pelas pausas e identificar a data atual

•  Platform:
Compatibilidade no momento de abrir o recibo

•  Unicodedata, Difllib, Phonenumbers:
Normalização dos dados

•  Google-genai:
Implementar a API do Gemini

• Collections:
Permite a API analisar o local crítico no arquivo json  

•  Dotenv:
Proteção da chave da API

•  Fpdf2:
Fazer o recibo no formato pdf

• Rich
Melhorar a exibição do projeto


## Principais dificuldades:
•	Fazer o código do motor de buscas

•	Atualizar status do item

•	Escopo de variáveis

•	Retorno e parâmetro de funções

•  Conversão para POO

•  Importações circulares

•  Gerar o recibo em pdf

•  Implementar a API do Gemini


## Importações necessárias

pip install fpdf2

pip install google-genai

pip install python-dotenv

pip install rich

## Links

Link da Planilha:
https://docs.google.com/spreadsheets/d/1myEqbO7eCX_OGsQmDMzTTACJum08KHDDSSPvzOUeiec/edit?usp=drivesdk

Link do Artigo:
https://drive.google.com/file/d/12p0SUaHRK-updm0wrc3O9CvurfkHVH7H/view?usp=drivesdk

Link do Vídeo de Caio Vinícius:
https://youtu.be/_B8-QdGjztg

Link do Vídeo de Carlos Henrique:
https://youtu.be/GcJab5rmTjw 
