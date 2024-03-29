import re
import os
from tables_patterns import *
from custom_errors import *
from code_writer import *

COMMENT_OR_EMPTY = "COMMENT"
C_ARITHMETIC = "C_ARITHMETIC"
C_PUSH = "C_PUSH"
C_POP = "C_POP"
C_LABEL = "C_LABEL"
C_GOTO = "C_GOTO"
C_IF = "C_IF"
C_FUNCTION = "C_FUNCTION"
C_CALL = "C_CALL"
C_RETURN = "C_RETURN"


class Parser:
	hasMoreCommands = False

	def __init__(self, file_str, coder):
		self.file_str = file_str

		fileArray = self.file_str.split('.', 1)
		self.filename = fileArray[0]
		self.fileType = fileArray[1]
		self.coder = coder
		"""
		*Moved to main file*
		try:
			assert self.fileType == "asm"
		except AssertionError as e:
			#e.args+=("FileTypeError: Expected .asm", self.fileType)
			errorInfo = "\nFileTypeError: Expected .asm | Received ." + self.fileType
			#e.args[0] += errorInfo
			print(errorInfo)
			raise

		self.out_file_str = self.filename + ".hack"
		"""
		# self.out_file_str = out_file_str + ".txt"
		# self.output = out_file_str + ".asm"
		pushMemSeg["static"] = pushStatic(self.filename)
		popMemSeg["static"] = popStatic(self.filename)
		self.variable_address = 16

	def advance(self):
		"""
		Loop through the assembly file and convert each instruction to machine code
		"""
		#path = os.path.realpath(f.name)
		# coder = CodeWriter(self.out_file_str)
		# coder.write(bootstrap["sys.init"])
		# coder.writeCall("sys.init", "0", 0)

		with open(self.file_str, 'r') as in_file:

			line_number = 1
			syntax_error_line = 0

			# coder = CodeWriter(self.out_file_str)
			# coder.setFunctionName("sys.init")
			# commented_command = "//Set up SP and call sys.init\n"
			# coder.write(commented_command)
			# coder.write(bootstrap["sys.init"])
			# coder.writeCall("sys.init", "0", 0)
			# coder.write(bootstrap["end"])
			# #coder.write("End sys.init\n")
			# coder.setDefaultFunctionName()

			for line in in_file:
				syntax_error_line+=1
				command = line.strip()	#remove white space
				try:
					command_type = self.commandType(command)
				except VMSyntaxError as e:
					with open(coder.out_file, 'a+') as out_file:
						#Clear the contents of the hack file from previous assembles
						out_file.truncate(0)
					errorInfo = "\nVM Syntax Error at line " + str(line_number)
					print(errorInfo)
					raise
				else:


					if command_type != COMMENT_OR_EMPTY:
						commented_command = "//" + command + "\n"
						self.coder.write(commented_command)
						if command_type == C_ARITHMETIC:
                            #assembly_encoding = arithmeticSymbolTable[command]
							command = re.search(c_arithmetic, command).group(0)
							self.coder.writeArithmetic(command)
						elif command_type == C_POP or command_type == C_PUSH:

							mem_seg = self.getMemorySegment(command)
							index = self.getMemoryIndex(command)
							self.coder.writePushPop(command, mem_seg, int(index), command_type)

						elif command_type == C_LABEL:
							command_array = command.split()
							label_name = command_array[1]
							self.coder.writeLabel(label_name)

						elif command_type == C_GOTO:
							command_array = command.split()
							label_name = command_array[1]
							self.coder.writeGoto(label_name)

						elif command_type == C_IF:
							command_array = command.split()
							label_name = command_array[1]
							self.coder.writeIf(label_name)

						elif command_type == C_FUNCTION:
							command_array = command.split()
							function_name = command_array[1]
							nVars = command_array[2]
							self.coder.setFunctionName(function_name)
							self.coder.writeFunction(nVars, line_number)

						elif command_type == C_CALL:
							command_array = command.split()
							function_name = command_array[1]
							nArgs = command_array[2]
							self.coder.writeCall(function_name, nArgs, line_number)

						elif command_type == C_RETURN:
							self.coder.writeReturn()

						else:
							#Raise Syntax Error
							pass
						line_number=line_number+1


				"""
				finally:
					coder.close()
				"""
			file_name = self.coder.filename + ".asm"
			in_file = open(self.coder.out_filename, "r")
			out_file = open(file_name, "a+")
			for line in in_file:
				if line.strip():
					out_file.write(line)
			#out_file.flush()
			in_file.close()
			out_file.close()

	def commandType(self, command):
		if re.fullmatch(comment_pattern, command) != None or len(command)==0:
			return COMMENT_OR_EMPTY

		elif re.fullmatch(c_arithmetic_pattern, command) != None:
			return C_ARITHMETIC

		elif re.fullmatch(c_push_pattern, command) != None:
			return C_PUSH
		elif re.fullmatch(c_pop_pattern, command) != None:
			return C_POP
		elif re.fullmatch(c_label_pattern, command) != None:
			return C_LABEL
		elif re.fullmatch(c_goto_pattern, command) != None:
			return C_GOTO
		elif re.fullmatch(c_if_pattern, command) != None:
			return C_IF
		elif re.fullmatch(c_function_pattern, command) != None:
			return C_FUNCTION
		elif re.fullmatch(c_call_pattern, command) != None:
			return C_CALL
		elif re.fullmatch(c_return_pattern, command) != None:
			return C_RETURN
		else:
			print("SYNTAX ERROR WITH COMMAND: " + command + "\n")
			raise VMSyntaxError

	def getMemorySegment(self, command):
		"""
			We'll generalize this to the arg1() function for project 8
		"""
		mem_seg = re.search(mem_seg_pattern, command).group(0)
		return mem_seg

	def getMemoryIndex(self, command):
		"""
			We'll generalize this to the arg2() function for project 8
		"""
		indexStr =  re.search(index_pattern, command).group(0)
		return indexStr
