from ContextFreeGrammar import CFG
from PushdownAutomaton import PDA


def FileRead(path):
    """
    Read file from path and return text.
    """
    try:
        inputFile = open(path)
        inputText = inputFile.read()
        return inputText
    except:
        print("wrong path!")
        exit()


def main():
    flag = 0
    in1 = input("PDA/CFG? ")
    if in1.lower() == "pda":
        flag = 1
    elif in1.lower() == "cfg":
        flag = -1
    else:
        print("wrong input!")
    theObject = None
    if flag == 1:
        path = input("path: ")
        theObject = PDA()
        theObject.TextToPDA(FileRead(path))
    elif flag == -1:
        path = input("path: ")
        theObject = CFG()
        theObject.TextToCFG(FileRead(path))
    else:
        exit()
    while 1:
        choice = input(
"""
1. show PDA/CFG
2. Convert PDA to CFG or vice versa and show result
3. exit
"""
        )
        if int(choice) == 1:
            print(theObject.ToString())
        elif int(choice) == 2:
            if flag == 1:
                print(theObject.ToCFG().ToString())
            else:
                print(theObject.ToPDA().ToString())
        elif int(choice) == 3:
            exit()
        else:
            print("wrong input!")


if __name__ == "__main__":
    main()
