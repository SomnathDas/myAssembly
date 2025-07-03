def prinz(key):
    for i in key:
        print(hex(i).split("0x")[1], end=" ")
    print()

# 65 5a 19 6b 4c 02 4f 6e 26 5d 63 78 0c 28 65 1b
# key = bytearray(b"\x07<}\x05;{\x038w\r1j\x13)f\x1c")

def sort(key):
    for ix, char in enumerate(key):
        for ix, char in enumerate(key):
            if((ix) >= 15):
                break
            if(key[ix] > key[ix + 1]):
                temp = key[ix]
                key[ix] = key[ix+1]
                key[ix+1] = temp

def xor_1(key):
    for ix, char in enumerate(key):
        key[ix] = key[ix] ^ 0x3e

def swi(key):
    for ix, char in enumerate(key):
        rax = ix % 5
        if(rax == 0):
            key[ix] = key[ix] ^ 0xd7
        if(rax == 1):
            key[ix] = key[ix] ^ 0xbd
        if(rax == 2):
            key[ix] = key[ix] ^ 0x77
        if(rax == 3):
            key[ix] = key[ix] ^ 0xe
        if(rax == 4):
            key[ix] = key[ix] ^ 0x8d

def resp(key):
    for ix, char in enumerate(key):
        temp = key[ix]
        key[ix] = key[0x1b - ix]
        key[0x1b - ix] = temp

def xor_2(key):
    for ix, char in enumerate(key):
        key[ix] = key[ix] ^ 0xb8

key = bytearray(b"0R\x98\xe6j:V\x87\xf9h)\\\x8b\xf8d(W\x80\xfcg0B\x98\xef~$I\x9d")

with open("key_og", "wb") as f:
    f.write(key)

print("Length of key: ", hex(len(key)))

xor_2(key)
resp(key)
resp(key)
swi(key)
xor_1(key)


with open("key", "wb") as f:
    f.write(key)
