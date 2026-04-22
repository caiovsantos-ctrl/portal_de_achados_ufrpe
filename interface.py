import subprocess, os
from time import sleep

def exibir_menu_padrao(titulo, lista_opcoes, largura=50):
    print("=" * largura)
    print("=====" + titulo.center(largura - 10) + "=====")
    print("=" * largura)
    print("")
    for opcao in lista_opcoes:
        print(f"  {opcao}")
    print("") 
    print("=" * largura)



def limpar_tela():
    sleep(1.5)
    comando  = 'cls' if os.name == 'nt' else 'clear'
    subprocess.run(comando, shell=True)


def verificar_escape(modelo):
    if modelo == '0':
        print('Retornando...\n\n')
        return True
    return False


def tentar_novamente(mensagem = 'Deseja tentar novamente?[S/N] '):
     while True:
        tentativa = input(mensagem)
        tentativa = tentativa.strip().upper()
        if tentativa == '':
            print('Resposta não pode ser vazia. Tente novamente')
            continue
        elif not tentativa.isalpha() or tentativa not in 'SN':
            print('Resposta deve ser S ou N. Tente novamente')
            continue
        elif len(tentativa) != 1:
            print('Resposta deve ser apenas um caractere. Tente novamente')
        return tentativa