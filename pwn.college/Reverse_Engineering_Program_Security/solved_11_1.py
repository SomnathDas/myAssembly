import pwn

p = pwn.process("./babyrev-level-11-1", env={"LD_PRELOAD": "./libcrypto.so.1.1"})

p.sendline(b"2796")
p.sendline(b"86")
p.sendline(b"2873")
p.sendline(b"74")

p.sendline(b"blyat")

res = p.readall()
print(res)

p.close()
