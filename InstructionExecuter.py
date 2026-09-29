import FlagTypesDatatype
FlagTypes = FlagTypesDatatype.FlagTypes

BinaryValues = [128, 64, 32, 16, 8, 4, 2, 1]
ConditionFlag = FlagTypes.NONE
StandaloneOperators = [
    "LDR",
    "STR",
    "MOV",
    "CMP",
    "NOT",
    "PRT",
    "RET",
    "HALT",
    "ERR"
]
BranchOperators = [
    "JMP",
    "JEQ",
    "JNE",
    "JGT",
    "JLT"
]
MathOperators = [
    "ADD",
    "SUB",
    "MUL",
    "DIV"
]
BitwiseOperators = [
    "AND",
    "ORR",
    "XOR",
    "LSL",
    "LSR"
]
Memory = []
Registers = [
    #R0 - 3
    0, 0, 0, 0, 0, 0, 0, 0, 0,
    #S0 - 3
    "", "", "", "",
    #A0
    0
]

def init():
    global Memory
    Memory = []
    for i in range(256):
        Memory.append(0)
    global ConditionFlag
    ConditionFlag = FlagTypes.NONE
    global Registers
    Registers = [
        0, 0, 0, 0, 0, 0, 0, 0, 0,
        "", "", "", "",
        0
    ]

def Execute(Operator, Operand1, Operand2 = None):
    ReturnValue = 0
    if Operator in StandaloneOperators:
        match Operator:
            case "LDR":
                ReturnValue = LDR(Operand1, Operand2)
            case "STR":
                ReturnValue = STR(Operand1, Operand2)
            case "MOV":
                ReturnValue = MOV(Operand1, Operand2)
            case "CMP":
                ReturnValue = CMP(Operand1, Operand2)
            case "NOT":
                ReturnValue = NOT(Operand1)
            case "PRT":
                ReturnValue = PRT(Operand1)
            case "RET":
                ReturnValue = RET()
            case "HALT":
                ReturnValue = "|--|"
            case "ERR":
                ReturnValue = "!--!" + str(Operand1) + str(Operand2)
    elif Operator in BranchOperators:
        ReturnValue = Branch(Operator, Operand1)
    elif Operator in MathOperators:
        ReturnValue = MATH(Operator, Operand1, Operand2)
    elif Operator in BitwiseOperators:
        ReturnValue = SetRegister("A0", BitwiseOperations(Operator, Operand1, Operand2))
    else:
        ReturnValue = "!::!" + Operator
    return ReturnValue

def IntToBinary(number):
    number = int(number)
    binary = ""
    number = number % 256
    for i in range(8):
        if number - BinaryValues[i] >= 0:
            number -= BinaryValues[i]
            binary += "1"
        else:
            binary += "0"
    return binary

def BinaryToInt(binary):
    FullBinary = binary
    FullBinary = list(FullBinary)
    ReturnBinary = ""
    for i in range(8):
        ReturnBinary += FullBinary.pop(-1)
    return int(ReturnBinary[::-1], 2)

def SetRegister(register, data):
    if register == "ACC" or "A" in register[0]:
        register = "A0"
    if len(register) > 2:
        return "!::!" + register

    try:
        match register[0]:
            case "R":
                Registers[int(register[1])] = int(data)
            case "S":
                Registers[int(register[1]) + 9] = str(data)[1:-1]
            case "A":
                Registers[int(register[1]) + 13] = int(data)
        return "|::|"
    except Exception as e:
        return "!::!" + data

def GetRegister(register: str):
    if register == "ACC" or "A" in register[0]:
        register = "A0"
    if len(register) > 2:
        return 0

    match register[0]:
        case "R":
            return Registers[int(register[1])]
        case "S":
            return Registers[int(register[1]) + 9]
        case "A":
            return Registers[int(register[1]) + 13]
    return 0

def LDR(register, address):
    ReturnValue = SetRegister(register, Memory[address])
    return ReturnValue

def STR(register, address: int):
    if GetRegister(register) is not None and address < len(Memory):
        Memory[address] = GetRegister(register)
        return "|::|"
    else:
        return "!::!" + str(address) + "¦" + register

def MATH(operation, register1, register2):
    if GetRegister(register1) is None or GetRegister(register2) is None:
        return "!::!" + register1 + "¦" + register2
    match operation:
        case "ADD":
            SetRegister("A0", (GetRegister(register1) + GetRegister(register2)))
            return "|::|"
        case "SUB":
            SetRegister("A0", (GetRegister(register1) - GetRegister(register2)))
            return "|::|"
        case "MUL":
            SetRegister("A0", (GetRegister(register1) * GetRegister(register2)))
            return "|::|"
        case "DIV":
            SetRegister("A0", (GetRegister(register1) / GetRegister(register2)))
            return "|::|"
        case _:
            return "!::!" + operation

def MOV(register, data):
    if isinstance(data, str):
        if data == "":
            return "!::!"
        match data[0]:
            case "#":
                Number = ""
                for i in range(len(data) - 1):
                    Number += data[i+1]
                Number = int(Number)
                return SetRegister(register, Number)
            case "R":
                return SetRegister(register, GetRegister(data))
            case "A":
                return SetRegister(register, GetRegister(data))
            case "\"":
                return SetRegister(register, data)
            case "'":
                return SetRegister(register, data)
            case _:
                try:
                    MOV(register, int(data))
                except ValueError:
                    return "!::!" + "MOV" + data
    elif isinstance(data, int):
        return SetRegister(register, Memory[data])
    else:
        return "!::!" + str(data)

def CMP(register, data):
    global ConditionFlag
    CompareResult = 0
    if isinstance(data, str):
        match data[0]:
            case "#":
                Number = ""
                for i in range(len(data) - 1):
                    Number += data[i + 1]
                Number = int(Number)
                CompareResult = GetRegister(register) - Number
            case "R":
                CompareResult = GetRegister(register) - GetRegister(data)
            case "S":
                CompareResult = GetRegister(register) == GetRegister(data)
            case "A":
                CompareResult = GetRegister(register) - GetRegister(data)
            case _:
                try:
                    CMP(register, int(data))
                except ValueError:
                    return "!::!" + data
    elif isinstance(data, int):
        CompareResult = GetRegister(register) - Memory[data]

    if isinstance(CompareResult, bool):
        if CompareResult:
            ConditionFlag = FlagTypes.ZERO
        else:
            ConditionFlag = FlagTypes.NEQ
    else:
        if CompareResult > 0:
            ConditionFlag = FlagTypes.POS
        elif CompareResult < 0:
            ConditionFlag = FlagTypes.NEG
        else:
            ConditionFlag = FlagTypes.ZERO

    print(ConditionFlag)
    return "|::|"

def Branch(Oper, Label):
    match Oper:
        case "JMP":
            return Label
        case "JEQ":
            if ConditionFlag == FlagTypes.ZERO:
                return Label
            else:
                return "|::|"
        case "JNE":
            if ConditionFlag != FlagTypes.ZERO:
                return Label
            else:
                return "|::|"
        case "JGT":
            if ConditionFlag == FlagTypes.POS:
                return Label
            else:
                return "|::|"
        case "JLT":
            if ConditionFlag == FlagTypes.NEG:
                return Label
            else:
                return "|::|"
        case _:
            return "!::!" + Oper

def BitwiseOperations(Operation, Register, data):
    FirstValue = IntToBinary(GetRegister(Register))
    SecondValue = 0
    if isinstance(data, str):
        match data[0]:
            case "#":
                Number = ""
                for i in range(len(data) - 1):
                    Number += data[i+1]
                SecondValue = Number
            case "&":
                SecondValue = GetRegister(data)
            case "R":
                SecondValue = GetRegister(data)
            case "%":
                SecondValue = GetRegister(data)
            case "S":
                SecondValue = GetRegister(data)
            case "A":
                SecondValue = GetRegister(data)
            case _:
                try:
                    BitwiseOperations(Operation, Register, int(data))
                except ValueError:
                    return "!::!" + data
    elif isinstance(data, int):
        SecondValue = Memory[data]
    SecondValue = IntToBinary(int(SecondValue))
    match Operation:
        case "AND":
            OutputBinary = ""
            for i in range(8):
                FirstVal = FirstValue[i]
                SecondVal = SecondValue[i]
                if FirstVal == "1" and SecondVal == "1":
                    OutputBinary += "1"
                else:
                    OutputBinary += "0"
            return BinaryToInt(OutputBinary)
        case "ORR":
            OutputBinary = ""
            for i in range(8):
                FirstVal = FirstValue[i]
                SecondVal = SecondValue[i]
                if FirstVal == "1" or SecondVal == "1":
                    OutputBinary += "1"
                else:
                    OutputBinary += "0"
            return BinaryToInt(OutputBinary)
        case "XOR":
            OutputBinary = ""
            for i in range(8):
                FirstVal = FirstValue[i]
                SecondVal = SecondValue[i]
                if FirstVal == "1" and SecondVal == "1":
                    OutputBinary += "0"
                elif FirstVal == "1" and SecondVal == "0":
                    OutputBinary += "1"
                elif FirstVal == "0" and SecondVal == "1":
                    OutputBinary += "1"
                else:
                    OutputBinary += "0"
            return BinaryToInt(OutputBinary)
        case "LSL":
            FirstValue = BinaryToInt(FirstValue)
            SecondValue = BinaryToInt(SecondValue) % 8
            if SecondValue > 0:
                FirstValue *= (2 * SecondValue)
            return FirstValue
        case "LSR":
            FirstValue = BinaryToInt(FirstValue)
            SecondValue = BinaryToInt(SecondValue) % 8
            if SecondValue > 0:
                FirstValue /= (2 * SecondValue)
            return FirstValue
        case _:
            return 0

def NOT(Register):
    Value = IntToBinary(GetRegister(Register))
    OutputBinary = ""
    for i in range(8):
        if Value[i] == "1":
            OutputBinary += "0"
        else:
            OutputBinary += "1"
    return SetRegister(Register, BinaryToInt(OutputBinary))

def PRT(data):
    ReturnValue = ""
    if isinstance(data, str):
        match data[0]:
            case "#":
                Number = ""
                for i in range(len(data) - 1):
                    Number += data[i+1]
                ReturnValue = Number
            case "R":
                ReturnValue = GetRegister(data)
            case "S":
                if GetRegister(data) != "":
                    ReturnValue = GetRegister(data)
                else:
                    ReturnValue = " "
            case "A":
                ReturnValue = GetRegister(data)
            case _:
                try:
                    PRT(int(data))
                except ValueError:
                    return "!::!" + data
    elif isinstance(data, int):
        try:
            ReturnValue = Memory[data]
        except IndexError:
            return "!::!" + str(data)
    return ReturnValue

def RET():
    return "|^^|"