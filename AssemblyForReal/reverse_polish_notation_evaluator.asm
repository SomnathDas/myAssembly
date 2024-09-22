;
; A program which will evaluate RPN expressions
; Reverse Polish Notation (RPN or Łukasiewiczian notation) is a way to specify arithmetical sums.
; Written by Somnath
; Disclaimer :: My code is shit.
;

;
; Commands to assemble and run ::
; 1. nasm -f elf64 rpn.asm -o rpn.o
; 2. ld -A elf_x86_64 -no-pie rpn.o --entry main -o rpn
;

section .bss
	fileContent: RESB 1000000

section .data
	pathName DD "/home/kali/0DE5/0x06/input";

section .text
global main

main:
	call _read; output in $rax
	mov r13, 0; counter
	mov r15, rax;
	call _go_through_byte; output (result) in $rax
	jmp _exit;

; Main logic :: goes through each byte and operates accordingly
_go_through_byte:
	; switches
	mov r8, 0; switch for is_number
	mov r9, 0; switch for is_number
	mov r10, 0; switch for is_operator
	mov r11, 0; holder for operator
	; pointing to the byte
	mov rcx, [r15+r13];
	inc r13;
	; "cl" contains byte of our input
	; if byte is an integer
	call _set_r8;
	call _set_r9;
	jmp _is_number;

	; if byte is an operator
	_check_operator:
		call _set_r10;
	jmp _is_operator;

	_check_nul:
		; if end of input i.e null byte
		cmp cl, 0x00; 
		jne _go_through_byte;

	pop rax;
	ret;

_set_r8:
	cmp cl, 0x30;
	jge _set_r8_true;
	_set_r8_false:
		mov r8, 0;
		ret;
	_set_r8_true:
		mov r8, 1;
		ret;

_set_r9:
	cmp cl, 0x39;
	jle _set_r9_true;
	_set_r9_false:
		mov r9, 0;
		ret;
	_set_r9_true:
		mov r9, 1;
		ret;

_is_number:
	and r8, r9;
	cmp r8, 1;
	je _is_number_true;
	_is_number_false:
		jmp _check_operator;
	_is_number_true:
		mov rdx, 0;
		add dl, cl;
		sub rdx, 0x30;
		push rdx;

		jmp _check_nul;

_set_r10:
	cmp cl, 0x2b; ( + )
	mov r11, 0x2b; operator = +
	je _set_r10_true;
	cmp cl, 0x2d; ( - )
	mov r11, 0x2d; operator = -
	je _set_r10_true;
	cmp cl, 0x2a; ( * )
	mov r11, 0x2a; operator = *
	je _set_r10_true;
	cmp cl, 0x2f; ( / )
	mov r11, 0x2f; operator = /
	je _set_r10_true;
	_set_r10_false:
		mov r11, 0; operator = 0x00
		mov r10, 0;
		ret;
	_set_r10_true:
		mov r10, 1;
		ret;


_is_operator:
	and r10, 1;
	cmp r10, 1;
	je _is_operator_true;
	_is_operator_false:
		jmp _check_nul;
	_is_operator_true:
		pop r12;
		pop r14;
		
		cmp r11, 0x2b;
		je _to_add;
		cmp r11, 0x2d;
		je _to_sub;
		cmp r11, 0x2a;
		je _to_mul;
		cmp r11, 0x2f;
		je _to_div

		_to_add:
			add r12, r14;
			push r12;
			jmp _check_nul;
		_to_sub:
			sub r14, r12;
			push r14;
			jmp _check_nul;
		_to_mul:
			mov rax, r12;
			mov rdx, r14;
			mul rdx;
			mov r12, rax;
			push r12;
			jmp _check_nul;
		_to_div:
			mov rax, r14;
			mov rcx, r12;
			mov rdx, 0;
			div rcx;
			mov r12, rax;
			push r12;
			jmp _check_nul;

		jmp _check_nul;

; Procedure to read the "input" file
_read:
	push rbp;
	mov rbp, rsp;
	
	mov rax, 0x02;
	mov rdi, pathName;
	mov rsi, 0x00;
	syscall;

	mov rdi, rax;
	mov rax, 0x00;
	mov rsi, fileContent;
	mov rdx, 1000000;
	syscall;

	mov rax, rsi;

	pop rbp;
	ret;

; Procedure to exit
_exit:
	mov rax, 60;
	mov rdi, 0;
	syscall;