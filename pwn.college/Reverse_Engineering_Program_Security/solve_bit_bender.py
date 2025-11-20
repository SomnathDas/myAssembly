import sys

def solve():
    target_str = "bQQyKgcgSacMiOIi"
    target_bytes = [ord(c) for c in target_str]
    solution = bytearray()

    print(f"Target Hex: {target_str.encode().hex()}")
    print("-" * 30)
    
    for b in target_bytes:
        rotated_val = ((b & 0x03) << 6) | (b >> 2)
        original_val = (rotated_val - 72) % 256
        solution.append(original_val)

    print(f"Recovered Key (Hex): {solution.hex()}")
    
    try:
        print(f"Recovered Key (Str): {solution.decode('latin-1')}")
    except:
        print("Key contains non-printable characters")
        
    with open('key.bin', 'wb') as f:
        f.write(solution)
    print("-" * 30)
    print("Key saved to 'key.bin'")

if __name__ == "__main__":
    solve()
