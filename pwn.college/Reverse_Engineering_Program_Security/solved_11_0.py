import pwn

p = pwn.process("./babyrev-level-11-0", env={"LD_PRELOAD": "./libcrypto.so.1.1"})

p.sendline(b"1cc3")
p.sendline(b"74")
p.sendline(b"1f59")
p.sendline(b"74")

p.sendline(b"blyat")

res = p.readall()
print(res)

p.close()
