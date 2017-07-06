"""Cuida da interacao entre LeitorTweets e a estrutura de Hash. Insere na hash aquilo que é lido nos tweets."""
#Necessaria para AppliesRE, biblioteca de expressoes regulares
import re

from Hash import Hash
from LeitorTweets import GetFileContent

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

class DictAndText:
    """Estrutura que contera o hash e uma lista de tweets associado a ele.
    Importante para a implementacao da funcionalidade de mostrar em que tweets aparece cada palavra"""
    def __init__(self, Dictionary, Text, NextIndex):
        self.Dictionary = Dictionary
        self.Tweets = Text
        self.NextIndex = NextIndex

    def ReturnsNegativeTweets(self, Word):
        ReturnList = []
        for i in self.Dictionary.Check(Word).NegativeAppear:
            ReturnList.append(self.Tweets[i][0])
        return ReturnList

    def ReturnsPositiveTweets(self, Word):
        ReturnList = []
        for i in self.Dictionary.Check(Word).PositiveAppear:
            ReturnList.append(self.Tweets[i][0])
        return ReturnList

    def ReturnsNeutralTweets(self, Word):
        ReturnList = []
        for i in self.Dictionary.Check(Word).NeutralAppear:
            ReturnList.append(self.Tweets[i][0])
        return ReturnList



def InsertOnHash(Dictionary, Word, Value, LocalOnList):
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
    ReturningValue = DictAndText(Dictionary, StringToPass, LocalOnList)
    return ReturningValue

def GetAnotherFile(OldDict):
    """Recebe a antiga estrutura DictAndText; Processa outro arquivo e insere no mesmo dicionário anterior"""
    LocalOnList = OldDict.NextIndex
    StringToPass = GetFileContent()
    Dictionary = OldDict.Dictionary
    TextToReturn = OldDict.Tweets

    for i in StringToPass:
        TextToReturn.append(i)
        Temp = AppliesRE(i[0])
        Temp = list(set(Temp)) #Remove todas as ocorrencias repetidas de um tweet
        Value = int(i[1])
        for Word in Temp:
            InsertOnHash(Dictionary ,Word, Value, LocalOnList)
        LocalOnList += 1

    ReturningValue = DictAndText(Dictionary, TextToReturn, LocalOnList)
    return ReturningValue


if __name__ == "__main__":  #Debug only
    AllInAll = GetInitialFile()
    Text= AllInAll.ReturnsNegativeTweets('microsoft')
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
        print(i)
