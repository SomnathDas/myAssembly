# Calling standard C functions into x86 assembly

- We are going to be running our `object` file created through NASM by GCC. So we need to start global with "main" because we need a main function to work with GCC.

1. For starters:
    ```asm
    global main
    main:
    ```

2. First, we kind-of import it using `extern [function name]`. So for example:

    ```asm
    extern printf
    extern exit
    ```

3. Second, think of argument of these functions and define those arguments in the 
`section .data`

    For example:
    ```asm
    msg DD "Hello World!",0  <--- 0 is null terminator for this string
    fmt DB "Output is: %s",10,0 <--- 10 is used here for newline and 0 is null terminator for this string
    ```
 
4. For our `printf(fmt,msg,...)` function:
 
    Now, we need to push this data into STACK using "PUSH" instruction. Remember, STACK is LIFO (Last-In First-Out) Data structure.

    We push data into stack and then control goes over to C and then it removes data in that LIFO format. 

    So, first arugment of the function is last thing you should push!
    
    ```asm
    main:
	    PUSH msg
	    PUSH fmt
	    CALL printf
    	PUSH 1
	    CALL exit
	```
	
    and like this :)

# To Compile

1. `nasm -f elf -o filename.o filename`
2. `gcc -no-pie -m32 -z noexecstack filename.o -o filename`


# Working with custom C functions

1. First in your `.c` code, make sure you kind-of "export" your function which you want to use in `.asm` program like this:

    ```c
    #include <stdio.h>
    
    extern int myFunc(int,int);
    
    int myFunc(int a, int b) {...}
    ```
    Then you simply import it as stated above!

# COMPILING .asm WITH CUSTOM C

1. `nasm -f elf -o filename.o filename`
2. `gcc -no-pie -m32 -z noexecstack filename.o customFunc.c -o filename`


