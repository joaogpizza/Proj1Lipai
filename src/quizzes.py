""" Contém a classe Quiz e métodos para salvar e carregar estes. """

import os
import csv
import perguntas

PATH_CSV = os.path.join((os.path.dirname(os.path.abspath(__file__))), '..', 'data', 'quizzes.csv')
TAMANHO_MINIMO = 2

class Quiz:
    """ Classe que lida com quizzes """
    def __init__(self, idq, titulo, lista_perguntas):
        self.idq = idq
        self.titulo = titulo
        self.lista_perguntas = lista_perguntas
    def para_csv(self):
        """ Transforma um Quiz em uma linha csv """
        resultado = [str(self.idq), self.titulo]
        for pergunta in self.lista_perguntas:
            resultado.append(str(pergunta.idp))
        return resultado
    def __str__(self):
        return f'{self.idq}: {self.titulo}, {len(self.lista_perguntas)} perguntas;'
    def __eq__(self, value):
        if isinstance(value, self.__class__):
            return value.idq == self.idq
        return False
    def __hash__(self):
        return hash(self.idq)
    # Getters e Setters
    @property
    def idq(self):
        """ Getter de idq """
        return self._idq
    @idq.setter
    def idq(self, idq):
        """ Pode levantar ValueError caso idq não seja um int ou seja negativo """
        if not isinstance(idq, int) or idq < 0:
            raise ValueError('id invalido')
        self._idq = idq
    @property
    def titulo(self):
        """ Getter de titulo """
        return self._titulo
    @titulo.setter
    def titulo(self, titulo):
        """ Pode levantar ValueError caso titulo não seja uma string ou seja uma vazia """
        if not isinstance(titulo, str) or not titulo.strip():
            raise ValueError('titulo invalido')
        self._titulo = titulo
    @property
    def lista_perguntas(self):
        """ Getter de lista_perguntas """
        return self._lista_perguntas
    @lista_perguntas.setter
    def lista_perguntas(self, valor):
        """ 
        Pode levantar ValueError caso lista_perguntas não seja uma lista de Perguntas ou  
        seja uma vazia
        """
        if not (isinstance(valor, list) and all(isinstance(i, perguntas.Pergunta) for i in valor)) or not valor:
            raise ValueError('lista_perguntas invalida')
        self._lista_perguntas = valor

def salvar_quiz(quiz):
    """
    Salva o quiz quiz em data/quizzes.csv.
    """
    with open(PATH_CSV, 'a', newline = '', encoding = 'utf-8') as arq:
        escritor = csv.writer(arq)
        escritor.writerow(quiz.para_csv())

def carregar_quizzes(lista_arq_perguntas):
    """
    Retorna um vetor com todos os quizzes em data/quizzes.csv como entidades 
    da classe Quiz, pode levantar ValueError caso uma linha não esteja de acordo
    com os conformes.
    """
    if not lista_arq_perguntas:
        return []
    quizzes = []
    numero_linha = 0
    with open(PATH_CSV, newline = '', encoding = 'utf-8') as arq:
        leitor = csv.reader(arq, delimiter = ',')
        for linha in leitor:
            numero_linha += 1
            if not linha or all(cedula.strip() == '' for cedula in linha):
                continue
            lista_ids_perguntas = []
            lista_perguntas = []
            if len(linha) < TAMANHO_MINIMO:
                raise ValueError(f'(Quizzes) Linha {numero_linha} está errada')
            idq = int(linha[0].strip())
            titulo = linha[1]
            for cedula_original in linha[2:]:
                cedula = cedula_original.strip()
                if not cedula:
                    continue
                lista_ids_perguntas.append(int(cedula))
            if not lista_ids_perguntas:
                raise ValueError(f'Quiz {numero_linha} sem perguntas')
            for pergunta in lista_arq_perguntas:
                if pergunta.idp in lista_ids_perguntas:
                    lista_perguntas.append(pergunta)
            if len(lista_perguntas) != len(lista_ids_perguntas):
                raise ValueError(f'Alguma pergunta do quiz da linha {numero_linha} não existe')
            quiz = Quiz(idq, titulo, lista_perguntas)
            quizzes.append(quiz)
    return quizzes
