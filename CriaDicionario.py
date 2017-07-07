"""Cuida da interacao entre LeitorTweets e a estrutura de Hash. Insere na hash aquilo que é lido nos tweets."""
#Necessaria para AppliesRE, biblioteca de expressoes regulares
import re

from Hash import Hash
from LeitorTweets import GetFileContent, GetTextToRate, WriteCSV, WriteTXT, GetTXT

#-----------------------------------------------------------------------------------------------------------------#
#----------------------------------------------Objects------------------------------------------------------------#

class KeyContent:
    """O conteudo presente que sera associado a cada uma das chaves da Hash"""
    def __init__(self):
        self.Value = 0
        self.AccValue = 0
        self.Freq = 0
        self.NegativeAppear = []
        self.PositiveAppear = []
        self.NeutralAppear = []

    def AppendOnAppear(self, Value, LocalOnList):
        if Value < 0:
            self.NegativeAppear.append(LocalOnList)
        if Value > 0:
            self.PositiveAppear.append(LocalOnList)
        if Value == 0:
            self.NeutralAppear.append(LocalOnList)

    def UpdateValue(self, Value):
        self.AccValue += Value
        self.Freq += 1
        self.Value = self.AccValue / self.Freq

#-----------------------------------------------------------------------------------------------------------------#
#------------------------------------------Dict and Text----------------------------------------------------------#

class DictAndText:
    """Estrutura que contem o hash e uma lista de tweets associado a ele.
    Importante para a implementacao da funcionalidade de mostrar em que tweets aparece cada palavra"""
    def __init__(self, Dictionary, NextIndex):
        self.Dictionary = Dictionary
        self.NextIndex = NextIndex #Contador de quantos tweets foram lidos ate entao.
        self.TextFile = "BufferText.txt" #Será guardado nesse arquivo os tweets lidos.


    def ReturnsNegativeTweets(self, Word):
        """Retorna uma lista com todos os tweets negativos"""
        Tweets = GetTXT(self.TextFile)
        Tweets = Tweets.split('\n') #Cria uma lista de strings, cada elemento com um tweet.
        ReturnList = []
        for i in self.Dictionary.Check(Word).NegativeAppear:
            ReturnList.append(Tweets[i])
        return ReturnList

    def ReturnsPositiveTweets(self, Word):
        """Retorna uma lista com todos os tweets positivos"""
        Tweets = GetTXT(self.TextFile)
        Tweets = Tweets.split('\n') #Cria uma lista de strings, cada elemento com um tweet.
        ReturnList = []
        for i in self.Dictionary.Check(Word).PositiveAppear:
            ReturnList.append(Tweets[i])
        return ReturnList

    def ReturnsNeutralTweets(self, Word):
        """Retorna uma lista com todos os tweets neutros"""
        Tweets = GetTXT(self.TextFile)
        Tweets = Tweets.split('\n') #Cria uma lista de strings, cada elemento com um tweet.
        ReturnList = []
        for i in self.Dictionary.Check(Word).NeutralAppear:
            ReturnList.append(Tweets[i])
        return ReturnList

    def ReturnsAllAppears(self, Word):
        """Retorna todos os tweets em que Word aparece"""
        return(self.ReturnsNeutralTweets(Word) + self.ReturnsPositiveTweets(Word) + self.ReturnsNegativeTweets(Word))

#-----------------------------------------------------------------------------------------------------------------#
#------------------------------------Inserting on Dictionary------------------------------------------------------#

def InsertOnHash(Dictionary, Word, Value, LocalOnList):
    """Recebe o dicionario, a palavra normalizada, sentimento associado e o indice do tweet"""
    Content = Dictionary.Check(Word)
    if Content == False:
        Content = KeyContent()
    Content.AppendOnAppear(Value, LocalOnList)
    Content.UpdateValue(Value)
    Dictionary.Append(Word, Content)


def AppliesRE(TweetString):
    """Aplica um conjunto de expressoes regulares em cada tweet, retornando uma lista com apenas strings a serem inseridas no hash"""
    Temp = re.split("[:]|[.]|[,]|[;]|[ ]|[-]|[/]|[?]|[!]|[#]|[|]|[*]|[(]|[)]|[\"]|[\"]", TweetString)
    ReturnValue = []
    for i in Temp:
        if len(i) > 3:
            ReturnValue.append(i.lower())
    return ReturnValue

#-----------------------------------------------------------------------------------------------------------------#
#------------------------------------File Operations--------------------------------------------------------------#

def GetInitialFile():
    """Pega o arquivo inicial e insere seu conteudo numa Hash"""
    LocalOnList = 0
    StringToPass = GetFileContent()
    Dictionary = Hash()
    for i in StringToPass:
        Temp = AppliesRE(i[0])
        Temp = list(set(Temp)) #Remove todas as ocorrencias repetidas de um tweet
        Value = int(i[1])
        for Word in Temp:
            InsertOnHash(Dictionary ,Word, Value, LocalOnList)
        LocalOnList += 1
    ReturningValue = DictAndText(Dictionary, LocalOnList)
    WriteTXT(StringToPass, 'w', ReturningValue.TextFile)
    return ReturningValue

def GetAnotherFile(OldDict):
    """Recebe a antiga estrutura DictAndText; Processa outro arquivo e insere no mesmo dicionário anterior"""
    LocalOnList = OldDict.NextIndex
    StringToPass = GetFileContent()
    Dictionary = OldDict.Dictionary
    TextToReturn = []

    #i = uma linha do documento; i[0] = tweet, i[1] = valor
    for i in StringToPass:
        TextToReturn.append(i)
        Temp = AppliesRE(i[0])
        Temp = list(set(Temp)) #Remove todas as ocorrencias repetidas de um tweet
        Value = int(i[1])
        for Word in Temp:
            InsertOnHash(Dictionary ,Word, Value, LocalOnList)
        LocalOnList += 1

    ReturningValue = DictAndText(Dictionary, LocalOnList)
    WriteTXT(TextToReturn, 'a', ReturningValue.TextFile)
    return ReturningValue

#-----------------------------------------------------------------------------------------------------------------#
#-------------------------------------Predict Operations----------------------------------------------------------#

def PredictFeelings(Dictionary):
    TweetsToPredict = GetTextToRate()
    TweetsToPredict = TweetsToPredict.split('\n')
    ListToReturn = []
    for Tweet in TweetsToPredict:
        SumOfValue = 0
        Temp = AppliesRE(Tweet)
        for Word in Temp:
            WordValue = Dictionary.Check(Word) #Dictionary.Check(Word) retornara uma KeyContent
            if WordValue != False:
                WordValue = WordValue.Value
                SumOfValue += WordValue

        if SumOfValue > 0.1:
            SumOfValue = 1
        if SumOfValue < -0.1:
            SumOfValue = -1
        if SumOfValue <= 0.1 and SumOfValue >= -0.1:
            SumOfValue = 0
        ListToReturn.append([Tweet, str(SumOfValue)])
    WriteCSV(ListToReturn)

#-----------------------------------------------------------------------------------------------------------------#
#-------------------------------------Map Tweets Operations-------------------------------------------------------#

def PassTweetsToCSV(Value, ListTweets):
    """Recebe uma lista de Tweets e um sentimento, forma uma tupla [tweet, sentimento] e passa tudo para WriteCSV"""
    ListtoPass = []
    for tweet in ListTweets:
        ListtoPass.append([tweet, Value])
    WriteCSV(ListtoPass)

def PassTweetsWithoutValue(Word, Dictionary):
    """Passa todos os tweets e chama WriteCSV direto"""
    ListToPass = []
    Temp = Dictionary.ReturnsPositiveTweets(Word)
    for tweet in Temp:
        ListToPass.append([tweet, 1])
    Temp = Dictionary.ReturnsNegativeTweets(Word)
    for tweet in Temp:
        ListToPass.append([tweet, -1])
    Temp = Dictionary.ReturnsNeutralTweets(Word)
    for tweet in Temp:
        ListToPass.append([tweet, 0])
    WriteCSV(ListToPass)

#-----------------------------------------------------------------------------------------------------------------#
#------------------------------------Debugging only---------------------------------------------------------------#
#-----------------------------------------------------------------------------------------------------------------#

if __name__ == "__main__":  #Debug only
    AllInAll = GetInitialFile()
    #PredictFeelings(AllInAll.Dictionary)
    """
    AllInAll = GetAnotherFile(AllInAll)
    PredictFeelings(AllInAll.Dictionary)
    """

    Word = input("Insira palavra a buscar: ")
    PassTweetsWithoutValue(Word, AllInAll)
    """print("Positivas: ")
    output = AllInAll.ReturnsPositiveTweets(Word)
    PassTweetsToCSV(1, output)
    for i in output:
        print(i)
    print()

    print("Negativas: ")
    output = AllInAll.ReturnsNegativeTweets(Word)
    for i in output:
        print(i)
    print()

    print("Neutras: ")
    output = AllInAll.ReturnsNeutralTweets(Word)
    for i in output:
        print(i)
    print()
    #Text= AllInAll.ReturnsAllAppears('microsoft')
    #PredictFeelings(AllInAll.Dictionary)

    print("Negative: ")
    print()
    for i in Text:
        print(i)
    Text= AllInAll.ReturnsPositiveTweets('microsoft')
    print()
    print("Positive: ")
    print()
    for i in Text:
        print(i)
    Text= AllInAll.ReturnsNeutralTweets('microsoft')
    print()
    print("Neutral: ")
    print()
    for i in Text:
        print(i)"""
