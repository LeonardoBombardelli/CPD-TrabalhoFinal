"""Arquivo inicial!!! Tratar como main()"""
import CriaDicionario as cd

def MenuOptionsDisplay():
    print("Selecione o que deseja fazer:")
    print("1 - Inserir um arquivo .csv novo para o dicionario (Overwrite no antigo)")
    print("2 - Inserir um arquivo .csv a mais para o dicionario (Nisso, leia-se append)")
    print("3 - Faz a predicao de sentimentos de frases em um arquivo .txt")
    print("4 - Gera um .csv com todos os tweets de uma determinada palavra")
    print("0 - Sai do programa")
    print()
    print()

def SubMenu4(Dictionary):
    print()
    Word= input("Escolha a palavra: ")
    Word = Word.lower()
    print()
    print("Escolha:")
    print("1 - Retorna todos os tweets de determinada palavra")
    print("2 - Retorna apenas tweets positivos")
    print("3 - Retorna apenas tweets negativos")
    print("4 - Retorna apenas tweets neutros")

    Opt = int(input("Insira a opcao: "))

    if Opt == 1:
        cd.PassTweetsWithoutValue(Word, Dictionary)
        return
    if Opt == 2:
        Temp = Dictionary.ReturnsPositiveTweets(Word)
        cd.PassTweetsToCSV(1, Temp)
        return
    if Opt == 3:
        Temp = Dictionary.ReturnsNegativeTweets(Word)
        cd.PassTweetsToCSV(-1, Temp)
        return
    if Opt == 4:
        Temp = Dictionary.ReturnsNeutralTweets(Word)
        cd.PassTweetsToCSV(0, Temp)
        return
    else:
        print("Digite um numero valido!!!")





def Menu():
    """Loop onde ocorrera o programa. Impossibilita chamada de funcoes antes de inserir um dicionario, por exemplo."""
    GotValidDict = False
    LoopControl = True
    while LoopControl:
        MenuOptionsDisplay()
        try:
            Option = int(input("Insira a opcao desejada: "))
        except:
            print("Insira um numero valido")

        if Option == 0:
            exit(0)

        if Option == 1:
            Dictionary = cd.GetInitialFile()
            GotValidDict = True

        if GotValidDict:
            if Option == 2:
                Dictionary = cd.GetAnotherFile(Dictionary)

            if Option == 3:
                cd.PredictFeelings(Dictionary.Dictionary)

            if Option == 4:
                SubMenu4(Dictionary)

        else:
            print("Insira um .csv antes de usar essa opcao")

        print()
        input("Digite enter para continuar...")
        print()

if __name__ == "__main__":
    Menu()
