import struct
import sys
import os

ENTRY_SIZE = 16
HEADER_SIZE = 16

def parse_gamefile(filename):
    if not os.path.exists(filename):
        print(f"\nOops! It looks like I can't find the file: '{filename}'. Make sure it's in the same folder as me.")
        return None

    with open(filename, "rb") as f:
        header_data = f.read(HEADER_SIZE)
        if len(header_data) != HEADER_SIZE:
            print("Hmm, the file seems to be cut short. It looks like the header is incomplete.")
            return None

        try:
            magic, version, data_size, num_levels = struct.unpack("<4sIII", header_data)
        except struct.error:
            print("I had trouble reading the beginning of the file. It might be corrupted.")
            return None
        
        version_check = struct.unpack("<H", header_data[4:6])[0]
        
        if version_check != 1:
            print(f"Heads up! The file version is a bit off ({version_check}). The game might not accept it, but let's try anyway.")
        
        print(f"Success! The game file is ready to go.")
        print(f"I found {num_levels} different challenges in the file.")
        
        levels = []
        for i in range(num_levels):
            entry_data = f.read(ENTRY_SIZE)
            if len(entry_data) != ENTRY_SIZE:
                print(f"Wait, the file seems to end suddenly while I was reading challenge {i+1}. I'll stop here.")
                break

            try:
                lvl_id, max_guesses, code_len, secret_raw = struct.unpack("<IHH8s", entry_data)
            except struct.error:
                print(f"Something went wrong reading the data for challenge {i+1}. Skipping that one.")
                continue

            secret_value = struct.unpack("<Q", secret_raw)[0]
            secret_string = str(secret_value)
            
            levels.append({
                'id': lvl_id,
                'max_guesses': max_guesses,
                'code_length': code_len,
                'secret_decimal': secret_string,
                'required_failures': max_guesses - 1
            })
            
        return levels

def run_solver():
    filename = "gamefile.bin"
    levels = parse_gamefile(filename)

    if not levels:
        return

    print("\n" + "=" * 60)
    print("      Reverse Engineering: Bulls and Cows Solver")
    print("=" * 60)
    
    print("\nAvailable Challenge IDs:")
    for level in levels:
        print(f"  - ID: {level['id']}")
    
    while True:
        try:
            user_id = input("\nEnter the Challenge ID you want to solve (or 'q' to quit): ").strip()
            
            if user_id.lower() == 'q':
                print("Quitting now. Go get that flag!")
                break
                
            target_id = int(user_id)
            target_level = next((l for l in levels if l['id'] == target_id), None)
            
            if target_level:
                print("\n" + "*" * 60)
                print(f"       *** WINNING STRATEGY FOR CHALLENGE ID: {target_id} ***")
                print("*" * 60)
                print(f"   Max Guesses Allowed:    {target_level['max_guesses']}")
                print(f"   Required Code Length:   {target_level['code_length']}")
                print(f"   The Secret Code (Dec):  {target_level['secret_decimal']}")
                print("\n--- ACTION PLAN ---")
                print("1. Remember the game has a trap: you must only win on the FINAL GUESS.")
                print(f"2. Enter a WRONG guess (e.g., '0') for the first {target_level['required_failures']} turns.")
                print(f"3. On the FINAL guess (Turn {target_level['max_guesses']}), input the secret:")
                print(f"   >>> {target_level['secret_decimal']}")
                print("*" * 60 + "\n")
                
            else:
                print(f"I couldn't find a challenge with ID '{target_id}'. Check the list and try another number!")
                
        except ValueError:
            print("That wasn't a number I recognized. Please enter a valid challenge ID or 'q' to quit.")
        except KeyboardInterrupt:
            print("\nQuitting now. Go get that flag!")
            break

if __name__ == "__main__":
    run_solver()
