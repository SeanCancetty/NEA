from unittest import case

Operator = {
    "00001":"LDR",
    "00010":"STR",
    "00011": "ADD",
    "00100": "SUB",
    "00101": "MUL",
    "00110": "DIV",
    "00111": "MOV",
    "01000": "CMP",
    "01001": "JMP",
    "01010": "JEQ",
    "01011": "JNE",
    "01100": "JGT",
    "01101": "JLT",
    "01110": "AND",
    "01111": "ORR",
    "10000": "XOR",
    "10001": "NOT",
    "10010": "LSL",
    "10011": "LSR",
    "10100": "PRT",
    "10101": "RET",
    "10110": "HALT"
}
Register = {
    "00000000":"A0",
    "00000001":"R0",
    "00000010":"R1",
    "00000011":"R2",
    "00000100":"R3",
    "00000101":"R4",
    "00000110":"R5",
    "00000111":"R6",
    "00001000":"R7",
    "00001001":"R8",
    "00001010":"S0",
    "00001011":"S1",
    "00001100":"S2",
    "00001101":"S3",
    "00001110":"S4",
}
AddressMode = [
    #Memory Access
    "001",
    #Constant Access
    "010",
    "011",
    #Register Access
    "100"
]
BranchOperators = [
    "JMP",
    "JEQ",
    "JNE",
    "JGT",
    "JLT"
]

BinaryValues = [128, 64, 32, 16, 8, 4, 2, 1]

def BinaryToInt(binary):
    FullBinary = binary
    FullBinary = list(FullBinary)
    ReturnBinary = ""
    for i in range(8):
        ReturnBinary += FullBinary.pop(-1)
    return int(ReturnBinary[::-1], 2)

def ConvertLabel(Line, AddPeriod: bool = True):
    Line = Line.split("-")
    if AddPeriod:
        if Line[0][0] != ".":
            Line[0][0] = "."

    String = ""
    for Character in Line:
        if Character != ".":
            String += chr(BinaryToInt(Character))
    return String

def ConvertLine(Operat: str, Operand1: str = "", Operand2: str = ""):
    Oper = Operat[:5]
    Adr = Operat[5:]
    if Operand1 == "":
        return Operator[Oper]
    elif Operand2 == "":
        if Operator[Oper] in BranchOperators:
            Operand1 = Operand1.split("-")
            String = ""
            for Character in Operand1:
                String += chr(BinaryToInt(Character))
            return Operator[Oper] + " " + String
        else:
            return Operator[Oper] + " " + Register[Operand1]
    else:
        match Adr:
            case "011":
                return Operator[Oper] + " " + Register[Operand1] + ", " + "\"" + ConvertLabel(Operand2, False) + "\""
            case "001":
                return Operator[Oper] + " " + Register[Operand1] + ", " + str(BinaryToInt(Operand2))
            case "010":
                return Operator[Oper] + " " + Register[Operand1] + ", #" + str(BinaryToInt(Operand2))
            case "100":
                return Operator[Oper] + " " + Register[Operand1] + ", " + Register[Operand2]
            case _:
                return ""

def ConvertSection(SectionLabel, Instructions):
    Label = ConvertLabel(SectionLabel)
    Data = []
    for Instruction in Instructions:
        Data.append(ConvertLine(Instruction.Operator, Instruction.Operand1, Instruction.Operand2))
    return Label, Data
