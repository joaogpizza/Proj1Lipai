""" Contém a classe Quiz e métodos para salvar estes. """

import os
import csv

PATH_CSV = os.path.join((os.path.dirname(os.path.abspath(__file__))), '..', 'data', 'quizzes.csv')
TAMANHO_MINIMO = 2

class Quiz:
    """ Classe que lida com quizzes """
    def __init__(self, idq, titulo, lista_ids_perguntas):
        self.idq = idq
        self.titulo = titulo
        self.lista_ids_perguntas = lista_ids_perguntas
    def para_csv(self):
        """ Transforma um Quiz em uma linha csv """
        return [
            str(self.idq),
            self.titulo,
            *self.lista_ids_perguntas
        ]
    def __str__(self):
        return f'{self.idq}: {self.titulo}, {len(self.lista_ids_perguntas)} perguntas;'
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
    def lista_ids_perguntas(self):
        """ Getter de lista_perguntas """
        return self._lista_ids_perguntas
    @lista_ids_perguntas.setter
    def lista_ids_perguntas(self, valor):
        """ 
        Pode levantar ValueError caso lista_perguntas não seja uma lista de Perguntas ou  
        seja uma vazia
        """
        if not isinstance(valor, list[int]) or not valor:
            raise ValueError('lista_ids_perguntas invalida')
        self._lista_ids_perguntas = valor

def salvar_quiz(quiz):
    """
    Salva o quiz quiz em data/quizzes.csv.
    """
    with PATH_CSV.open(newline = '', encoding = 'utf-8') as arq:
        escritor = csv.writer(arq)
        escritor.writerow(quiz.para_csv())

def carregar_quizzes():
    """
    Retorna um vetor com todos os quizzes em data/quizzes.csv como entidades 
    da classe Quiz, pode levantar ValueError caso uma linha não esteja de acordo
    com os conformes.
    """
    quizzes = []
    numero_linha = 0
    with PATH_CSV.open(newline = '', encoding = 'utf-8') as arq:
        leitor = csv.reader(arq, delimiter = ';')
        for linha in leitor:
            numero_linha += 1
            if not linha or all(cedula.strip() == '' for cedula in linha):
                continue
            lista_ids_perguntas = []
            if len(linha) < TAMANHO_MINIMO:
                raise ValueError(f'Linha {numero_linha} está errada')
            idq = int(linha[0])
            titulo = linha[1]
            for cedula_original in linha[2:]:
                cedula = cedula_original.strip()
                if not cedula:
                    continue
                lista_ids_perguntas.append(int(cedula))
            if not lista_ids_perguntas:
                raise ValueError(f'Quiz {numero_linha} sem perguntas')
            pergunta = Quiz(idq, titulo, lista_ids_perguntas)
            quizzes.append(pergunta)
    return quizzes
