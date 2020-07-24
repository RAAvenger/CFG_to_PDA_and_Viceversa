def FileRead(path):
    """
    Read file from path and return CFG.
    """
    inputFile = open(path)
    inputText = inputFile.read()
    return inputText


class ProductionRule:
    def __init__(self, leftVariable, rightTerminal, *rightVariables):
        self.leftVariable = tuple(leftVariable)
        self.rightTerminal = tuple(rightTerminal)
        self.rightVariables = tuple(rightVariables)


class CFG:
    def __init__(self):
        self.variables = set()
        self.terminals = set()
        self.rules = set()

    def __init__(self, inputText):
        """
        Get text and find Variables, Terminals and rules then create a CFG object.
        """
        terminals = set()
        variables = set()
        for char in inputText:
            if char.islower():
                terminals.add(char)
            elif char.isupper():
                variables.add(char)
        self.AddTerminal(*terminals)
        self.AddVariable(*variables)
        inputText = inputText.splitlines()
        for rule in inputText:
            self.AddRule(*rule.split())

    def AddVariable(self, *VariableName):
        """
        Add new Variable(s) to class variable list.
        """
        for item in VariableName:
            self.variables.add(item)

    def AddTerminal(self, *TerminalName):
        """
        Add new Terminal(s) to class terminal list.
        """
        for item in TerminalName:
            self.terminals.add(item)

    def AddRule(self, left, right):
        """
        get lefthand and righthand of rule and add rule to CFG.
        """
        if not right:
            raise Exception("AddRule: empty right.")
        terminal, *variables, = right
        if (
            left in self.variables
            and terminal in self.terminals
            and all(item in self.variables for item in variables)
        ):
            self.rules.add(ProductionRule(left, terminal, *variables))


## main
txt = FileRead("test\in.txt")
f = CFG(txt)
pass
