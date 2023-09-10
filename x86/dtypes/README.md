1. When we define `lists`, we need an indicator to denote the end of this list... usually we take `-1`.

    ```asm
    list DB 1,2,3,4,-1
    ```

2. Similarly with dealing with `string`, we need an indicator

    ```asm
    string1 DB "ABA",0
    string2 DB "CDE",0
    ```
