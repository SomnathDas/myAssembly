import struct
import random
import string

GAME_FILE = "data.bin" # Ensure this is in the same directory

def parse_gamefile():
    try:
        with open(GAME_FILE, "rb") as f:
            # Read Global Header
            # 0-8: Unknown/Padding
            # 8-12: Data Size
            # 12-16: Entry Count
            f.seek(8)
            data_size = struct.unpack("<I", f.read(4))[0]
            entry_count = struct.unpack("<I", f.read(4))[0]
            
            entries = {}
            
            print(f"[*] Parsed Header: {entry_count} entries found.")
            
            # Loop through entries
            for _ in range(entry_count):
                entry_id = struct.unpack("<I", f.read(4))[0]
                max_guesses = struct.unpack("<H", f.read(2))[0]
                num_len = struct.unpack("<H", f.read(2))[0]
                target_val = struct.unpack("<Q", f.read(8))[0]
                
                # Format target as string with leading zeros if necessary
                target_str = f"{target_val:0{num_len}d}"
                
                history = []
                for _ in range(max_guesses):
                    h_data = f.read(6).decode('utf-8', errors='ignore')
                    try:
                        cows = int(h_data[0:2])
                        bulls = int(h_data[3:5])
                        history.append((cows, bulls))
                    except ValueError:
                        history.append((0, 0))

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
    
    # Calculate Bulls
    for i in range(len(g_list)):
        if g_list[i] == t_list[i]:
            bulls += 1
            g_list[i] = None 
            t_list[i] = None
            
    # Calculate Cows
    for i in range(len(g_list)):
        if g_list[i] is not None and g_list[i] in t_list:
            cows += 1
            t_list.remove(g_list[i])
            
    return cows, bulls

def find_matching_guess(target, req_cows, req_bulls, length):
    max_attempts = 200000
    
    # Determine safe character set
    # If target has no '0', we strictly use 1-9 to avoid invalid inputs
    if '0' in target:
        charset = string.digits # 0-9
    else:
        charset = "123456789"   # 1-9
        
    # Determine if leading zero is risky
    # If target starts with 0, leading zeros are definitely allowed.
    # If not, we avoid them to prevent "Length Mismatch" errors (e.g. 0781 parsed as 781)
    allow_leading_zero = target.startswith('0')
    
    for _ in range(max_attempts):
        # Generate random permutation
        guess_digits = random.sample(charset, length)
        guess = "".join(guess_digits)
        
        # Enforce Leading Zero Constraint
        if not allow_leading_zero and guess.startswith('0'):
            continue

        c, b = calculate_cows_bulls(guess, target)
        
        if c == req_cows and b == req_bulls:
            return guess
            
    return "UNKNOWN"

def main():
    print("--- Gamefile Parser & Solver (Safe Mode) ---")
    entries = parse_gamefile()
    
    if not entries:
        return

    print("\nRun the binary challenge. It will output a line like:")
    print("'Entry ID: 12345'")
    
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
            print(f"[*] Required Length: {entry['len']}")
            
            # Constraint analysis for logging
            constraints = ["Unique Digits"]
            if '0' not in target: constraints.append("No Zeros (1-9)")
            if not target.startswith('0'): constraints.append("No Leading Zeros")
            print(f"[*] Constraints applied: {', '.join(constraints)}")
            
            solution_sequence = []
            
            for i, (req_cows, req_bulls) in enumerate(entry['history']):
                step = i + 1
                
                if req_bulls == entry['len']:
                    print(f"Step {step}: {target} (WIN - All Bulls)")
                    solution_sequence.append(target)
                    break
                
                guess = find_matching_guess(target, req_cows, req_bulls, entry['len'])
                
                if guess == "UNKNOWN":
                    print(f"Step {step}: FAILED to find matching guess for {req_cows}C {req_bulls}B")
                    solution_sequence.append("0000") # Placeholder to maintain sequence length
                else:
                    print(f"Step {step}: {guess} (Req: {req_cows} Cows, {req_bulls} Bulls)")
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
