from tables_patterns import *

class CodeWriter:

    def __init__(self, filename):
        self.fileString = filename.split(".")[0]
        self.out_file = open(filename, 'a+')
        self.function_name = ""

    def setFunctionName(self, function_name):
        """
        If there is a function command or a call command, we update the function name for the
        coder
        """
        self.function_name = function_name


    def writeArithmetic(self, command):
        assembly_encoding = arithmeticSymbolTable[command]
        self.out_file.write(assembly_encoding)

    def writePushPop(self, command, segment, index, command_type):
        if segment == "temp":
            index = index + 5
        elif segment == "pointer":
            index = index + 3

        if command_type == "C_PUSH":
            partial_enconding = pushMemSeg[segment]
        elif command_type == "C_POP":
            partial_enconding = popMemSeg[segment]
        assembly_encoding = self.insertIndex(partial_enconding, str(index))
        self.out_file.write(assembly_encoding)

    def insertIndex(self, code, i):
        return code.replace("_", i)

    def close(self):
        self.out_file.close()

    """
    Project 08 Additions
    """
    def writeInit(self):
        #write the bootstrap code here
        pass

    def writeLabel(self, label):
        #Write the code corresponding to vm label command
        label_array = label.split()
        label_name = label_array[1]
        label_name = "(" + self.getFullFunctionName() + "$" + label_name + ")"
        self.out_file.write(label_name)

    def writeGoto(self, label):
        label_array = label.split()
        label_name = label_array[1]
        label_name = self.getFullFunctionName() + "$" + label_name
        goto_encoding = flowControlTable["goto"]
        goto_encoding = goto_encoding.replace("*", label_name)
        self.out_file.write(goto_encoding)

    def writeIf(self, label):
        label_array = label.split()
        label_name = label_array[1]
        label_name = self.getFullFunctionName() + "$" + label_name
        if_encoding = flowControlTable["if-goto"]
        if_encoding = goto_encoding.replace("*", label_name)
        self.out_file.write(if_encoding)

    def writeFunction(self):
        pass

    def writeCall(self):
        pass

    def writeReturn(self):
        pass

    def getFullFunctionName(self):
        """
        This is assuming our assumption of setting the function_name each time we encounter a
        new function is valid
        """
        function_name = self.fileString + "." + self.function_name
        return function_name
