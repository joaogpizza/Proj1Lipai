""" Contém o menu principal, responsável pela interface com o usuário """

from datetime import datetime
import perguntas
import quizzes
import resultados

# Métodos do menu
def cadastrar_pergunta(idp):
    enunciado = input('Digite o enunciado: ')
    alternativas = []
    for i in range(0, perguntas.NUMERO_ALTERNATIVAS):
        alternativas.append(input(f'Digite a alternativa {chr(ord('A')+i)}: '))
    while True:
        alternativa_correta = input('Digite a alternativa correta: ')
        if len(alternativa_correta.strip()) == 1:
            if ord(alternativa_correta.strip()) in range(65, 65+perguntas.NUMERO_ALTERNATIVAS):
                break
        print('Digite uma alternativa válida (A, B, C, ...).')
    pergunta = perguntas.Pergunta(idp, enunciado, alternativas, alternativa_correta)
    perguntas.salvar_pergunta(pergunta)
    print(f'Pergunta salva com id {idp}')
    return pergunta

def montar_quizzes(idq, lista_perguntas):
    titulo = input('Digite o titulo do quiz: ')
    while True:
        try:
            qtd_perguntas = int(input('Digite o número de perguntas desejado: '))
            if qtd_perguntas <= 0:
                print('Digite um número inteiro válido.')
                continue
            break
        except ValueError:
            print('Digite um número inteiro válido.')
    perguntas_quiz = []
    for pergunta in lista_perguntas:
        print(pergunta.em_linha())
    for i in range(0, qtd_perguntas):
        while True:
            try:
                idp = int(input(f'Digite o id da pergunta {i+1}: '))
                if idp < 0 or idp > len(lista_perguntas)-1:
                    print('Digite um id válido.')
                    continue
                perguntas_quiz.append(lista_perguntas[i])
                break
            except ValueError:
                print('Digite um id válido.')
    quiz = quizzes.Quiz(idq, titulo, perguntas_quiz)
    quizzes.salvar_quiz(quiz)
    print(f'Quiz salvo com id {idq}.')
    return quiz

def aplicar_quiz(idr, lista_quizzes):
    for quiz in lista_quizzes:
        print(quiz)
    while True:
        try:
            idq = int(input('Digite o id do quiz a ser aplicado: '))
            if idq < 0 or idq > len(lista_quizzes)-1:
                print('Digite um id válido.')
                continue
            break
        except ValueError:
            print('Digite um id válido')
    nome_participante = input('Digite o nome de quem vai responder: ')
    data = datetime.today().strftime("%d/%m/%Y")
    quiz = lista_quizzes[idq]
    soma = 0
    for pergunta in quiz.lista_perguntas:
        soma += pergunta.aplicar_pergunta()
    resultado = resultados.Resultado(idr, quiz, nome_participante, soma, data)
    resultados.salvar_resultados(resultado)
    print(f'Resultado salvo com id {idr}')
    return resultado

def ver_resultados(lista_resultados):
    if not lista_resultados:
        print('Sem resultados registrados.')
    else:
        for resultado in lista_resultados:
            print(resultado)

def escolha(quantidade_escolhas):
    while True:
        try:
            tentativa = int(input('Digite a opção desejada: '))
            if 0 <= tentativa and tentativa < quantidade_escolhas:
                return tentativa
            print('Digite uma opção válida.')
        except ValueError:
            print('Digite uma opção válida.')

def sair():
    print('Deseja mesmo sair?')
    print('(0) Sim')
    print('(1) Não')
    opcao = escolha(2)
    if not opcao:
        print('Encerrando...')
        return True
    return False

def mais_alguma_coisa():
    print('Mais alguma coisa?')
    print('(0) Sim')
    print('(1) Não')
    opcao = escolha(2)
    if not opcao:
        return False
    return sair()

# Menu (efetivamente, o main)
saiu = False
lista_perguntas = []
lista_quizzes = []
lista_resultados = []
try:
    lista_perguntas = perguntas.carregar_perguntas()
    lista_quizzes = quizzes.carregar_quizzes(lista_perguntas)
    lista_resultados = resultados.carregar_resultados(lista_quizzes)
except ValueError as e:
    print(e)
    saiu = True

idp_atual = len(lista_perguntas)
idq_atual = len(lista_quizzes)
idr_atual = len(lista_resultados)

while not saiu:
    print('--- Menu ---')
    print('Qual a operação desejada?')
    print('(0) Cadastrar Pergunta;')
    print('(1) Montar um Quiz')
    print('(2) Aplicar um Quiz')
    print('(3) Mostrar os resultados')
    print('(4) Sair')
    opcao = escolha(5)
    print('------------')
    if opcao == 0:
        lista_perguntas.append(cadastrar_pergunta(idp_atual))
        idp_atual += 1
    elif opcao == 1:
        if not lista_perguntas:
            print('Como não há perguntas, não se pode montar um quiz.')
        else:
            lista_quizzes.append(montar_quizzes(idq_atual, lista_perguntas))
            idq_atual += 1
    elif opcao == 2:
        if not lista_quizzes:
            print('Não há quizzes para serem aplicados.')
        else:
            lista_resultados.append(aplicar_quiz(idr_atual, lista_quizzes))
            idr_atual += 1
    elif opcao == 3:
        ver_resultados(lista_resultados)
    
    if opcao != 4:
        print('------------')
        saiu = mais_alguma_coisa()
        continue
    saiu = sair()
