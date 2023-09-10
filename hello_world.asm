extern exit
extern printf

section .data
	msg DD "Hello, World!",0
	fmt DD "%s",0

section .text
 global main

 main:
	PUSH msg
	PUSH fmt
	CALL printf
	PUSH 1
	CALL exit
