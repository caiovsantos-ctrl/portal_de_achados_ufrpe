PORTAL DE ACHADOS UFRPE


   É um projeto colaborativo para tratamento e centralização de achados e perdidos na UFRPE, desenvolvido no terminal do Python.
   Para a primeira Release foi desenvolvido os seguintes pontos:
Funcionalidades:
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

Bibliotecas:
•	Os
•	Subprocess
•	Json
•	Textwrap
Organizar o mural de itens, evitando que a descrição não quebre a formatação.
•	Time


Principais dificuldades:
•	Fazer o código do motor de buscas
•	Atualizar status do item
•	Escopo de variáveis
•	Retorno e parâmetro de funções

Link da Planilha:
https://docs.google.com/spreadsheets/d/1myEqbO7eCX_OGsQmDMzTTACJum08KHDDSSPvzOUeiec/edit?usp=drivesdk
Link do Fluxograma:
https://drive.google.com/file/d/1xlWcvnnhI0ZfQU3xtPDnWYeeXmHsPmtY/view?usp=drivesdk
Link do Vídeo de Caio Vinícius:
https://youtu.be/4-7x5nZafME
Link do Vídeo de Carlos Henrique:
https://youtu.be/V0VnSVOsZy0
