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
        string = self.leftHand + " ->"
        for right in sorted(self.rightHand):
            string += " " + right + " |"
        return string[:-1]


class CFG:
    def __init__(self):
        self.variables = set()
        self.terminals = set()
        self.terminals.add("$")
        self.rules = {}

    def textToCFG(self, inputText):
        """
        Get text and find Variables, Terminals and rules then create a CFG object.
        """
        for char in inputText:
            if char.islower():
                self.AddTerminal(char)
            elif char.isupper():
                self.AddVariable(char)
        inputText = inputText.splitlines()
        for rule in inputText:
            self.AddRule(*rule.split())

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
        if left in self.variables and terminal in self.terminals:
            self.rules[left].AddRight(right)

    def ToString(self):
        string = ""
        for variable in self.rules:
            string = string + self.rules[variable].ToString() + "\n"
        string = string.replace("$", "\u03BB")
        return string[:-1]

    def ToPDA(self):
        """
        create a PDA from this CFG
        """
        pda = PDA()
        pda.SetStates(3, 0, 2)
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

    def ToString(self):
        string = (
            "\u03B4(q"
            + self.state1
            + ","
            + self.inputChar
            + ","
            + self.topOfStack
            + ") = (q"
            + self.state2
            + ","
            + self.stackPushValue
            + ")"
        )
        return string


class PDA:
    def __init__(self):
        self.transitions = {}
        self.inputAlfabet = set()
        self.stackAlfabet = set()

    def TextToPDA(self, inputText):
        """
        creat PDA from InputText.
        """
        inputText = inputText.splitlines()
        self.SetStates(int(inputText[0]), 0, int(inputText[1]))
        del [inputText[1], inputText[0]]
        for item in inputText:
            item = item.split()
            self.AddTransition(item[0], item[3], item[1], item[2], item[4])
            self.AddInputChar(item[1])
            self.AddStackChar(*item[2], *item[4])

    def SetStates(self, statesCount, startState, acceptingState):
        """
        get self, statesCount, startState & acceptingState then set them and create dictionary for PDA transitions.
        """
        self.statesCount = statesCount
        self.startState = startState
        self.acceptingState = acceptingState
        for i in range(self.statesCount):
            self.transitions[str(i)] = set()

    def AddInputChar(self, *char):
        for item in char:
            self.inputAlfabet.add(item)

    def AddStackChar(self, *char):
        for item in char:
            self.stackAlfabet.add(item)

    def AddTransition(self, state1, state2, inputChar, topOfStack, stackPushValue):
        """
        get Transition data and add new Transition to PDA's transitions.
        """
        self.transitions[str(state1)].add(
            Transition(str(state1), str(state2), inputChar, topOfStack, stackPushValue)
        )

    def ToString(self):
        string = ""
        for state in self.transitions.values():
            for transition in state:
                string += transition.ToString() + "\n"
        string = string.replace("$", "\u03BB")
        return string[:-2]

    def ToCFG(self):
        """
        create CFG from this PDA.
        """
        cfg = CFG()
        cfg.AddTerminal(*self.inputAlfabet, "$")
        for state in self.transitions.values():
            for transition in state:
                if transition.stackPushValue == "$":
                    cfg.AddVariable(
                        "q"
                        + transition.state1
                        + transition.topOfStack
                        + "q"
                        + transition.state2
                    )
                    cfg.AddRule(
                        "q"
                        + transition.state1
                        + transition.topOfStack
                        + "q"
                        + transition.state2,
                        transition.inputChar,
                    )
                else:
                    for qk in range(self.statesCount):
                        for ql in range(self.statesCount):
                            left = (
                                "q"
                                + transition.state1
                                + transition.topOfStack
                                + "q"
                                + str(qk)
                            )
                            right = (
                                transition.inputChar
                                + "(q"
                                + transition.state2
                                + transition.stackPushValue[0]
                                + "q"
                                + str(ql)
                                + ")(q"
                                + str(ql)
                                + transition.stackPushValue[1]
                                + "q"
                                + str(qk)
                                + ")"
                            )
                            cfg.AddVariable(left)
                            cfg.AddRule(left, right)
        return cfg