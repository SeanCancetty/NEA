import ScriptAssembler as Assembler
import InstructionExecuter as IExecuter
import time
import customtkinter
import tkinter
import XMCToXASMConverter as Converter
from tkinter import filedialog

TerminalEntry = "<Return>"
UploadPath = ""

class TerminalFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.Textbox = customtkinter.CTkTextbox(self, height=240, width=240)
        self.Textbox.grid(column=0, row=0, sticky="nsew")
        #Ensures the user can't edit displayed text
        self.Textbox.configure(state="disabled")

        self.Entry = customtkinter.CTkEntry(self, height=30, width=240)
        self.Entry.bind(TerminalEntry, self.RunEntry)
        self.Entry.grid(column=0, row=1, sticky="nsew")

    def RunEntry(self, event):
        self.Entry.configure(state="disabled")
        Line = self.Entry.get()
        if Line != "":
            Check = Line[:3]
            Check2 = Line[:4]
            if Check == "ORD":
                try:
                    FullString = Line[4:]
                    for Character in FullString:
                        self.AppendText(IExecuter.IntToBinary(ord(Character)))
                except Exception as e:
                    self.AppendText(e)
            elif Check2 == "HASH":
                try:
                    FullString = Line[5:]
                    HashResult = 1
                    for Character in FullString:
                        HashResult *= ord(Character)
                    self.AppendText(str(HashResult))
                except Exception as e:
                    self.AppendText(e)
            else:
                Assembler.init()
                self.Entry.delete(0, "end")
                ExecutableLine = Assembler.GetXSMLine(Line)
                self.AppendText(ExecutableLine.Execute())

        self.Entry.configure(state="normal")

    def ReplaceText(self, text: str):
        self.Textbox.configure(state="normal")
        self.Textbox.delete(1.0, "end")
        self.Textbox.insert(0.0, text)
        self.Textbox.configure(state="disabled")

    def AppendText(self, text: str):
        text = str(text)
        self.Textbox.configure(state="normal")
        if text[len(text) - 1] != "\n":
            text += "\n"
        self.Textbox.insert(   "end", text)
        self.Textbox.configure(state="disabled")

#Main terminal class containing the Label and Frame created earlier
class Terminal:
    def __init__(self, Window: customtkinter.CTk):
        self.Frame = TerminalFrame(Window)
        self.Frame.grid(column=2, row=1, sticky="nsew")

        self.Label = customtkinter.CTkLabel(Window, height=100, width=200, text="Terminal")
        self.Label.grid(column=2, row=0, sticky="nsew")

class MemoryFrame(customtkinter.CTkFrame):
    def __init__(self, Window: customtkinter.CTk):
        super().__init__(Window)
        self.configure(height=720, width=230)
        self.Textbox = customtkinter.CTkTextbox(self, height=600, width=115)
        self.Textbox.grid(column=0, row=0, sticky="nsew")
        self.Textbox.configure(state="disabled")

        self.Mem = customtkinter.CTkTextbox(self, height=600, width=115)
        self.Mem.grid(column=1, row=0, sticky="nsew")
        self.Mem.configure(state="disabled")

    def UpdateRegisterAndMemory(self):
        self.Textbox.configure(state="normal")
        self.Mem.configure(state="normal")
        self.Textbox.delete(1.0, "end")
        self.Mem.delete(1.0, "end")

        FullMem = ""
        FullReg = ""
        for i in range(len(Assembler.Memory) - 1):
            FullMem += f"{str(i).zfill(3)}: " + str(Assembler.Memory[i]) + "\n"
        for i in range(len(Assembler.Registers)):
            if i <= 8:
                FullReg += f"R{i}: " + str(Assembler.Registers[i]) + "\n"
            elif i <= 12:
                FullReg += f"S{i-9}: " + Assembler.Registers[i] + "\n"
            else:
                FullReg += f"A{i-12}: " + str(Assembler.Registers[i]) + "\n"
        self.Mem.insert( 0.0, FullMem)
        self.Textbox.insert(0.0, FullReg)
        self.Textbox.configure(state="disabled")
        self.Mem.configure(state="disabled")


#The display for internal Register values
class RegisterDisplay:
    def __init__(self, Window: customtkinter.CTk):
        self.Frame = MemoryFrame(Window)
        self.Frame.grid(column=0, row=1, sticky="nsew")
        Assembler.init()
        self.Frame.UpdateRegisterAndMemory()

        self.Label = customtkinter.CTkLabel(Window, height=100, width=230, text="Register Values")
        self.Label.grid(column=0, row=0)

#File Editor class
class FileEditor:
    def __init__(self, Window: customtkinter.CTk):
        self.Textbox = customtkinter.CTkTextbox(Window, height=720, width=650)
        self.Textbox.insert(0.0,'.main\n\tMOV S0, "Hello, World!"\n\tPRT S0\n\tJMP .label\n.label\n\tMOV S0, "Stupid"\n\tPRT S0')
        self.Textbox.grid(column=1, row=1)

        self.Label = customtkinter.CTkLabel(Window, height=100, width=650, text="Code Editor")
        self.Label.grid(column=1, row=0)

    #Replace text function to make replacing the text of the element streamlined
    def ReplaceText(self, text: str):
        self.Textbox.delete(1.0, "end")
        self.Textbox.insert(0.0, text)

    def GetText(self):
        return self.Textbox.get(0.0, "end")

class HelpMenu(customtkinter.CTkToplevel):
    def __init__(self, Window: customtkinter.CTk, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configure(height=700, width=1080)
        self.Textbox = customtkinter.CTkTextbox(self, height=600, width=1080)
        self.Textbox.grid(column=0, row=1, sticky="nsew")
        self.Textbox.insert(0.0,
                            "This menu will show the registers and Operators, their binary translations and their purpose.\n\n" +
                            "Registers:\n" +
                            "A0, 00000000: Stores the result of logical operations\n" +
                            "R0 - R8, 00000001 - 00001001: General Purpose Registers\n" +
                            "S0 - S4, 00001010 - 00001110: Stores string values\n\n" +
                            "Operations:\n" +
                            "Address Mode Note: Some functions support the use of multiple Address Modes\n001: Memory Location, 010: Constant Number, 011: Constant String, 100: Register Value\n"
                            "LDR [Register], [Memory Address] | 00001100 - Loads a value from the memory address specified into the specified Register\n" +
                            "STR [Register], [Memory Address] | 00010100 - Stores a value from the specified Register into the specified memory address\n" +
                            "ADD [Register1], [Register2] | 00011100 - Adds the value from Register2 to Register1 and stores in Register A0\n" +
                            "SUB [Register1], [Register2] | 00100100 - Subtracts the value in Register2 from Register1 and stores in Register A0\n" +
                            "MUL [Register1], [Register2] | 00101100 - Multiplies the value in Register1 by Register2 and stores in Register A0\n" +
                            "DIV [Register1], [Register2] | 00110100 - Divides the value in Register1 by Register2 and stores in Register A0\n" +
                            "MOV [Register], [Operand] | 00111100 (Supports 010, 011 and 001) - Copies the value in Operand and stores in Register\n" +
                            "CMP [Register], [Operand] | 01000100 (Supports 010, 011 and 001) - Compares the value in Operand to Register and sets a condition flag based on the result\n" +
                            "JMP [Label] | 01001011 - Jumps to the Section with the same name as [Label]\n" +
                            "JEQ [Label] | 01010011 - Jumps to the Section with the same name as [Label] if the previous comparison was Equal\n" +
                            "JNE [Label] | 01011011 - Jumps to the Section with the same name as [Label] if the previous comparison was anything other than Equal\n" +
                            "JGT [Label] | 01100011 - Jumps to the Section with the same name as [Label] if the previous comparison was Greater Than\n" +
                            "JLT [Label] | 01101011 - Jumps to the Section with the same name as [Label] if the previous comparison was Less Than\n" +
                            "AND [Register], [Operand] | 01110 011 (Supports 010, 011 and 001) - Performs a Bitwise AND Operation on the value held in [Register] and [Operand] and stores in Register A0\n" +
                            "ORR [Register], [Operand] | 01111 011 (Supports 010, 011 and 001) - Performs a Bitwise OR Operation on the value held in [Register] and [Operand] and stores in Register A0\n" +
                            "XOR [Register], [Operand] | 10000 011 (Supports 010, 011 and 001) - Performs a Bitwise XOR Operation on the value held in [Register] and [Operand] and stores in Register A0\n" +
                            "NOT [Register] | 10001 100 - Performs a Bitwise NOT Operation on the value held in [Register] and stores in Register A0\n" +
                            "LSL [Register], [Operand] | 10010 011 (Supports 010, 011 and 001) - Performs a Logic Shift to the left on the value held in [Register] by [Operand] and stores in Register A0\n" +
                            "LSR [Register], [Operand] | 10011 011 (Supports 010, 011 and 001) - Performs a Logic Shift to the right on the value held in [Register] by [Operand] and stores in Register A0\n" +
                            "PRT [Operand] | 10100 011 (Supports 010, 011 and 001) - Outputs the value in [Operand] to the Terminal\n" +
                            "RET | 10101 - Sends program execution back to the previous Section that called the section it is in\n" +
                            "HALT | 10110 - Ends program execution\n" +
                            "ORD [Value] | Terminal Only. - Returns the ASCII Codes of each character in a provided string."
                            )
        self.Textbox.configure(state='disabled')
        self.Label = customtkinter.CTkLabel(self, height=30, width=1080, text="Help")
        self.Label.grid(column=0, row=0, sticky="nsew")

#The main app class, this is the main window that opens when the program starts.
class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        #Getting the monitor width (usually the active monitor)
        Width = 1080
        Height = 720

        # Adding Display and Interactable Widgets
        menu = tkinter.Menu(self)
        self.registerdisplay = RegisterDisplay(self)
        self.codeeditor = FileEditor(self)
        self.terminal = Terminal(self)
        self.geometry(f"{Width}x{Height}")
        self.title("XASM Assembler")
        self.configure(menu=menu)

        #Export and Execution menu options
        expmenu = tkinter.Menu(menu)
        runmenu = tkinter.Menu(menu)

        # 'Upload' and 'Run as' Buttons set up
        menu.add_command(label="Upload", command=self.upload_file)
        menu.add_cascade(label="Export as...", menu=expmenu)
        menu.add_cascade(label="Run as...", menu=runmenu)
        menu.add_command(label="Help", command=self.Help_menu)
        expmenu.add_command(label="XASM", command=self.export_xasm_file)
        #expmenu.add_command(label="x86-64")
        expmenu.add_command(label="XMC", command=self.export_xmc_file)
        runmenu.add_command(label="XASM", command=self.run_xasm_file)
        runmenu.add_command(label="XMC", command=self.run_xmc_file)

        # App Configurations
        customtkinter.set_appearance_mode("dark")
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)

    #Open the Help Menu
    def Help_menu(self):
        helpmenu = HelpMenu(self)
        helpmenu.focus()

    #Runs when the Upload button is used                                                                                                                
    #Reads the data from the given .xasm or .xmc file and loads the contents into the code editor
    def upload_file(self):
        global UploadPath
        UploadPath = filedialog.askopenfilename(filetypes=[("XASM Files", "*.XASM"), ("XMC Files", "*.XMC")])
        OutputText = ""
        with open(UploadPath, 'r') as File:
            FileText = File.readlines()
            for Line in FileText:
                OutputText += Line + "\r"
        self.codeeditor.ReplaceText(OutputText)

    def run_xasm_file(self):
        Assembler.init()
        self.codeeditor.Textbox.configure(state="disabled")
        Focus = 0
        CallLabel = ""
        Sections = Assembler.GetSections(self.codeeditor.Textbox.get(0.0, "end"))
        if Sections:
            for Section in Assembler.Sections:
                if Section.SectionLabel == "main":
                    Focus = Assembler.Sections.index(Section)
                    print("Main Found")
                    print(Assembler.Sections)
                elif Section.SectionLabel == "Section1":
                    print("Section 1 Found")
                    Focus = Assembler.Sections.index(Section)

            i = 0
            while i < len(Assembler.Sections[Focus].Instructions):

                Output = Assembler.Sections[Focus].Instructions[i].Execute()
                if isinstance(Output, int):
                    Output = str(Output)
                if "|::|" in Output:
                    pass
                elif "!::!" in Output:
                    self.terminal.Frame.AppendText(Output)
                    break
                elif Output[0] == ".":
                    Found = False
                    for Section in Assembler.Sections:
                        if Section.SectionLabel == Output[1:]:
                            print("Focus Shifted")
                            CallLabel = Assembler.Sections[Focus].SectionLabel
                            Focus = Assembler.Sections.index(Section)
                            Found = True
                            i = -1
                            time.sleep(0.2)
                            break
                    if not Found:
                        self.terminal.Frame.AppendText("Invalid Label " + Output)
                elif Output[0] == "|^^|":
                    Focus = Assembler.Sections.index(CallLabel)
                    i = -1
                    time.sleep(0.2)
                else:
                    self.terminal.Frame.AppendText(Output)
                self.registerdisplay.Frame.UpdateRegisterAndMemory()
                self.update()
                time.sleep(0.2)
                i += 1
        self.codeeditor.Textbox.configure(state="normal")

    def run_xmc_file(self):
        Assembler.init()
        self.codeeditor.Textbox.configure(state="disabled")
        Sections = Assembler.GetSections(self.codeeditor.Textbox.get(0.0, "end"))
        ConvertedSections = []
        Focus = 0
        CallLabel = ""
        if Sections:
            for Section in Assembler.Sections:
                SectionLabel, SectionData = Converter.ConvertSection("." + Section.SectionLabel, Section.Instructions)
                XMLines = []
                for Instruction in SectionData:
                    XMLines.append(Assembler.GetXSMLine(Instruction))
                ConvertedSections.append(Assembler.SectionData(SectionLabel,len(SectionData) , XMLines))

        for Section in ConvertedSections:
            if Section.SectionLabel == "main":
                Focus = ConvertedSections.index(Section)
                print("Main Found")
                print(ConvertedSections)
            elif Section.SectionLabel == "Section1":
                print("Section 1 Found")
                Focus = ConvertedSections.index(Section)

        i = 0
        while i < len(ConvertedSections[Focus].Instructions):

            Output = ConvertedSections[Focus].Instructions[i].Execute()
            if isinstance(Output, int):
                Output = str(Output)
            if "|::|" in Output:
                pass
            elif "!::!" in Output:
                self.terminal.Frame.AppendText(Output)
                break
            elif Output[0] == ".":
                Found = False
                for Section in ConvertedSections:
                    if Section.SectionLabel == Output[1:]:
                        print("Focus Shifted")
                        CallLabel = ConvertedSections[Focus].SectionLabel
                        Focus = ConvertedSections.index(Section)
                        Found = True
                        i = -1
                        time.sleep(0.2)
                        break
                if not Found:
                    self.terminal.Frame.AppendText("Invalid Label " + Output)
            elif Output[0] == "|^^|":
                Focus = ConvertedSections.index(CallLabel)
                i = -1
                time.sleep(0.2)
            else:
                self.terminal.Frame.AppendText(Output)
            self.registerdisplay.Frame.UpdateRegisterAndMemory()
            self.update()
            time.sleep(0.2)
            i += 1
        print(ConvertedSections)

    def export_xasm_file(self):
        global UploadPath
        UploadPath = filedialog.asksaveasfile(filetypes=[("XASM Files", "*.xasm")])
        FileText = self.codeeditor.GetText()
        with open(UploadPath.name, "w") as f:
            f.write(FileText)

    def export_xmc_file(self):
        AcceptedCharacters = ["0", "1", ".", "-", "\n", "\t", " "]
        FileText = self.codeeditor.GetText()

        if not set(list(FileText)).issubset(set(AcceptedCharacters)):
            self.terminal.Frame.AppendText("Invalid XMC File")
        else:
            global UploadPath
            UploadPath = filedialog.asksaveasfile(filetypes=[("XMC Files", "*.xmc")])
            with open(UploadPath.name, "w") as f:
                f.write(FileText)

app = App()
app.mainloop()