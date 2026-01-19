# Projeto H - Quizzes

Esse sistema foi feito para criar perguntas, montar quizzes com as perguntas criadas e aplicar os quizzes montados, guardando o resultado das aplicações.
Foi feito pensando nas seguintes funcionalidades:
- Ler arquivos .csv contendo as perguntas, os quizzes e os resultados
- Criar uma nova pergunta, com enunciado, 4 alternativas e uma alternativa correta
- Montar um novo quiz, com título e número variável de perguntas
- Aplicar um quiz já existente, guardando o nome de quem respondeu, a data em que foi respondido, o quiz respondido e a nota obtida
- Visualizar todos os resultados guardados
- Escrever nos arquivos .csv as novas perguntas, os novos quizzes e os novos resultados

O projeto possui dois diretórios principais: src e data.
O src contém os arquivos .py (perguntas, quizzes, resultados e main), além do pycache
O data contém os 3 arquivos .csv (perguntas, quizzes e resultados) utilizados no projeto

# Como executar o projeto

Para sua execução, deve-se ter uma versão do Python superior a 3.10.

Clone o repositório para o local de sua preferência
Após clonar o projeto, navegue com seu terminal até a pasta do projeto (Deve estar algo similar a C:\Proj1Lipai>)
Após a realização da ultima etapa, digite no terminal o seguinte comando: 
- No Windows: python src/main.py
- No Linux/Mac: python3 src/main.py

Se tudo deu certo, um menu deve aparecer com 5 opções:
- (0) Cadastrar Pergunta
- (1) Montar um Quiz
- (2) Aplicar um Quiz
- (3) Mostrar os resultados
- (4) Sair

# Como utilizar o software

O software lhe pedira dois tipos de input:
- Um deles será como o do menu, onde deve-se digitar somente o número da opção desejada e, em seguida, apertar na tecla Enter
- Outro será um input de texto (Ex: Digite o enunciado: , Digite o número de perguntas: ), onde deve-se digitar o que lhe for requisitado.
(Caso o input não seja do tipo desejado pelo programa, apenas irá requisitar ele novamente)

# Formato dos .csv

perguntas.csv: id,enunciado,alternativa_A,alternativa_B,alternativa_C,alternativa_D,alternativa_correta
Ex: 0,Vai rodar?,Sim,Não,Claro,Negativo,A

quizzes.csv: id,titulo,perguntas (onde perguntas contempla todos os ids das perguntas no quiz)
Ex: 1,Teste de mais linhas,0,1

resultados.csv: (id do resultado),(id do quiz),(nome do participante),nota,data
Ex: 1,1,tester,2,19/01/2026