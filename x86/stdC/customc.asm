extern doAdd
extern exit

section .data

section .text
 global main

 main:
	PUSH 2
	PUSH 1
	CALL doAdd
	PUSH eax

 end:
	CALL exit
