- `INT 80h` or `INT 0x80`

    - `INT` => Interrupt Instruction

    - Looks for value in `eax` register which it uses to look-up for which system call to make. For example, It maps value of `1` to `EXIT` syscall

    - And Looks for value in `ebx` register to return after making the system call
