@0
D=M
@a
M=D

@1
D=M
@b
M=D

@0
D=A
@sum
M=D

(LOOP)
@a
D=M
@SET
D;JEQ
@b
D=M
@sum
M=D+M
@a
M=M-1
@LOOP
0;JMP

(SET)
@sum
D=M
@2
M=D
@END
0;JMP


(END)
@END
0;JMP
