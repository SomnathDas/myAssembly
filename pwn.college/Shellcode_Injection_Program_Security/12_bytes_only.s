.global _start
_start:
.intel_syntax noprefix
	mov al, 0x5a
	shr esi, 0x3c
	push 0x66
	mov rdi, rsp
	syscall
