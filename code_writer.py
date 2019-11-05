from tables_patterns import *

class CodeWriter:

    def __init__(self, filename):
        self.fileString = filename.split(".")[0].split("/")[-1]
        self.out_file = open(filename, 'a+')
        #self.function_name = self.fileString + default_function

    def setDefaultFunctionName(self):
        self.function_name = self.fileString + ".default"

    def setFunctionName(self, function_name):
        """
        If there is a function command or a call command, we update the function name for the
        coder
        """
        self.function_name = function_name


    def writeArithmetic(self, command):
        assembly_encoding = arithmeticSymbolTable[command]
        if command == "eq":
            eq_label = self.function_name + "$EQEQ"
            push_label = self.function_name + "$PUSH2STACKEQ"
            assembly_encoding = assembly_encoding.replace("~", eq_label)
            assembly_encoding = assembly_encoding.replace("*", push_label)
        elif command == "gt":
            gt_label = self.function_name + "$GTGT"
            push_label = self.function_name + "$PUSH2STACKGT"
            assembly_encoding = assembly_encoding.replace("~", gt_label)
            assembly_encoding = assembly_encoding.replace("*", push_label)
        elif command == "lt":
            lt_label = self.function_name + "$LT"
            push_label = self.function_name + "$PUSH2STACKLT"
            assembly_encoding = assembly_encoding.replace("~", lt_label)
            assembly_encoding = assembly_encoding.replace("*", push_label)
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
    def write(self, input):
        self.out_file.write(input)

    def writeInit(self):
        #write the bootstrap code here
        pass

    def writeCommand(self, command):
        """
        """
        comment = "//" + command
        self.out_file.write(comment)

    def writeLabel(self, label):
        #Write the code corresponding to vm label command
        """
        label_array = label.split()
        label_name = label_array[1]
        #label_name = "(" + self.getFullFunctionName() + "$" + label_name + ")"
        label_name = self.function_name + "$" + label_name
        """
        label_name = self.createLabel(label, self.function_name)
        label_name = "(" + label_name + ")\n"
        self.out_file.write(label_name)

    def writeGoto(self, label):
        """
        label_array = label.split()
        label_name = label_array[1]
        #label_name = self.getFullFunctionName() + "$" + label_name
        label_name = self.function_name + "$" + label_name
        """
        label_name = self.createLabel(label, self.function_name)
        goto_encoding = flowControlTable["goto"]
        goto_encoding = goto_encoding.replace("*", label_name)
        self.out_file.write(goto_encoding)

    def writeIf(self, label):
        """
        label_array = label.split()
        label_name = label_array[1]
        label_name = self.function_name + "$" + label_name
        """
        label_name = self.createLabel(label, self.function_name)
        if_encoding = flowControlTable["if-goto"]
        if_encoding = if_encoding.replace("*", label_name)
        self.out_file.write(if_encoding)

    def writeFunction(self, nVars, line_number):
        """
        Using # instead of $ for our predefined labels. Why? I have no idea
        """
        loop_label_name = self.function_name + "$LOOP." + str(line_number)

        function_encoding = flowControlTable["function"]
        function_encoding = function_encoding.replace("*", loop_label_name)
        function_encoding = function_encoding.replace("_", nVars)
        self.out_file.write(function_encoding)


    def writeCall(self, function_name, nArgs, line_number):
        """
        Using # instead of $ for our predefined labels. Why? I have no idea
        Nvm I changed that
        """
        return_label = self.function_name + "$ret." + str(line_number)
        call_encoding = flowControlTable["call"]
        call_encoding = call_encoding.replace("*", return_label)
        call_encoding = call_encoding.replace("_", nArgs)
        call_encoding = call_encoding.replace("~", function_name)

        self.out_file.write(call_encoding)

    def writeReturn(self):

        return_encoding = flowControlTable["return"]
        self.out_file.write(return_encoding)

    def createLabel(self, label_name, function_name):
        """
        label_array = label.split()
        label_name = label_array[1]
        """
        #label_name = "(" + self.getFullFunctionName() + "$" + label_name + ")"
        label_name = function_name + "$" + label_name
        return label_name

    def getFullFunctionName(self):
        """
        This is assuming our assumption of setting the function_name each time we encounter a
        new function is valid

        UPDATE:
        The function name will already be prepended with the file name
        We'll do this in the compiler front end
        """
        function_name = self.fileString + "." + self.function_name
        return function_name
