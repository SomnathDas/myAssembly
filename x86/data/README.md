- `DB` -> Define Byte -> `1 Byte`
`DW` -> Define Word -> `2 Bytes`
`DD` -> Define Double Word -> `4 Bytes`
`DQ` -> Define QWord -> `6 Bytes`
`DT` -> Define TWord -> `10 Bytes`

- Inconsistent Data Size:

    ```txt
    num DB 1 (DB -> 1 byte -> 8bits)
    num DB 2 (DB -> 1 byte -> 8bits)
    ```

    While storing these data into registers such as `eax`,`ebx`,`ecx`:
    
    (e => extended) -> `eax` = `ebx` = `ecx` = .. = __32 bits in capacity__
    `ax` = `bx` = `cx` = .. = __16bits in capacity__
    `ah` = __Upper 8bits of 16bits__
    `al` = __Lower 8bits of 16bits__

- Make sure you keep data-sizes consistent

    -> Be careful as to where you are placing our values in ah and al
    -> If working with ah,al together then it is fine
    -> Just use al,bl,cl if using individually
    -> If you set ah to some value and then check ax it will differ if you change al instead

    __Take-away:__
    1. If you are working with whole `32bits` then you use `eax`,`ebx`,`ecx` etc
    2. If you are wroking with `16bits` then you use `ax`,`bx`,`cx` etc
    3. If you are working with `8bits` then you use `ah`,`al` ,, `bh`,`bl` etc
