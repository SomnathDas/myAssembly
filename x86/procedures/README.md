# Procedures 
 1. Procedures can be thought of simply as `functions` in x86 assembly

 2. You just define a label like the following:

    ```asm
    addTwo:
    	ADD eax,ebx
    	RET
    ```
    and then use it below in the `main` or `_start` label.

    ```asm
    main:
    	MOV eax,4
    	MOV ebx,1
    	CALL addTwo
    	MOV ebx,eax
    	MOV eax,1
    	INT 80h
    ```

    Okay but when `addTwo` procedure finishes, it just takes us back to where we are supposed to be i.e next line in main: after `CALL addTwo`. 

    __But how?__

3. Data actually exist in the __STACK__.

    In `gdb`:
    You can get `esp` register address -> `info register esp` then
    Do => `x/x [address of esp]`

    Remember that the __Stack Pointer__ is pointing to the current available location at the memory

    When you run the `CALL`, __it places the RETURN address onto the STACK__.

4. Let's think about pushing data into the stack:

    ```asm
    main:
    	PUSH 4
    	PUSH 2
    	CALL addTwo
    	MOV ebx,eax
    	MOV eax,1
    ```

    IN STACK IT LOOKS LIKE FOLLOWING WHEN WE DO PUSH INSTRUCTION:
    ```txt
    ------------
         2
    ------------
         4
    ------------
    ```
    When we `CALL` this `doAdd` function it pushes the return address on the __stack__ as known previously above:

    ```txt
    ------------
    RETURN ADDRESS <------ ESP(Currently)
    ------------
         2
    ------------
         4
    ------------
    ```

    __RETURN ADDRESS__ is the location of next instruction after the `CALL` instruction in the `main` label of the program

    __Stack Pointer (ESP)__ is currently pointing at __RETURN ADDRESS__ that was pushed by the `CALL` instruction.
    
     __How do we get 2 or 4 values in our procedure/function?__

5. The Approach
    
    In our `procedure/function`:

    ```asm
    addTwo:
    	PUSH ebp
    	MOV ebp,esp
    	ADD eax,ebx
    	RET
    ```
    So what is happening here is that we are __PUSHING__ and setting a __BASE POINTER(EBP)__:
    
    ```txt
    ------------
        EBP   <------ ESP(Currently)
    ------------
    RETURN ADDRESS
    ------------
         2
    ------------
         4
    ------------
    ```
    Our Stack Pointer (`ESP`) moves upwards when something gets pushed into the stack, so it now points to `EBP`.

    Then when we set our Base Pointer (`EBP`) :
    ```asm
	    MOV ebp,esp
	```
	
    We are doing this to make sure __both are pointing towards the same address__.

    Now we can reference position with respect to EBP:

    ```txt
    ------------
        EBP   <------ ESP(Currently)
    ------------
    RETURN ADDRESS <---- this address 4 away from EBP
    ------------
         2 <---- this address 8 away from EBP
    ------------
         4 <---- this address 12 away from EBP
    ------------
    ```
    Each `memory slot` is of `4 bytes = 32 bits` remember.

6. So, now if we want to get value of 2 or value of 4, we can do so by following:

    ```asm
    addTwo:
    	PUSH ebp
    	MOV ebp,esp
    	MOV eax,[ebp+8]
    	MOV ebx,[ebp+12]
    	ADD eax,ebx
    	RET
    ```
	
    But there is one problem here and that is:
    Our Stack Pointer (`ESP`) is still pointing at `EBP`, so when this procedure of `addTwo` returns, it will return the address of `EBP`

    To fix this, 
    We just `POP` `EBP` out and hence making our __STACK__ like following:
    ```txt
    ------------
    RETURN ADDRESS <------ ESP(Currently)
    ------------
         2 <---- this address 8 away from EBP
    ------------
         4 <---- this address 12 away from EBP
    ------------
    ```

    ```asm
    addTwo:
    	PUSH ebp
    	MOV ebp,esp
    	MOV eax,[ebp+8]
    	MOV ebx,[ebp+12]
    	ADD eax,ebx
    	POP ebp
    	RET
    ```
    Poping off elements moves `ESP` downwards in the stack and now it is pointing to the __RETURN ADDRESS__ again.


