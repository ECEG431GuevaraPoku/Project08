import os
import sys
from parser import *

def fileIsVM(file_str):
    fileArray = file_str.split('.', 1)
    fileType = fileArray[1]
    if fileType == "vm":
        return True
    else:
        return False

def main():

    for arg_file in sys.argv[1:]:
        if os.path.isdir(arg_file+"/"):
            #print("WE GOT A DIRECTORY\n")
            #out_file = arg_file.strip(".vm") + ".asm"
            out_file = arg_file.strip(".vm")
            if os.path.exists(out_file):
                #might stop removing it completely
                os.remove(out_file)
            with os.scandir(arg_file+"/") as entries:
                for entry in entries:
                    if fileIsVM(entry):
                        parser = Parser(entry, out_file)
                        parser.advance()
        elif os.path.exists(arg_file) and fileIsVM(arg_file):
            #print("WE GOT A FILE\n")
            #out_file = arg_file.strip(".vm") + ".asm"
            out_file = arg_file.strip(".vm")
            if os.path.exists(out_file):
                os.remove(out_file)
            parser = Parser(arg_file, out_file)
            parser.advance()
        else:
            sys.exit("Path does not exist or filetype is incorrect\n")
            #Maybe add something so we know which it is

if __name__ == '__main__':
    main()
