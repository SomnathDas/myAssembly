extern printf
extern exit

section .data
	msg1 DD "Hello, World!",0
	msg2 DD "Working with .asm",0
	fmt DD "%s : %s",10,0

section .text
 global main

 main:
	PUSH msg2
	PUSH msg1
	PUSH fmt
	CALL printf
	PUSH 1
	CALL exit
	
