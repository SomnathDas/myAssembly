section .data
	pathname DD "/home/somnath/Playgrd/asm/orfiles/hello"

section .bss
	buffer: resb 256

section .text
 global main

 main:
	MOV eax,5
	MOV ebx,pathname
	MOV ecx,0
	INT 80h

	MOV ebx,eax
	MOV eax,3
	MOV ecx,buffer
	MOV edx,256
	INT 80h
	
	MOV eax,1
	MOV ebx,0
	INT 80h
