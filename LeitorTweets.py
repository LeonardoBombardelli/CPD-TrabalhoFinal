"""Nesse documentos estarão armazenadas as funções para a leitura e escrita no formato .csv"""
#Utilizaremos a biblioteca csv para trabalhar com os arquivos recebidos
#https://docs.python.org/3/library/csv.html
import csv

"""
Comecaremos criando funcoes para a leitura do arquivo fornecido (.csv)
"""

def GetFileContent():
    """Recebe o nome do arquivo do usuario e retorna, em apenas uma lista de strings."""
    """Para cada elemento de ReturningString, ReturningString[0] = tweet, ReturningString[1] = int com sentimento associado"""

    DidntFind = True
    ReturningString = []
    while DidntFind:
        FileToGet = input("Insira o nome do arquivo a ser lido (terminando com .csv)")
        try:
            with open(FileToGet, newline='', encoding = 'utf-8') as f:
                FileContent = csv.reader(f)
                for row in FileContent:
                    ReturningString.append(row)
            f.closed
            DidntFind = False
        except FileNotFoundError:
            print("Insira um arquivo presente no diretorio")
    return ReturningString

if __name__ == "__main__":  #Debug only
    a = GetFileContent()
    for i in a:
        print(i[0])
