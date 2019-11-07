//Set up SP and call sys.init

@261
D=A
@SP
M=D

@Sys.init$ret.0
D=A

@SP
A=M
M=D
@SP
M=M+1

@LCL
D=M

@SP
A=M
M=D
@SP
M=M+1

@ARG
D=M

@SP
A=M
M=D
@SP
M=M+1

@THIS
D=M

@SP
A=M
M=D
@SP
M=M+1

@THAT
D=M

@SP
A=M
M=D
@SP
M=M+1

@0
D=A
@5
D=D-A
@SP
D=M-D
@ARG
M=D

@SP
D=M
@LCL
M=D
@SP
M=M-1
@SP
A=M
D=M

@Sys.init
D;JMP

(Sys.init$ret.0)

@Sys.init$ret.0
0;JMP
//function Sys.init 0

(Sys.init)

@0
D=A
@R15
M=D
@R14
M=0

(Sys.init$LOOP.1)
@R14
A=M
D=0

@SP
A=M
M=D
@SP
M=M+1

@R14
M=M+1
@R15
M=M-1
D=M
@Sys.init$LOOP.1
D;JGT
//push constant 4

@4
D=A

@SP
A=M
M=D
@SP
M=M+1

//call Main.fibonacci 1   // computes the 4'th fibonacci element

@Sys.init$ret.3
D=A

@SP
A=M
M=D
@SP
M=M+1

@LCL
D=M

@SP
A=M
M=D
@SP
M=M+1

@ARG
D=M

@SP
A=M
M=D
@SP
M=M+1

@THIS
D=M

@SP
A=M
M=D
@SP
M=M+1

@THAT
D=M

@SP
A=M
M=D
@SP
M=M+1

@1
D=A
@5
D=D-A
@SP
D=M-D
@ARG
M=D

@SP
D=M
@LCL
M=D
@SP
M=M-1
@SP
A=M
D=M

@Main.fibonacci
D;JMP

(Sys.init$ret.3)
//label WHILE
(Sys.init$WHILE)
//goto WHILE              // loops infinitely

@Sys.init$WHILE
0;JMP
//function Main.fibonacci 0

(Main.fibonacci)

@0
D=A
@R15
M=D
@R14
M=0

(Main.fibonacci$LOOP.1)
@R14
A=M
D=0

@SP
A=M
M=D
@SP
M=M+1

@R14
M=M+1
@R15
M=M-1
D=M
@Main.fibonacci$LOOP.1
D;JGT
//push argument 0

@0
D=A
@ARG
A=M+D
D=M


@SP
A=M
M=D
@SP
M=M+1

//push constant 2

@2
D=A

@SP
A=M
M=D
@SP
M=M+1

//lt                     // checks if n<2


@SP
M=M-1
@SP
A=M
D=M

@SP
M=M-1
M=M-D
D=M
@Main.fibonacci$LT
D;JLT
@Main.fibonacci$PUSH2STACKLT
D=0;JMP
(Main.fibonacci$LT)
D=-1
@Main.fibonacci$PUSH2STACKLT
D;JMP
(Main.fibonacci$PUSH2STACKLT)

@SP
A=M
M=D
@SP
M=M+1

//if-goto IF_TRUE

@SP
M=M-1
@SP
A=M
D=M

@Main.fibonacci$IF_TRUE
D;JNE
//goto IF_FALSE

@Main.fibonacci$IF_FALSE
0;JMP
//label IF_TRUE          // if n<2, return n
(Main.fibonacci$IF_TRUE)
//push argument 0

@0
D=A
@ARG
A=M+D
D=M


@SP
A=M
M=D
@SP
M=M+1

//return

@LCL
D=M
@R15
M=D

@5
D=A
@R15
D=M-D
@R14
M=D

@SP
M=M-1
@SP
A=M
D=M

@ARG
M=D

@ARG
D=M+1
@SP
M=D
@R15
D=M-1
@THAT
M=D

@2
D=A
@R15
D=M-1
@THIS
M=D

@3
D=A
@R15
D=M-1
@ARG
M=D

@4
D=A
@R15
D=M-1
@LCL
M=D

@R14
A=M
D;JMP
//label IF_FALSE         // if n>=2, returns fib(n-2)+fib(n-1)
(Main.fibonacci$IF_FALSE)
//push argument 0

@0
D=A
@ARG
A=M+D
D=M


@SP
A=M
M=D
@SP
M=M+1

//push constant 2

@2
D=A

@SP
A=M
M=D
@SP
M=M+1

//sub


@SP
M=M-1
@SP
A=M
D=M

@SP
M=M-1
A=M
D=M-D

@SP
A=M
M=D
@SP
M=M+1
//call Main.fibonacci 1  // computes fib(n-2)

@Main.fibonacci$ret.14
D=A

@SP
A=M
M=D
@SP
M=M+1

@LCL
D=M

@SP
A=M
M=D
@SP
M=M+1

@ARG
D=M

@SP
A=M
M=D
@SP
M=M+1

@THIS
D=M

@SP
A=M
M=D
@SP
M=M+1

@THAT
D=M

@SP
A=M
M=D
@SP
M=M+1

@1
D=A
@5
D=D-A
@SP
D=M-D
@ARG
M=D

@SP
D=M
@LCL
M=D
@SP
M=M-1
@SP
A=M
D=M

@Main.fibonacci
D;JMP

(Main.fibonacci$ret.14)
//push argument 0

@0
D=A
@ARG
A=M+D
D=M


@SP
A=M
M=D
@SP
M=M+1

//push constant 1

@1
D=A

@SP
A=M
M=D
@SP
M=M+1

//sub


@SP
M=M-1
@SP
A=M
D=M

@SP
M=M-1
A=M
D=M-D

@SP
A=M
M=D
@SP
M=M+1
//call Main.fibonacci 1  // computes fib(n-1)

@Main.fibonacci$ret.18
D=A

@SP
A=M
M=D
@SP
M=M+1

@LCL
D=M

@SP
A=M
M=D
@SP
M=M+1

@ARG
D=M

@SP
A=M
M=D
@SP
M=M+1

@THIS
D=M

@SP
A=M
M=D
@SP
M=M+1

@THAT
D=M

@SP
A=M
M=D
@SP
M=M+1

@1
D=A
@5
D=D-A
@SP
D=M-D
@ARG
M=D

@SP
D=M
@LCL
M=D
@SP
M=M-1
@SP
A=M
D=M

@Main.fibonacci
D;JMP

(Main.fibonacci$ret.18)
//add                    // returns fib(n-1) + fib(n-2)


@SP
M=M-1
@SP
A=M
D=M

@SP
M=M-1
A=M
D=M+D

@SP
A=M
M=D
@SP
M=M+1
//return

@LCL
D=M
@R15
M=D

@5
D=A
@R15
D=M-D
@R14
M=D

@SP
M=M-1
@SP
A=M
D=M

@ARG
M=D

@ARG
D=M+1
@SP
M=D
@R15
D=M-1
@THAT
M=D

@2
D=A
@R15
D=M-1
@THIS
M=D

@3
D=A
@R15
D=M-1
@ARG
M=D

@4
D=A
@R15
D=M-1
@LCL
M=D

@R14
A=M
D;JMP
