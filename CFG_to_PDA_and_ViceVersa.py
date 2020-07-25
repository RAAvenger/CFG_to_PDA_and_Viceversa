import functools
import operator


def FileRead(path):
    """
    Read file from path and return CFG.
    """
    inputFile = open(path)
    inputText = inputFile.read()
    return inputText


class ProductionRule:
    def __init__(self, left, *right):
        self.leftHand = left
        self.rightHand = set()
        for item in right:
            self.rightHand.add(item)

    def AddRight(self, *right):
        for item in right:
            self.rightHand.add(item)

    def ToString(self):
        string = self.leftHand + "->"
        for right in self.rightHand:
            string += right + "|"
        return string[:-1]


class CFG:
    def __init__(self):
        self.variables = set()
        self.terminals = set()
        self.rules = {}

    def __init__(self, inputText):
        """
        Get text and find Variables, Terminals and rules then create a CFG object.
        """
        self.variables = set()
        self.terminals = set()
        self.terminals.add("$")
        self.rules = {}
        for char in inputText:
            if char.islower():
                self.AddTerminal(char)
            elif char.isupper():
                self.AddVariable(char)
        inputText = inputText.splitlines()
        for rule in inputText:
            self.AddRule(*rule.split())

    def ToString(self):
        string = ""
        for variable in self.rules:
            string = string + self.rules[variable].ToString() + "\n"
        return string[:-2]

    def AddVariable(self, *VariableName):
        """
        Add new Variable(s) to class variable list.
        """
        for item in VariableName:
            if item not in self.variables:
                self.variables.add(item)
                self.rules[item] = ProductionRule(item)

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
            self.rules[left].AddRight(right)

    def ToPDA(self):
        """
        create a PDA from this CFG
        """
        pda = PDA(3, 0, 2)
        pda.AddTransition(0, 1, "$", "z", "Sz")
        pda.AddTransition(1, 2, "$", "z", "z")
        for terminal in self.terminals:
            pda.AddTransition(1, 1, terminal, terminal, "$")
        for rule in self.rules.values():
            for right in rule.rightHand:
                pda.AddTransition(1, 1, "$", rule.leftHand, right)
        return pda


class Transition:
    def __init__(self, state1, state2, inputChar, topOfStack, stackPushValue):
        self.state1 = state1
        self.state2 = state2
        self.inputChar = inputChar
        self.topOfStack = topOfStack
        self.stackPushValue = stackPushValue


class PDA:
    def __init__(self):
        self.statesCount = 0
        self.startState = 0
        self.acceptingState = 0
        self.transitions = set()

    def __init__(self, text):
        text = text.splitlines()
        self.statesCount = int(text[0])
        self.startState = 0
        self.acceptingState = int(text[1])
        del [text[1], text[0]]
        self.transitions = set()
        for item in text:
            item = item.split()
            self.AddTransitions(item[0], item[3], item[1], item[2], item[4])

    def __init__(self, statesCount, startState, acceptingState):
        self.statesCount = statesCount
        self.startState = startState
        self.acceptingState = acceptingState
        self.transitions = set()

    def AddTransition(self, state1, state2, inputChar, topOfStack, stackPushValue):
        """
        get Transition data and add new Transition to PDA's transitions.
        """
        self.transitions.add(
            Transition(state1, state2, inputChar, topOfStack, stackPushValue)
        )


## main
txt = FileRead("test\in.txt")
cfg=CFG(txt)
print(cfg.ToString())
cfg.ToPDA()
pass
