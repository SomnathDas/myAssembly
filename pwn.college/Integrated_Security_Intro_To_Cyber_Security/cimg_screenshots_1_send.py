from pwn import *

p = process(["/challenge/integration-cimg-screenshot-sc", "/tmp/exploit.cimg"], env={})

print(p.clean())

p.close()
