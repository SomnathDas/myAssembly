import struct
import random
import string
import hashlib

GAME_FILE = "data.bin"

def generate_hash_lookup(max_val=50):
    """
    Pre-computes SHA256 hashes for all possible "XXCYYB" strings.
    Returns a dictionary: { bytes_hash : (cows, bulls) }
    """
    lookup = {}
    print("[*] Generating SHA256 Rainbow Table for history lookup...")
    
    # We iterate enough to cover reasonable max lengths (e.g., up to 50)
    for c in range(max_val + 1):
        for b in range(max_val + 1):
            # Format matches sub_1C3D: 01C02B
            status_str = f"{c:02d}C{b:02d}B"
            
            # Compute SHA256
            sha = hashlib.sha256(status_str.encode('utf-8')).digest()
            
            lookup[sha] = (c, b)
            
    return lookup

def parse_gamefile(hash_lookup):
    try:
        with open(GAME_FILE, "rb") as f:
            # Header
            f.seek(8)
            data_size = struct.unpack("<I", f.read(4))[0]
            entry_count = struct.unpack("<I", f.read(4))[0]
            
            entries = {}
            print(f"[*] Parsed Header: {entry_count} entries found.")
            
            for _ in range(entry_count):
                entry_id = struct.unpack("<I", f.read(4))[0]
                max_guesses = struct.unpack("<H", f.read(2))[0]
                num_len = struct.unpack("<H", f.read(2))[0]
                target_val = struct.unpack("<Q", f.read(8))[0]
                
                target_str = f"{target_val:0{num_len}d}"
                
                history = []
                # In V3, each history entry is a 32-byte SHA256 hash
                for _ in range(max_guesses):
                    entry_hash = f.read(32)
                    
                    if entry_hash in hash_lookup:
                        history.append(hash_lookup[entry_hash])
                    else:
                        # Fallback if hash not found (shouldn't happen if table is complete)
                        history.append((0, 0)) 
                        print(f"[!] Warning: Unknown hash found in Entry {entry_id}")

                entries[entry_id] = {
                    "target": target_str,
                    "len": num_len,
                    "guesses": max_guesses,
                    "history": history
                }
                
            return entries
            
    except FileNotFoundError:
        print(f"[!] Error: {GAME_FILE} not found.")
        return None

def calculate_cows_bulls(guess, target):
    bulls = 0
    cows = 0
    
    g_list = list(guess)
    t_list = list(target)
    
    # Bulls
    for i in range(len(g_list)):
        if g_list[i] == t_list[i]:
            bulls += 1
            g_list[i] = None 
            t_list[i] = None
            
    # Cows
    for i in range(len(g_list)):
        if g_list[i] is not None and g_list[i] in t_list:
            cows += 1
            t_list.remove(g_list[i])
            
    return cows, bulls

def find_matching_guess(target, req_cows, req_bulls, length):
    max_attempts = 200000
    charset = string.digits
    
    for _ in range(max_attempts):
        # 1. Generate Unique Digits (Constraint: Unique)
        guess_digits = random.sample(charset, length)
        guess = "".join(guess_digits)
        
        # 2. Check Leading Zero (Constraint: No leading zero)
        # Note: The binary explicitly checks `if (*a1 == 48)` which means ASCII '0'
        if guess.startswith('0'):
            continue

        # 3. Verify Logic
        c, b = calculate_cows_bulls(guess, target)
        
        if c == req_cows and b == req_bulls:
            return guess
            
    return "UNKNOWN"

def main():
    print("--- Gamefile Parser & Solver V3 (SHA256 Edition) ---")
    
    # 1. Crack the hashes
    hash_table = generate_hash_lookup()
    
    # 2. Parse file using cracked hashes
    entries = parse_gamefile(hash_table)
    
    if not entries:
        return

    print("\nRun the binary challenge. It will output: 'Entry ID: XXXXX'")
    
    while True:
        try:
            user_input = input("\nEnter the Entry ID: ").strip()
            if not user_input: break
            uid = int(user_input)
            
            if uid not in entries:
                print("[!] ID not found in file.")
                continue
                
            entry = entries[uid]
            target = entry['target']
            
            print(f"\n[*] Target Number: {target}")
            print(f"[*] Constraints: No Leading Zeros, Unique Digits")
            
            solution_sequence = []
            
            for i, (req_cows, req_bulls) in enumerate(entry['history']):
                step = i + 1
                
                # If this step requires full Bulls, we just output the target
                # (Assuming target obeys constraints, which it should)
                if req_bulls == entry['len']:
                    print(f"Step {step}: {target} (WIN - All Bulls)")
                    solution_sequence.append(target)
                    break
                
                guess = find_matching_guess(target, req_cows, req_bulls, entry['len'])
                
                if guess == "UNKNOWN":
                    print(f"Step {step}: FAILED ({req_cows}C, {req_bulls}B)")
                    # Add placeholder to keep indices aligned if user wants to try manual fix
                    solution_sequence.append("1234") 
                else:
                    print(f"Step {step}: {guess} (Req: {req_cows}C, {req_bulls}B)")
                    solution_sequence.append(guess)
            
            print("\n--- Python List Block ---")
            print(solution_sequence)
            print("-------------------------\n")
                
        except ValueError:
            print("Invalid input.")
        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    main()
