;
; nasm -o main.o main.asm -f elf64
; gcc -no-pie -z noexecstack main.o -o main
; :: Solution For ::
; https://www.hackerrank.com/challenges/breaking-best-and-worst-records
;
; r9 -> no. of times breaking most points records
; r8 -> no. of times breaking least points records. 
;

section .bss

section .data
	scores DQ 3,4,21,36,10,28,35,5,24,42;

section .text
global main

main:
	mov rbx, [scores]; min
	mov rcx, [scores]; max
	mov r8, 0; minRec
	mov r9, 0; maxRec
	mov r10, 0; ix
	jmp iterate;

iterate:
	cmp r10, 80; no of elements in a list times 8 bytes
	je final;
	mov r11, [scores+r10]; score
	add r10, 8;
	cmp r11, rbx; score < min
	jl if_score_is_less;
	cmp r11, rcx; score > max
	jg if_score_is_greater;
	jmp iterate;

if_score_is_less:
	mov rbx, r11;
	inc r8;
	jmp iterate;

if_score_is_greater:
	mov rcx, r11;
	inc r9;
	jmp iterate;

final:
	mov rax, 60;
	mov rdi, 0;
	syscall;
