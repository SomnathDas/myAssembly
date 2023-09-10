section .data

section .text
 global main

 doAdd:
	ADD eax,ebx
	RET

 main:
	MOV eax,4
	MOV ebx,2
	CALL doAdd
	MOV ebx,eax
	MOV eax,1
	INT 80h
