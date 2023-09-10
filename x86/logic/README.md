- `NOT` logical operator will flip each and every bit regardless of whether that is set by us or not or that we care about or not.

- To preserve bits that we care about, what we do is called `masking`

    ```asm
    MOV eax,0b1010
    NOT eax
    AND eax,0x0000000F <-- This will mask and preserve our values
    INT 80h
    ```

    Remember, in hex each digit is `4` bits and here from `line 1`, we care only about last `4` bits and hence setting it to be `F` in `line 3` to preserve our __NOT'd__ value previously in `line 2`.

    You can also just write `AND eax,0xF` as our ASM fills it up as last `4` bits
    if we are dealing with `32bit` register i.e eax then its last `4` bits is set to `1` hex digit that is F meaning all `1111`

- `XOR` operator -> Only sets the value to 1 if there is only single one

    ```txt
    Meaning:
    	0b1010
    	0b1100
    XOR	______
    	0b0110
    ```

- SHIFT instruction shifts the bit to `[n] step` in the (direction)

    SHR eax,1 (Shift Right) => will shift bits to right directory by 1 step

    ```txt
    Example:
    MOV eax,0b0010
    SHR eax,1 [ 0b0010 -> 0b0001 ]
    ```

    Note: last values always go to the `CF` (Carry Flag)

- Another way to think about this is that `SHIFT RIGHT` instruction is dividing the value by `2`.

and yes, `SHIFT LEFT` (SHL) instruction will act as multiplying by `2`.

and there are some other type of shifts too

__these operations are faster in comparision to MUL, DIV operations__


