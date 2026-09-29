import InstructionExecuter

Sections = []
Memory = []
Registers = []
class SectionData:
    def __init__(self, Label: str, Size: int, Data: list):
        self.SectionLabel: str = Label
        self.SectionSize: int = Size
        self.Instructions = Data

    def Execute(self):
        ReturnValues = []
        for Line in self.Instructions:
            ReturnValues.append(Line.Execute())
        return ReturnValues

class XSMLine:
    def __init__(self, instruction, opr1 = "", opr2 = ""):
        self.Operator = instruction
        self.Operand1 = opr1
        self.Operand2 = opr2

    def Execute(self):
        global Memory
        global Registers
        ReturnValue = InstructionExecuter.Execute(self.Operator, self.Operand1, self.Operand2)
        Memory = InstructionExecuter.Memory
        Registers = InstructionExecuter.Registers
        return ReturnValue

def init():
    global Sections
    global Memory
    global Registers
    Sections = []
    Memory = InstructionExecuter.Memory
    Registers = InstructionExecuter.Registers

    InstructionExecuter.init()

# Removes the New Line character, the tab character and four spaces next to each other (just in case '    ' is used instead of tab)
def CleanLine(Line):
    Templine = Line
    if "\n" in Line:
        Templine = Line.replace("\n", "")
    if "\t" in Line:
        Templine = Templine.replace("\t", "")
    if "    " in Line:
        Templine = Templine.replace("    ", "")
    if "," in Line:
        Templine = Templine.replace(",", "")

    return Templine


# Gets the different sections from the xasm file
def GetSections(text: str):
    global Sections
    Sections = []

    # Creates a SectionData Object to store the section data
    text = text.split("\n")
    TempList = []
    Counter = 0
    for Line in text:
        # Removes the new line character and tab character
        Line = CleanLine(Line)

        # Runs through the length of the file and creates instances of SectionData objects
        try:
            if Line[0] == "." and Counter == 0:
                Counter += 1
                TempList = []
                TempLabel = Line.replace(".", "")
            elif Line[0] == "." and Counter != 0:
                Counter += 1
                Sections.append(SectionData(TempLabel, len(TempList), TempList))
                TempList = []
                TempLabel = Line.replace(".", "")
            elif Line != "\n":
                TempList.append(GetXSMLine(Line))
        except:
            pass

    Sections.append(SectionData(TempLabel, len(TempList), TempList))
    return True

def GetString(Line: str, StringChar: str = "\""):
    String = ""
    if StringChar in Line:
        StartIndex = Line.index(StringChar) + 1
        for i in range((len(Line) - 1) - StartIndex):
            if Line[i + StartIndex] != StringChar:
                String += Line[i + StartIndex]
            else:
                break
        return String, StartIndex
    else:
        return "", 0

#Creates an XASMLine object
def GetXSMLine(Line):
    String, EndIndex = GetString(Line)
    #Split the Line into a list
    if EndIndex != 0:
        Line = Line[0:EndIndex - 1]
    Instruction = Line.replace(",", "").split(" ")

    if len(Instruction) > 2:
        if Instruction[2] == "" and String != "":
            Instruction[2] = "\"" + String + "\""
        return XSMLine(Instruction[0], Instruction[1], Instruction[2])
    elif len(Instruction) == 2:
        return XSMLine(Instruction[0], Instruction[1])
    else:
        return XSMLine("ERR", Instruction)