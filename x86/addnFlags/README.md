- `eflags` is a __set of bits__ that represent flags being set.
    
    `PF` - Parity flag -> set if the least-significant byte of the result has an even number of set bits.

    Example:
    `ADD bl,cl` where `bl` is `0b1101` =  `13` and `cl` is `0b0001` = `1`

    Result of this will __not__ set the `PF` parity flag since the result will be `14` = `0b1110` where `3` bits are set and hence number of bits set is odd.
    
    ```txt
      1101
      0001
    + ____
      1110
    ```
    ```txt
   0b0001
   0b0010
  +______
   0b0011 => 3
   ```
   ```txt
  4 bits = 1 hex 
  8 bits = 1 byte = 2 hex
  16 bits = 4 hex
  32 bits = 8 hex
  64 bits = 16 hex
  ```
  
  
 - `IF` - Interrupt Flag -> set to 1 when we allow interrupt to happen in our system. Set in the beginning of the execution.
  
 - `CF` - Carry flag -> If result of previous operation yielded a carry of one. [Also gets set during subtraction as it borrows] 
  
    For example:
    ```asm
    MOV al,0b11111111
    MOV bl,0b0001
    ADD al,bl
    ```
    
    `CF` will be set since the __result will yield__ a carry of `1`.
    
    ```txt
    1111 1111
         0001
    _________
    0000 0000
    ```

    to get carry instead of letting it go into `EFLAGS` register, use `ADC` operation. 
    
    We use `ADC` to continue from next `8` bits after `al`. `al` max value comes out to be `255` and adding `1` which is in carry will yield `256` in "eax".

    ```asm
    MOV al,0b11111111
    MOV bl,0b0001
    ADD al,bl
    ADC ah,0
    ```

- `AF` -> Auxilliary Flag -> Carry or Borrow happen out of the 3rd bit.

- `ZF` -> Zero Flag -> Result of previous operation yielded `zero`.

- Hex to Decimal
    ```txt
    An example:
    
    0x100
    = 1 0 0
    = 0001 0000 0000
    = 000100000000
    = 2^8 = 256
    ```
    
- Weird `SUB` behavior while dealing with `-ve` numbers.
    ```asm
    MOV eax,3
    MOV ebx,5
    SUB eax,ebx
    INT 80h
    ```
    `info registers eax` = `0xfffffffe` = `-2`
    Makes sense but how does x86 know it is supposed to be minus(-) 2 and not some large number as the hex value can be interpreted in both ways? 

    Answer is because __(Sign Flag) SF turned on represents previous operation yielded negative result__.

