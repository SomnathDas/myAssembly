section .data
	num DB 1
	num2 DB 2

section .text
 global _start

 _start:
	MOV ebx,[num] // fix use bl and cl
	MOV ecx,[num2]
	MOV eax,1
	INT 80h
