import pwn

p = pwn.process("./babyrev-level-10-1", env={"LD_PRELOAD": "./libcrypto.so.1.1"})

p.sendline(b"1efc")
p.sendline(b"74")

p.sendline(b"blyat")

res = p.readall()
print(res)
