import functools
import operator


class ProductionRule:
    def __init__(self, left, *right):
        self.leftHand = left
        self.rightHand = set()
        for item in right:
            self.rightHand.add(item)

    def AddRight(self, *right):
        """
        Add right hand to rule.
        """
        for item in right:
            self.rightHand.add(item)

    def ToString(self):
        """
        Return All rules with same left hand as string.
        """
        string = self.leftHand + " ->"
        for right in self.rightHand:
            string += " " + right + " |"
        return string[:-1]


class CFG:
    def __init__(self):
        self.variables = set()
        self.terminals = set()
        self.terminals.add("$")
        self.rules = {}

    def TextToCFG(self, inputText):
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
        """
        return CFG as string.
        """
        string = "V = { "
        for variable in self.variables:
            string += variable + ", "
        string = string[:-2]
        string += " }\n"
        string += "T = { "
        for terminal in self.terminals:
            string += terminal + ", "
        string = string[:-2]
        string += " }\n"
        string += "S = S\n"
        string += "P = {\n"
        for variable in self.rules:
            string += "\t" + self.rules[variable].ToString() + "\n"
        string = string.replace("$", "\u03BB")
        string += "}"
        return string

    def ToPDA(self):
        """
        create a PDA from this CFG
        """
        from PushdownAutomaton import PDA

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
