#!/bin/bash/python3
#
# Written by Somnath
#
# Description :: A shit-ass assembler made as part of Nand2Tetris Part-I course
#
# Tables
compTable = {
    "0": "0101010",
    "1": "0111111",
    "-1": "0111010",
    "D": "0001100",
    "A": "0110000",
    "!D": "0001101",
    "!A": "0110001",
    "-D": "0001111",
    "-A": "0110011",
    "D+1": "0011111",
    "A+1": "0110111",
    "D-1": "0001110",
    "A-1": "0110010",
    "D+A": "0000010",
    "D-A": "0001110",
    "A-D": "0000111",
    "D&A": "0000000",
    "D|A": "0010101",
    "M": "1110000",
    "!M": "1110001",
    "-M": "1110011",
    "M+1": "1110111",
    "M-1": "1110010",
    "D+M": "1000010",
    "D-M": "1010011",
    "M-D": "1000111",
    "D&M": "1000000",
    "D|M": "1010101",
}

destTable = {
    "null": "000",
    "M": "001",
    "D": "010",
    "MD": "011",
    "A": "100",
    "AM": "101",
    "AD": "110",
    "AMD": "111",
}

jumpTable = {
    "null": "000",
    "JGT": "001",
    "JEQ": "010",
    "JGE": "011",
    "JLT": "100",
    "JNE": "101",
    "JLE": "110",
    "JMP": "111",
}

symbolTable = {
    "R0": "0",
    "R1": "1",
    "R2": "2",
    "R3": "3",
    "R4": "4",
    "R5": "5",
    "R6": "6",
    "R7": "7",
    "R8": "8",
    "R9": "9",
    "R10": "10",
    "R11": "11",
    "R12": "12",
    "R13": "13",
    "R14": "14",
    "R15": "15",
    "SCREEN": "16384",
    "KBD": "24576",
    "SP": "0",
    "LCL": "1",
    "ARG": "2",
    "THIS": "3",
    "THAT": "4",
}


# Helper Functions
def removeNewLines(commands: list[str]) -> list[str]:
    _list = []
    for elem in commands:
        _list.append(elem.strip().split("\n")[0])
    _list = [x for x in _list if x]
    return _list


def isACommand(command: str) -> bool:
    if command[0] == "@":
        if ord(command[1]) >= 48 and ord(command[1]) <= 57:
            return True
    return False


def isCCommand(command: str) -> bool:
    if command[0] != "@" and command[0] != "(":
        return True
    return False


def extractFields(cInstructionString: str) -> list[str]:
    fields = ["", "", ""]  # dest=comp;jmp
    currIns = cInstructionString
    if not isCCommand(currIns):
        fields = ["", "", ""]
    else:
        if currIns.find("=") != -1:
            insComp = currIns.split("=")
            fields[0] = insComp[0]
            if len(insComp) > 0:
                fields[1] = insComp[1]
        if currIns.find(";") != -1:
            insComp = currIns.split(";")
            fields[1] = insComp[0]
            if len(insComp) > 0:
                fields[2] = insComp[1]
    return fields


class Assembler:
    _filename = ""
    _commands = []
    _current = ""
    _counter = 0

    def __init__(self, filename) -> None:
        self._filename = filename
        # Reading given file
        with open(self._filename) as buffer:
            self._commands = buffer.readlines()
        # Removing newlines (\n)
        self._commands = removeNewLines(self._commands)
        # Setting _current to 0th command
        self._current = self._commands[0]

    def getCurrentInstruction(self) -> str:
        return self._commands[self._counter]

    def nextInstruction(self) -> int:
        if self._counter == len(self._commands) - 1:
            self._counter = 0
        else:
            self._counter += 1
            self._current = self._commands[self._counter]
        return self._counter

    def currentInstructionType(self) -> bytes:
        if isACommand(self._current):
            return b"A"
        elif isCCommand(self._current):
            return b"C"
        else:
            return b"S"

    def dest(self):
        fields = extractFields(self._current)
        return fields[0]

    def comp(self):
        fields = extractFields(self._current)
        return fields[1]

    def jump(self):
        fields = extractFields(self._current)
        return fields[2]

    def translateAInstruction(self) -> str:
        translated = ""
        currIns = self._current
        if isACommand(currIns) == False:
            translated = ""
        else:
            strDecimal = "".join(currIns.split("@")[1:])
            decimal = int(strDecimal)
            binary = "{0:016b}".format(decimal)
            translated = binary

        return translated

    def translateCInstruction(self) -> str:
        translated = ""
        destVal = ""
        compVal = ""
        jumpVal = ""

        currIns = self._current
        if isCCommand(currIns) == False:
            translated = ""
        else:
            if p.dest():
                destVal = destTable.get(p.dest())
            else:
                destVal = "000"

            if p.comp():
                compVal = compTable.get(p.comp())
            else:
                compVal = "0000000"

            if p.jump():
                jumpVal = jumpTable.get(p.jump())
            else:
                jumpVal = "000"

            translated = "111" + compVal + destVal + jumpVal

        return translated

    def firstPass(self):
        insCounter = 0
        adjust = 0
        for i in range(len(self._commands)):
            currInc = self._commands[insCounter]
            if currInc.find("(") == -1 or currInc.find(")") == -1:
                pass
            else:
                label = currInc.split("(")[1].split(")")[0]
                symbolTable[label] = str(insCounter - adjust)
                adjust += 1
            insCounter += 1
        # Removing instruction of the form (xxx)
        self._commands = [x for x in self._commands if x.find("(")]

    def secondPass(self):
        n = 16
        insCounter = 0
        for i in range(len(self._commands)):
            currInc = self._commands[insCounter]
            # Dealing with variables
            if isACommand(currInc) or isCCommand(currInc):
                pass
            else:
                label = currInc.split("@")[1]
                if symbolTable.get(label):
                    labelValue = symbolTable.get(label)
                    self._commands[insCounter] = "@" + labelValue
                else:
                    symbolTable[label] = str(n)
                    self._commands[insCounter] = "@" + str(n)
                    n += 1
            insCounter += 1

    def finalPass(self):
        self.firstPass()
        self.secondPass()
        # Translation
        insCounter = 0
        for i in range(len(self._commands)):
            currIns = self._commands[insCounter]
            if isACommand(currIns):
                self._current = currIns
                translated = self.translateAInstruction()
                print(translated)
            else:
                self._current = currIns
                translated = self.translateCInstruction()
                print(translated)
            insCounter += 1


if __name__ == "__main__":
    p = Assembler("fill.asm")
    p.finalPass()
    print(symbolTable)
