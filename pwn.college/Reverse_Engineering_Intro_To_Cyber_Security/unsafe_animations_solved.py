import codecs
import struct

MAGIC_BYTES_STR = "cIMG"
VERSION_NUM = 4
WIDTH_NUM = 76
HEIGHT_NUM = 24
DIRECTIVE_CODE_NUM = 1s
CREATE_SPRITE_DIRECTIVE = 3
RENDER_SPRITE_DIRECTIVE = 4
LOAD_SPRITE_DIRECTIVE = 5

def prepare_magic_bytes(magic_bytes_str):
    magic_bytes = b""
    for char in magic_bytes_str:
        packed = struct.pack("<h", ord(char))
        magic_bytes += bytes(b for b in packed if b != 0)
    return magic_bytes

def prepare_file_version(version_num):
    return struct.pack("<H", version_num)

def prepare_dimensions(width, height):
	return struct.pack("<H", width).rstrip(b"\x00") + struct.pack("<H", height).rstrip(b"\x00")

def prepare_num_directive(rem_dir):
	return struct.pack("<I", rem_dir)

def build_header():
    header = b""
    header += prepare_magic_bytes(MAGIC_BYTES_STR)
    header += prepare_file_version(VERSION_NUM)
    header += prepare_dimensions(WIDTH_NUM, HEIGHT_NUM)
    header += prepare_num_directive(DIRECTIVE_CODE_NUM)
    print("Header Size:: ", len(header))
    return header

def create_sprite(sprite_id, width, height, data):
	sprite_data = b""
	packed = b""

	sprite_data += struct.pack("<H", CREATE_SPRITE_DIRECTIVE) # 2 bytes

	packed = struct.pack("<H", sprite_id)
	sprite_data += packed[:-1] if packed.endswith(b"\x00") and len(packed) > 1 else packed # 1 byte

	packed = struct.pack("<H", width)
	sprite_data += packed[:-1] if packed.endswith(b"\x00") and len(packed) > 1 else packed # 1 byte

	packed = struct.pack("<H", height)
	sprite_data += packed[:-1] if packed.endswith(b"\x00") and len(packed) > 1 else packed # 1 byte

	sprite_data += data # width * height bytes

	print("len(sprite_data) for {}: ".format(sprite_id), len(sprite_data))

	return sprite_data

def render_sprite(sprite_id, r, g, b, x, y, tile_x, tile_y, ord_t=" "):
	render_data = b""
	packed = b""

	render_data += struct.pack("<H", RENDER_SPRITE_DIRECTIVE) # 2 bytes

	packed = struct.pack("<H", sprite_id)
	render_data += packed[:-1] if packed.endswith(b"\x00") and len(packed) > 1 else packed # 1 byte

	packed = struct.pack("<H", r)
	render_data += packed[:-1] if packed.endswith(b"\x00") and len(packed) > 1 else packed # 1 byte

	packed = struct.pack("<H", g)
	render_data += packed[:-1] if packed.endswith(b"\x00") and len(packed) > 1 else packed # 1 byte

	packed = struct.pack("<H", b)
	render_data += packed[:-1] if packed.endswith(b"\x00") and len(packed) > 1 else packed # 1 byte

	packed = struct.pack("<H", x)
	render_data += packed[:-1] if packed.endswith(b"\x00") and len(packed) > 1 else packed # 1 byte
	
	packed = struct.pack("<H", y)
	render_data += packed[:-1] if packed.endswith(b"\x00") and len(packed) > 1 else packed # 1 byte

	packed = struct.pack("<H", tile_x)
	render_data += packed[:-1] if packed.endswith(b"\x00") and len(packed) > 1 else packed # 1 byte

	packed = struct.pack("<H", tile_y)
	render_data += packed[:-1] if packed.endswith(b"\x00") and len(packed) > 1 else packed # 1 byte

	packed = struct.pack("<H", ord(ord_t))
	render_data += packed[:-1] if packed.endswith(b"\x00") and len(packed) > 1 else packed # 1 byte


	print("len(render_data) for {}: ".format(sprite_id), len(render_data))

	return render_data

def load_sprite(sprite_id, height, width, sprite_location):
	load_sprite_data = b""
	packed = b""

	load_sprite_data += struct.pack("<H", LOAD_SPRITE_DIRECTIVE) # 2 bytes

	load_sprite_data += b"\x01\x3b\x01" + prepare_magic_bytes("/flag")

	load_sprite_data += b"\x00" * 250

	return load_sprite_data


def build_data():
	data = b""

	data += struct.pack("<H", 6)
	data += b"\x01"

	# PATH=.:$PATH /challenge/cimg test.cimg
	
	print("Data Size:: ", len(data))
	return data

def build_cimg():
    header = build_header()
    data = build_data()

    payload = ""
    payload += ''.join(f'\\x{byte:02x}' for byte in header)
    payload += ''.join(f'\\x{byte:02x}' for byte in data)

    byte_data = codecs.decode(payload, 'unicode_escape').encode('latin1')

    print("File Bytes:: ", len(byte_data))
    
    command = f'echo -ne "{payload}" > /tmp/test.cimg'
    print(command)

    with open("test.cimg", "wb") as f:
    	f.write(header + data)

def __main__():
    build_cimg()

__main__()
