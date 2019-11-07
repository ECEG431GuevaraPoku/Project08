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
                os.remove(out_file + ".asm")
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
            #coder = CodeWriter(out_file)
            if "Sys.vm" in dir_list:
                coder = CodeWriter(out_file)
                coder.setFunctionName("Sys.init")
                commented_command = "//Set up SP and call sys.init\n"
                coder.write(commented_command)
                coder.write(bootstrap["Sys.init"])
                coder.writeCall("Sys.init", "0", 0)
                coder.write(bootstrap["end"])
                #coder.write("End sys.init\n")
                coder.setDefaultFunctionName()


                path = arg_file + "/Sys.vm"
                abspath = os.path.abspath(path)
                parser = Parser(abspath, coder)
                parser.advance()
                dir_list.remove("Sys.vm")
                print(dir_list)
                parser.coder.close()
            for entry in dir_list:
                coder = CodeWriter(out_file)
                if fileIsVM(entry):
                    print("\nOTHER VM FILE: " + entry + "\n")
                    #file_name =
                    path = arg_file + "/" + entry
                    abspath = os.path.abspath(path)
                    parser = Parser(abspath, coder)
                    parser.advance()
            #os.remove(parser.coder.out_filename)
                parser.coder.close()
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
