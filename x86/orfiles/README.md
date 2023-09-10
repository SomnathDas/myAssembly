# System calls for opening and reading files


- Resources:
    `x86` System Call Table:
    https://faculty.nps.edu/cseagle/assembly/sys_call.html

    `open()` System Call:
    https://man7.org/linux/man-pages/man2/open.2.html
    https://sites.uclouvain.be/SystInfo/usr/include/bits/fcntl.h.html

1. So `INT` instruction will be the star of this show.

    We've been using `INT 80h` all along to trigger a `system call`,
    `exit()` syscall mostly by setting: 
    ```asm
    MOV eax,1
    MOV ebx,1
    ```
    where `eax` represented the __syscall code__ and `ebx` as __return value__.

2. For opening and reading file as per according to the resources mentioned, we have to first set `eax` to `5` so that `INT 80h` instruction calls the `sys_open` syscall.

    ```asm
    MOV eax,5
    ```
    Now from `manpage` of `open()` sys call, argument required are:
    
    1. `pathname`.
    2. `flags`.
    3. `mode_t` __(optional)__ which dictates if a file is not there and is created then with what permissions is that created.

    Let's focus on `pathname` and `flags` arguments:
    ```asm
    section .data
    	pathname DD "/home/user/code/asm/hello"
    ```
    and moving `pathname` address in the `ebx` register in main:
    ```asm
    MOV ebx,pathname
    ```
    
3. Next we need to put `flags` but we know these `flags` are defined __CONSTANTS__ in c-lang but since we are working with assembly, we will go to fcntl(2) file from manpage site https://sites.uclouvain.be/SystInfo/usr/include/bits/fcntl.h.html

4. Now we need `O_RDONLY` flag to simply... read only our file!

    Its numeric equivalent is `0` and therefore `ecx` (why ecx? look up at syscall table from resources) needs to be set `0`

    ```asm
    MOV ecx,0
    ```
    
    Now, when `INT` instruction is fired and system call of open is made, the result of that system call will be stored in `eax` register and that will be an integer. 
    
    Here that integer is the __file descripter unique-id__ which is in the __file discripter table__ where this __id__ is associated with the file which we just opened.

    Complete Code at this point:

    ```asm
    section .data
    	pathname DD "/home/user/code/asm/hello"
    
    section .bss
    
    section .text
     global main
    
     main:
    	MOV eax,5
    	MOV ebx,pathname
    	MOV ecx,0
    	INT 80h
    ```

- In `gdb` : `x/2s [address]` to view our `pathname` string.

__Congrats!__ 
Now we have opened the file and got the file descripter id to access it. __So let's read it!__

5. Same process, we gonna look at `x86` assembly table and manpage of `read()` system-call.

    `eax` needs to be set to 3 for `read()` syscall to trigger by `INT 80h` instruction
    `ebx` needs to be set to `file descripter id `
    `ecx` needs to be set to `buffer` ( which we will allocate in .bss section as reserved space )
    `edx` needs to be `set to size of that buffer` (bytes you are going to read from the file)

    ```asm
    MOV ebx,eax (moving previously got file discriptor id to ebx)
    MOV eax,3 
    ```

    Since we know our `hello` file is that of around `76bytes`, we can safely reserve `256 bytes` in `.bss` section memory for buffer.

    ```asm
    section .bss
    	buffer: resb 256
    
    MOV ecx,buffer
    MOV edx,256
    INT 80h
    ```

    and boom!
    
    Remember, your data which you read from the file is stored in the `buffer` which we set to `memory address` of the `buffer` in the `ecx` register.

