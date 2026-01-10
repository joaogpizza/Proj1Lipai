""" Contem a classe Resultado e métodos para salvar e carregar estes """

import os
import csv
from datetime import datetime
import quizzes

PATH_CSV = os.path.join((os.path.dirname(os.path.abspath(__file__))), '..', 'data', 'resultados.csv')
TAMANHO_ESPERADO = 4

class Resultado:
    """ Classe que lida com resultados """
    def __init__(self, idr, quiz, nome_participante, nota, data):
        self.idr = idr
        self.quiz = quiz
        self.nome_participante = nome_participante
        self.nota = nota
        self.data = data
    def para_csv(self):
        """ Transforma um Resultado em uma linha csv """
        return [
            str(self.idr),
            str(self.quiz.idq),
            self.nome_participante,
            str(self.nota),
            self.data
        ]
    def __str__(self):
        resultado = f'{self.idr} (quiz: {self.quiz.idq}):\n'
        resultado += f'Participante: {self.nome_participante}\n'
        resultado += f'Nota: {self.nota}\n'
        resultado += f'Data: {self.data}'
        return resultado
    def __eq__(self, valor):
        if isinstance(valor, self.__class__):
            return valor.idr == self.idr
        return False
    def __hash__(self):
        return hash(self.idr)
    # Getters e Setters
    @property
    def idr(self):
        """ Getter de idr """
        return self._idr
    @idr.setter
    def idr(self, valor):
        """ Pode levantar ValueError se valor não for um int ou for negativo """
        if not isinstance(valor, int) or valor < 0:
            raise ValueError('idr invalido')
        self._idr = valor
    @property
    def quiz(self):
        """ Getter de quiz """
        return self._quiz
    @quiz.setter
    def quiz(self, valor):
        """ Pode levantar ValueError se valor não for um quiz ou for nulo """
        if not isinstance(valor, quizzes.Quiz) or not valor:
            raise ValueError('quiz invalido')
        self._quiz = valor
    @property
    def nome_participante(self):
        """ Getter de nome_participante """
        return self._nome_participante
    @nome_participante.setter
    def nome_participante(self, valor):
        """ Pode levantar ValueError se valor não for str ou for nulo """
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError('nome_participante invalido')
        self._nome_participante = valor
    @property
    def nota(self):
        """ Getter de nota """
        return self._nota
    @nota.setter
    def nota(self, valor):
        """ 
        Pode levantar ValueError se valor não for int, 
        se for negativo ou se for maior que a nota máxima possível.
        """
        if not isinstance(valor, int) or valor < 0 or valor > len(self.quiz.lista_perguntas):
            raise ValueError('nota invalida')
        self._nota = valor
    @property
    def data(self):
        """ Getter de data """
        return self._data
    @data.setter
    def data(self, valor):
        """ 
        Pode levantar ValueError se valor não for uma str ou 
        se estiver no formato incorreto.
        """
        if isinstance(valor, str):
            try:
                datetime.strptime(valor, "%d/%m/%Y")
            except ValueError:
                raise ValueError('data invalida')
            self._data = valor
        else:
            raise ValueError('data invalida')

def salvar_resultados(resultado):
    """
    Salva o resultado resultado em data/resultados.csv
    """
    with PATH_CSV.open(newline = '', encoding = 'utf-8') as arq:
        escritor = csv.writer(arq)
        escritor.writerow(resultado.para_csv())

def carregar_resultados(lista_arq_quizzes):
    """
    Retorna um vetor com todos os resultados em data/resultados.csv como entidades 
    da classe Resultado, pode levantar ValueError caso uma linha não esteja de acordo
    com os conformes.
    """
    if not lista_arq_quizzes:
        return []
    resultados = []
    numero_linha = 0
    with PATH_CSV.open(newline = '', encoding = 'utf-8') as arq:
        leitor = csv.reader(arq, delimiter = ';')
        for linha in leitor:
            numero_linha += 1
            if not linha:
                continue
            if len(linha) != TAMANHO_ESPERADO:
                raise ValueError(f'Linha {numero_linha} invalida')
            idr = int(linha[0])
            idq = int(linha[1])
            nome_participante = linha[2]
            nota = int(linha[3])
            data = linha[4]
            achou_quiz = False
            for quiz in lista_arq_quizzes:
                if quiz.idq == idq:
                    achou_quiz = True
                    resultado = Resultado(idr, quiz, nome_participante, nota, data)
                    resultados.append(resultado)
                    break
            if not achou_quiz:
                raise ValueError(f'Quiz do resultado da linha {numero_linha} não encontrado')
    return resultados
