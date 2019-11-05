
comment_pattern = "^(\/\/).*"
embedded_comment_pattern = "(\/\/).*"

label_function_name = "((?![0-9])[\w._:]*)"

c_arithmetic_pattern = "(add|sub|neg|eq|gt|lt|and|or|not)"
mem_seg_pattern = "(local|argument|this|that|constant|static|temp|pointer)"
index_pattern = "(\d+)"
c_push_pattern = "^(push)\s{1}" + mem_seg_pattern + "{1}\s{1}" + index_pattern + "{1}\s*(" + embedded_comment_pattern + ")*"
c_pop_pattern = "^(pop)\s{1}" + mem_seg_pattern + "{1}\s{1}" + index_pattern + "{1}\s*(" + embedded_comment_pattern + ")*"

c_label_pattern = "^(label)\s{1}" + label_function_name + "{1}\s*(" + embedded_comment_pattern + ")*"
c_goto_pattern = "^(goto)\s{1}" + label_function_name + "{1}\s*(" + embedded_comment_pattern + ")*"
c_if_pattern = "^(if-goto)\s{1}" + label_function_name  + "{1}\s*(" + embedded_comment_pattern + ")*" #if-goto
c_function_pattern = "^(function)\s{1}" + label_function_name + "\s{1}(\d+){1}\s*(" + embedded_comment_pattern + ")*"
c_return_pattern = "^(return)" + "{1}\s*(" + embedded_comment_pattern + ")*"
c_call_pattern = "^(call)\s{1}" + label_function_name + "\s{1}(\d+){1}\s*(" + embedded_comment_pattern + ")*" #should we keep track of
#the functions in the current scope
                                #so that we know what are valid calls?

"""
Functions that initialize the values for the "static" keys in popMemSeg and pushMemSeg
dictionaries.
They are called with the Parser model
"""
def pushStatic(filename):
    dirArray = filename.split("/")
    var_name = dirArray[-1] +"._"
    asm_code = "\n@" + var_name + "\nD=M\n" + d_push + "\n"
    return asm_code

def popStatic(filename):
    dirArray = filename.split("/")
    var_name = dirArray[-1] +"._"
    asm_code = "\n@" + var_name + "\nD=A\n@R15\nM=D\n" + d_pop + "\n@R15\nA=M\nM=D\n"
    return asm_code

"""
Reusuable assembly instructions for local, argument, this, that
"""
def getMemSegPush(mem_pointer):
    """
    <> is the placeholder for the pointer to the Memory Segment
    """
    s = "\n@_\nD=A\n@<>\nA=M+D\nD=M\n".replace("<>", mem_pointer)
    return s

def getMemSegPop(mem_pointer):
    """
    <> is the placeholder for the pointer to the Memory Segment
    """
    s = "\n@_\nD=A\n@<>\nA=M+D\nD=A\n".replace("<>", mem_pointer)
    return s

store_pointer = "\n@R15\nM=D\n@SP\nD=M\n"
pop_to_memseg = "\n@R15\nA=M\nM=D\n"

"""
Generic strings for pushing and popping to D register as intermediary for
pushing and popping with mem segments
"""
d_push = "\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"
d_pop = "\n@SP\nM=M-1\n@SP\nA=M\nD=M\n"

"""
Symbol table for arithmetic and logical operations.
Arithmetic and logical operations all go through the stack for operands.
"""
arithmeticSymbolTable = {

    'add' : "\n" + d_pop + "\n@SP\nM=M-1\nA=M\nD=M+D\n" + d_push,

    "sub" : "\n" + d_pop + "\n@SP\nM=M-1\nA=M\nD=M-D\n" + d_push,

    "neg" : "\n" + d_pop + "\nD=-D\n" + d_push + "\n",

    #You could probably implement eq with just subtraction?
    #if D==0, D-0==0
    #if D!=0, D-0==D
    "eq" : "\n@R15\nM=D\nD=-1\n@R15\nD=D&M\n@~\nD;JEQ\n@*\nD;JMP\n(~)\nD=-1\n@*\nD;J\n(*)\n" + d_push + "\n",

    "gt" : "\n" + d_pop + "\n@SP\nM=M-1\nM=M-D\nD=M\n@~\nD;JGT\n@*\nD=0;J\n(~)\nD=-1\n@*\nD;JMP\n(*)\n" + d_push + "\n",

    "lt" : "\n" + d_pop + "\n@SP\nM=M-1\nM=M-D\nD=M\n@~\nD;JLT\n@*\nD=0;J\n(~)\nD=-1\n@*\nD;JMP\n(*)\n" + d_push + "\n",

    "and" : "\n" + d_pop + "\n@SP\nM=M-1\nM=M&D\nD=M\n@SP\nM=M+1\n",

    "or" : "\n" + d_pop + "\n@SP\nM=M-1\nM=M|D\nD=M\n@SP\nM=M+1\n",

    "not" : "\n" + d_pop + "\nD=!D\n" + d_push + "\n"
}

'''
For our implementation, @_ will be the placeholder for the first operand. We'll then use the string replace function to input the
actual values.
'''
popMemSeg = {
    #The first 4 will have the same generic format
    "local" : getMemSegPop("LCL") + store_pointer + d_pop + pop_to_memseg,
    "argument" : getMemSegPop("ARG") + store_pointer + d_pop + pop_to_memseg,
    "this" : getMemSegPop("THIS") + store_pointer + d_pop + pop_to_memseg,
    "that" : getMemSegPop("THAT") + store_pointer + d_pop + pop_to_memseg,

    "constant" : "\n@_\nD=A\n" + d_pop,
    "static" : "",  #This gets initialized by the Parser model
    "temp" : d_pop + "\n@_\nM=D\n",
    "pointer" : d_pop + "\n@_\nM=D\n"

}

pushMemSeg = {
    #The first 4 will have the same generic format
    "local" : getMemSegPush("LCL") + "\n" + d_push + "\n",
    "argument" : getMemSegPush("ARG") + "\n" + d_push + "\n",
    "this" : getMemSegPush("THIS") + "\n" + d_push + "\n",
    "that" : getMemSegPush("THAT") + "\n" + d_push + "\n",

    "constant" : "\n@_\nD=A\n" + d_push + "\n",
    "static" : "",  #This gets initialized by the Parser model
    "temp" : "\n@_\nD=M\n" + d_push + "\n",
    "pointer" : "\n@_\nD=M\n" + d_push + "\n"

}

"""
Variables and functions for function command
"""

saveKandZeroR14 = "\n@_\nD=A\n@R15\nM=D\n@R14\nM=0\n"

"""
Variables and functions for call command
"""
def saveCallerPointer(mem_pointer):
    """
    <> is the placeholder for the pointer to the Memory Segment
    """
    s = "\n@<>\nD=M\n".replace("<>", mem_pointer)
    s += d_push
    return s

push_return_address = "\n@*\nD=A\n" + d_push

reposition_ARG = "\n@_\nD=A\n@5\nD=D-A\n@SP\nD=M-D\n@ARG\nM=D\n"

reposition_LCL = "\n@SP\nD=M\n@LCL\nM=D"

goto_func = d_pop + "\n@~\nD;JMP\n" #if-goto

place_return_label = "\n(*)\n"

"""
Variables and functions for return command
"""
get_endframe = "\n@LCL\nD=M\n@R15\nM=D\n"

get_return_address = "\n@5\nD=A\n@R15\nD=M-D\n@R14\nM=D\n"

reposition_return_val = d_pop + "\n@ARG\nM=D\n"

reposition_caller_SP = "\n@ARG\nD=M+1\n@SP\nM=D"

restore_caller_THAT = "\n@R15\nD=M-1\n@THAT\nM=D\n"

restore_caller_THIS = "\n@2\nD=A\n@R15\nD=M-1\n@THIS\nM=D\n"

restore_caller_ARG = "\n@3\nD=A\n@R15\nD=M-1\n@ARG\nM=D\n"

restore_caller_LCL = "\n@4\nD=A\n@R15\nD=M-1\n@LCL\nM=D\n"

"""
def restoreCallerPointer(mem_pointer):
"""


goto_return_address = "\n@R14\nA=M\nD;J\n"

"""
For our implementation, @* will be the placeholder for the label name, @~ will be the
placeholder function names, and @_ will be the placeholder for numbers

Those will be taken care of in the code_writer
"""
flowControlTable = {
    #label is taken care of in code_writer
    "goto" : "\n@*\n0;JMP\n",
    "if-goto" : d_pop + "\n@*\nD;JNE\n",

    #function: * in function will be replaced with "filename.function_nameLOOP"
    #Need to add unique identifier to the loop label if a function has more than one loop
    "function" : saveKandZeroR14 + "\n(*)\n@R14\nA=M\nD=0\n" + d_push + "\n@R14\nM=M+1\n@R15\nM=M-1\n@*\nD;JNE\n",
    #call: Appending the return label - (return_label) - is done in code_writer
    "call" : push_return_address + saveCallerPointer("LCL") + saveCallerPointer("ARG") + saveCallerPointer("THIS") + saveCallerPointer("THAT") + reposition_ARG + reposition_LCL + goto_func + place_return_label,
    "return" : get_endframe + get_return_address + reposition_return_val + reposition_caller_SP + restore_caller_THAT + restore_caller_THIS + restore_caller_ARG + restore_caller_LCL + goto_return_address

}
