import pwn

p = pwn.gdb.debug("./babyrev-level-9-1", env={"LD_PRELOAD": "./libcrypto.so.1.1"})

p.sendline(b"1738")
p.sendline(b"eb")
p.sendline(b"1739")
p.sendline(b"29")
p.sendline(b"173a")
p.sendline(b"90")
p.sendline(b"173b")
p.sendline(b"90")
p.sendline(b"173c")
p.sendline(b"90")

result = b"~c\x04\xd0\xac{\x94k^I\x9f8\xe9\x94v\xb0"

p.send(result)

res = p.readall()
print(res)
