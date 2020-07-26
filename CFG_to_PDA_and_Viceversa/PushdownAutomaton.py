class Transition:
    def __init__(self, state1, state2, inputChar, topOfStack, stackPushValue):
        self.state1 = state1
        self.state2 = state2
        self.inputChar = inputChar
        self.topOfStack = topOfStack
        self.stackPushValue = stackPushValue

    def ToString(self):
        """
        return transition as string.
        """
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
        """
        Add char to input alfabet.
        """
        for item in char:
            self.inputAlfabet.add(item)

    def AddStackChar(self, *char):
        """
        Add char to stack alfabet.
        """
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
        """
        return PDA as string.
        """
        string = ""
        for state in self.transitions.values():
            for transition in state:
                string += transition.ToString() + "\n"
        string = string.replace("$", "\u03BB")
        return string[:-1]

    def ToCFG(self):
        """
        create CFG from this PDA.
        """
        from ContextFreeGrammar import CFG

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
