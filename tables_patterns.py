
c_arithmetic_pattern = "(add|sub|neg|eq|gt|lt|and|or|not)"
mem_seg_pattern = "(local|argument|this|that|constant|static|temp|pointer)"
index_pattern = "(\d+)"
c_push_pattern = "^(push)\s{1}" + mem_seg_pattern + "{1}\s{1}" + index_pattern
c_pop_pattern = "^(pop)\s{1}" + mem_seg_pattern + "{1}\s{1}" + index_pattern

c_label_pattern = "^(label)\s{1}" + label_function_name
c_goto_pattern = "^(goto)\s{1}" + label_function_name
c_if_pattern = "^(if-goto)\s{1}" + label_function_name #if-goto
c_function_pattern = "^(function)\s{1}" + label_function_name + "\s{1}(\d+)"
c_return_pattern = "^(return)"
c_call_pattern = "^(call)\s{1}" + label_function_name + "\s{1}(\d+)" #should we keep track of
#the functions in the current scope
                                #so that we know what are valid calls?

label_function_name = "((?![0-9])[\w._:]*)"
comment_pattern = "^(\/\/).*"

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
    "eq" : "\n@R15\nM=D\nD=-1\n@R15\nD=D&M\n@EQEQ\nD;JEQ\n@PUSH2STACKEQ\nD;J\n(EQEQ)\nD=-1\n@PUSH2STACKEQ\nD;J\n(PUSH2STACKEQ)\n" + d_push + "\n",

    "gt" : "\n" + d_pop + "\n@SP\nM=M-1\nM=M-D\nD=M\n@GTGT\nD;JGT\n@PUSH2STACKGT\nD=0;J\n(GTGT)\nD=-1\n@PUSH2STACKGT\nD;J\n(PUSH2STACKGT)\n" + d_push + "\n",

    "lt" : "\n" + d_pop + "\n@SP\nM=M-1\nM=M-D\nD=M\n@LTLT\nD;JLT\n@PUSH2STACKLT\nD=0;J\n(LTLT)\nD=-1\n@PUSH2STACKLT\nD;J\n(PUSH2STACKLT)\n" + d_push + "\n",

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

flowControlTable = {
"""
For our implementation, @* will be the placeholder for the label name
"""

    "goto" : "\n@*\n0;J\n"
    "if-goto" : d_pop + "\n@*\nD;JNE\n"
}
