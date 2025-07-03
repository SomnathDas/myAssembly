import pwn

# GAS syntax for relative to rip jump
# jmp .+0x2b

p = pwn.gdb.debug("./babyrev-level-9-0", env={"LD_PRELOAD": "./libcrypto.so.1.1"})

p.sendline(b"1a46")
p.sendline(b"eb")
p.sendline(b"1a47")
p.sendline(b"29")
p.sendline(b"1a48")
p.sendline(b"90")
p.sendline(b"1a49")
p.sendline(b"90")
p.sendline(b"1a4a")
p.sendline(b"90")

result = b"\xd9\xe3\x1e\x04\xa6\x18C\xb7\x99h\xa8\xad\xc4\xbe\xf3\xbe"

p.send(result)

res = p.readall()
print(res)
