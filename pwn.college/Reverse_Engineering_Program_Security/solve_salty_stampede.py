import struct
import random
import string
import hashlib

GAME_FILE = "data.bin"

def crack_history(salt, history_hashes, entry_id):
    """
    Generates a salt-specific lookup table to crack the history hashes.
    """
    cracked_history = []
    lookup = {}
    
    # Generate small rainbow table for this specific salt
    for c in range(51):
        for b in range(51):
            status_str = f"{c:02d}C{b:02d}B"
            # V4 Logic: SHA256(Salt + String)
            payload = salt + status_str.encode('utf-8')
            sha = hashlib.sha256(payload).digest()
            lookup[sha] = (c, b)
            
    # Resolve hashes
    for h in history_hashes:
        if h in lookup:
            cracked_history.append(lookup[h])
        else:
            # If cracking fails, return dummy value (0,0) but warn user
            cracked_history.append((0, 0))
            
    return cracked_history

def parse_gamefile():
    try:
        with open(GAME_FILE, "rb") as f:
            # Header
            f.seek(8)
            data_size_bytes = f.read(4)
            if not data_size_bytes: return None
            data_size = struct.unpack("<I", data_size_bytes)[0]
            entry_count = struct.unpack("<I", f.read(4))[0]
            
            entries = {}
            print(f"[*] Parsed Header: {entry_count} entries found.")
            
            for i in range(entry_count):
                try:
                    # Save current offset for debugging
                    curr_offset = f.tell()
                    
                    # Read Entry Header
                    entry_id_bytes = f.read(4)
                    if len(entry_id_bytes) < 4: break # EOF safety
                    
                    entry_id = struct.unpack("<I", entry_id_bytes)[0]
                    max_guesses = struct.unpack("<H", f.read(2))[0]
                    num_len = struct.unpack("<H", f.read(2))[0]
                    
                    # Salt (16 bytes)
                    salt = f.read(16)
                    
                    # Target (8 bytes)
                    target_val = struct.unpack("<Q", f.read(8))[0]
                    target_str = f"{target_val:0{num_len}d}"
                    
                    # === CRITICAL FIX FOR V4 ===
                    # There is a hidden buffer of (2 * max_guesses) bytes 
                    # between the Target and the History Hashes.
                    f.read(2 * max_guesses) 
                    
                    # Read History Hashes (32 bytes each)
                    history_hashes = []
                    for _ in range(max_guesses):
                        history_hashes.append(f.read(32))

                    entries[entry_id] = {
                        "target": target_str,
                        "len": num_len,
                        "guesses": max_guesses,
                        "salt": salt,
                        "hashes": history_hashes
                    }
                except struct.error:
                    print(f"[!] Warning: Malformed entry at index {i}, offset {curr_offset}. Stopping parse.")
                    break
                
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
        # Constraint 1: Unique Digits
        guess_digits = random.sample(charset, length)
        guess = "".join(guess_digits)
        
        # Constraint 2: No Leading Zero
        if guess.startswith('0'):
            continue

        c, b = calculate_cows_bulls(guess, target)
        
        if c == req_cows and b == req_bulls:
            return guess
            
    return "UNKNOWN"

def main():
    print("--- Gamefile Parser & Solver V4 (Fixed Offset Edition) ---")
    
    entries = parse_gamefile()
    if not entries:
        return

    print("\nRun the binary challenge. It will output: 'Entry ID: XXXXX'")
    
    while True:
        try:
            user_input = input("\nEnter the Entry ID: ").strip()
            if not user_input: break
            uid = int(user_input)
            
            if uid not in entries:
                print("[!] ID not found in file (or file parsing stopped early).")
                continue
                
            entry = entries[uid]
            target = entry['target']
            
            print(f"\n[*] Target Number: {target}")
            print(f"[*] Cracking history hashes using salt: {entry['salt'].hex()}...")
            
            history = crack_history(entry['salt'], entry['hashes'], uid)
            
            solution_sequence = []
            
            for i, (req_cows, req_bulls) in enumerate(history):
                step = i + 1
                
                if req_bulls == entry['len']:
                    print(f"Step {step}: {target} (WIN - All Bulls)")
                    solution_sequence.append(target)
                    break
                
                guess = find_matching_guess(target, req_cows, req_bulls, entry['len'])
                
                if guess == "UNKNOWN":
                    print(f"Step {step}: FAILED ({req_cows}C, {req_bulls}B)")
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
