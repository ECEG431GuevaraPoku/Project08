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
        path = ""
        if os.path.isdir(arg_file+"/"):
            #print("WE GOT A DIRECTORY\n")
            #out_file = arg_file.strip(".vm") + ".asm"
            out_file = arg_file.strip(".vm")
            #out_file = out_file + "/" + out_file
            if os.path.exists(out_file + ".asm"):
                #might stop removing it completely
                os.remove(out_file)
            dir_list =  os.listdir(arg_file+"/")
            print(dir_list)
            """
            with os.scandir(arg_file+"/") as entries:
                for entry in entries:
                    if fileIsVM(entry.name):
                        #file_name =
                        parser = Parser(entry.path, out_file)
                        parser.advance()
            """
            if "Sys.vm" in dir_list:
                path = arg_file + "/Sys.vm"
                abspath = os.path.abspath(path)
                parser = Parser(abspath, out_file)
                parser.advance()
                dir_list.remove("Sys.vm")
            for entry in dir_list:
                if fileIsVM(entry):
                    #file_name =
                    path = arg_file + "/" + entry
                    abspath = os.path.abspath(path)
                    parser = Parser(abspath, out_file)
                    parser.advance()
        elif os.path.exists(arg_file) and fileIsVM(arg_file):
            #print("WE GOT A FILE\n")
            #out_file = arg_file.strip(".vm") + ".asm"
            out_file = arg_file.strip(".vm")
            if os.path.exists(out_file + ".asm"):
                os.remove(out_file)
            parser = Parser(arg_file, out_file)
            parser.advance()
        else:
            sys.exit("Path does not exist or filetype is incorrect\n")
            #Maybe add something so we know which it is

if __name__ == '__main__':
    main()
