.global _start
_start:
.intel_syntax noprefix
	xor edi, edi
	mov esi, edx
	syscall
