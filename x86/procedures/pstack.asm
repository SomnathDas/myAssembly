section .data

section .text
 global main

 doAdd:
	PUSH ebp
	MOV ebp,esp
	MOV eax,[ebp+8]
	MOV ebx,[ebp+12]
	POP ebp
	ADD eax,ebx
	RET

 main:
	PUSH 4
	PUSH 2
	CALL doAdd
	MOV ebx,eax
	MOV eax,1
	INT 80h
