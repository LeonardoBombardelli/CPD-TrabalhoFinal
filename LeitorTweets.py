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
        FileToGet = input("Insira o nome do arquivo a ser lido (terminando com .csv): ")
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

def GetTextToRate():
    """Recebe o nome do arquivo do usuario e retorna uma lista de texto."""
    FileToRead = ""
    DidntFind = True
    while DidntFind:
        FileToRead = input("Insira o nome do arquivo a ser lido (terminando com .txt): ")
        try:
            with open(FileToRead) as f:
                FileContent = f.read()
            f.closed
            DidntFind = False
        except FileNotFoundError:
            print("Insira um arquivo presente no diretorio")
    return FileContent

def WriteTXT(Text, Mode, FileName):
    with open(FileName, Mode, encoding = 'utf-8') as Output:    #Mode = 'w' for overwrite, 'a' for append
        for tweet in Text:
            Output.write(tweet[0] + '\n')
    Output.close()

def GetTXT(FileName):
    try:
        with open(FileName, encoding = 'utf-8') as FileToRead:
            FileContent = FileToRead.read()
        FileToRead.closed
        return FileContent
    except FileNotFoundError:
        print("Arquivo " + FileName + " nao esta presente no diretorio!")

def WriteCSV(DataToWrite):
    """Recebe um array de arrays e cria um arquivo .csv com esses dados"""
    #Primeiro, tentamos nao fazer um overwrite de conteudos anteriores
    Counter = 1
    DidntFind = True
    while DidntFind:
        try:
            open('Output' + str(Counter) + '.csv')
            Counter += 1
        except FileNotFoundError:
            OutFile = open('Output' + str(Counter) + '.csv', 'w')
            DidntFind = False
    Writer = csv.writer(OutFile)
    Writer.writerows(DataToWrite)
    OutFile.close()

if __name__ == "__main__":  #Debug only
    Data = [["Eu nao aguento mais", "-1"], ["Eu nao aguento mais mesmo", "-1"], ["AAAAAAAAAAAAAAAAAaaaaaaa", "1"]]
    WriteCSV(Data)
