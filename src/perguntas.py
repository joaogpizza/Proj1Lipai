""" Contém a classe Pergunta e métodos para salvar e carregar estas. """

import os
import csv

NUMERO_ALTERNATIVAS = 4
PATH_CSV = os.path.join((os.path.dirname(os.path.abspath(__file__))), '..', 'data', 'perguntas.csv')
TAMANHO_ESPERADO = NUMERO_ALTERNATIVAS + 3

class Pergunta:
    """ Classe que lida com perguntas. """
    def __init__(self, idp, enunciado, alternativas, alternativa_correta):
        self.idp = idp
        self.enunciado = enunciado
        self.alternativas = alternativas
        self.alternativa_correta = alternativa_correta
    def para_csv(self):
        """ Converte a pergunta em uma linha csv. """
        return [
            str(self.idp),
            self.enunciado,
            *self.alternativas,
            self.alternativa_correta
        ]
    def em_linha(self):
        """ 
        Converte a pergunta em uma linha do tipo 'idp: enunciado', para não lotar 
        a tela de listagem de perguntas
        """
        return f'{self.idp}: {self.enunciado}'
    def __str__(self):
        resultado = f'{self.enunciado}\n'
        for i in range(0, NUMERO_ALTERNATIVAS):
            resultado += f'\n({chr(ord('A') + i)}) {self.alternativas[i]}'
        return resultado + '\n'
    def __eq__(self, valor):
        if isinstance(valor, self.__class__):
            return valor.idp == self.idp
        return False
    def __hash__(self):
        return hash(self.idp)
    def respondeu_certo(self, chute):
        """ 
        Verifica se a resposta dada é correta ou não, pode levantar ValueError caso chute não 
        corresponda a uma alternativa ou TypeError caso não seja um caractere.
        """
        if ord(chute) not in range(65, 65+NUMERO_ALTERNATIVAS):
            raise ValueError('Valor não corresponde a uma alternativa')
        return self.alternativa_correta == chute
    def aplicar_pergunta(self):
        """ Aplica uma pergunta e fica em um loop até receber uma resposta válida """
        print(self)
        while True:
            resposta = input('Digite a alternativa que julgar correta: ')
            try:
                acertou = self.respondeu_certo(resposta)
                break
            except Exception as e:
                print(e)
        if acertou:
            return 1
        return 0
    # Getters e Setters
    @property
    def idp(self):
        """ Getter de idp """
        return self._idp
    @idp.setter
    def idp(self, idp):
        """ Pode levantar ValueError caso idp não seja um int ou seja negativo """
        if not isinstance(idp, int) or idp < 0:
            raise ValueError('id invalido')
        self._idp = idp
    @property
    def enunciado(self):
        """ Getter de enunciado """
        return self._enunciado
    @enunciado.setter
    def enunciado(self, enunciado):
        """ Pode levantar ValueError caso enunciado não seja uma string ou seja uma vazia """
        if not isinstance(enunciado, str) or not enunciado.strip():
            raise ValueError('enunciado invalido')
        self._enunciado = enunciado
    @property
    def alternativas(self):
        """ Getter de alternativas """
        return self._alternativas
    @alternativas.setter
    def alternativas(self, alternativas):
        """ 
        Pode levantar ValueError caso alternativas não seja uma lista de strings,  
        o número de alternativas não seja o esperado ou tenha pelo menos uma 
        alternativa vazia.
        """
        if not isinstance(alternativas, list[str]) or len(alternativas) != NUMERO_ALTERNATIVAS:
            raise ValueError('alternativas invalida')
        for i in range(0, NUMERO_ALTERNATIVAS):
            if not (alternativas[i]).strip():
                raise ValueError(f'alternativa {i} invalida')
        self._alternativas = alternativas
    @property
    def alternativa_correta(self):
        """ Getter de alternativa_correta """
        return self._alternativa_correta
    @alternativa_correta.setter
    def alternativa_correta(self, alternativa_correta):
        """ 
        Pode levantar ValueError caso alternativa_correta não seja um char válido 
        ou seja um vazio.
        """
        if not isinstance(alternativa_correta, str) or len(alternativa_correta.split()) != 1 or ord(alternativa_correta) not in range(65, 65+NUMERO_ALTERNATIVAS):
            raise ValueError('alternativa_correta invalida')
        self._alternativa_correta = alternativa_correta

def salvar_pergunta(perg):
    """
    Salva a pergunta perg em data/perguntas.csv.
    """
    with PATH_CSV.open(newline = '', encoding = 'utf-8') as arq:
        escritor = csv.writer(arq)
        escritor.writerow(perg.para_csv())

def carregar_perguntas():
    """
    Retorna um vetor com todas as perguntas em data/perguntas.csv como entidades 
    da classe Pergunta, pode levantar ValueError caso uma linha não esteja de acordo
    com os conformes.
    """
    perguntas = []
    numero_linha = 0
    with PATH_CSV.open(newline = '', encoding = 'utf-8') as arq:
        leitor = csv.reader(arq, delimiter = ';')
        for linha in leitor:
            numero_linha += 1
            if not linha:
                continue
            alternativas = []
            if len(linha) != TAMANHO_ESPERADO:
                raise ValueError(f'Linha {numero_linha} está errada')
            idp = int(linha[0].strip())
            enunciado = linha[1]
            for i in range(0, NUMERO_ALTERNATIVAS):
                alternativas.append(linha[2+i])
            alternativa_correta = linha[TAMANHO_ESPERADO - 1]
            pergunta = Pergunta(idp, enunciado, alternativas, alternativa_correta)
            perguntas.append(pergunta)
    return perguntas
