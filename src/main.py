""" Contém o menu principal, responsável pela interface com o usuário """

import perguntas
import quizzes
import resultados

# Métodos do menu
def cadastrar_pergunta(idp):
    enunciado = input('Digite o enunciado: ')
    alternativas = []
    for i in range(0, perguntas.NUMERO_ALTERNATIVAS):
        alternativas[i] = input(f'Digite a alternativa {chr(ord('A')+i)}: ')
    alternativa_correta = input('Digite a alternativa correta: ')
    pergunta = perguntas.Pergunta(idp, enunciado, alternativas, alternativa_correta)
    perguntas.salvar_pergunta(pergunta)
    print(f'Pergunta salva com id {idp}')
    return idp+1

def montar_quizzes(idq):
    pass

def aplicar_quiz(idr):
    pass

def ver_resultados():
    pass

def escolha(quantidade_escolhas):
    while True:
        try:
            tentativa = int(input('Digite a opção desejada: '))
            if 0 < tentativa and tentativa <= quantidade_escolhas:
                return tentativa
            print('Digite uma opção válida.')
        except ValueError:
            print('Digite uma opção válida.')

def sair():
    print('Deseja mesmo sair?')
    print('(1) Sim')
    print('(2) Não')
    opcao = escolha(2)
    if opcao == 1:
        print('Encerrando...')
        return True
    return False

def mais_alguma_coisa():
    print('Mais alguma coisa?')
    print('(1) Sim')
    print('(2) Não')
    opcao = escolha(2)
    if opcao == 1:
        return False
    return sair()

# Menu (efetivamente, o main)
saiu = False
try:
    lista_perguntas = perguntas.carregar_perguntas()
    lista_quizzes = quizzes.carregar_quizzes(lista_perguntas)
    lista_resultados = resultados.carregar_resultados(lista_quizzes)
except ValueError as e:
    print(e)
    saiu = True

while not saiu:
    print('--- Menu ---')
    print('Qual a operação desejada?')
    print('(1) Cadastrar Pergunta;')
    print('(2) Montar um Quiz')
    print('(3) Aplicar um Quiz')
    print('(4) Mostrar os resultados')
    print('(5) Sair')
    opcao = escolha(5)
    print('------------')
    if opcao == 1:
        cadastrar_pergunta(len(lista_perguntas))
    elif opcao == 2:
        montar_quizzes(len(lista_quizzes))
    elif opcao == 3:
        aplicar_quiz(len(lista_resultados))
    elif opcao == 4:
        ver_resultados()
    
    if opcao != 5:
        print('------------')
        saiu = mais_alguma_coisa()
        continue
    saiu = sair()
