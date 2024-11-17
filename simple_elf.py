# A Python Script to write bytes to make a simple ELF Executable Program
# The Program simply prints "Hello, Mom!" to the stdout
# Written by Somnath, Year is 2024

# File Structure #

## ELF File Header (64-bytes) ##
### e_ident == 16 bytes ###
MAGIC_BYTES = b"\x7f\x45\x4c\x46" # 4 bytes : [0:3]
ARCH_BYTE = b"\x02" # 1 byte : [4]
ENDIAN_BYTE = b"\x01" # 1 byte : [5]
ELF_VERSION_BYTE = b"\x01" # 1 byte : [6]
ABI_VERSION_BYTE = b"\x00" # 1 byte : [7]
PADDING_BYTES = b"\x00\x00\x00\x00\x00\x00\x00\x00" # 7 bytes : [8:15]
### e_ident == 16 bytes ###
ELF_TYPE = b"\x02\x00" # 2 bytes [16:17]
INSTRUCTION_SET = b"\x3e\x00" # 2 bytes [18:19]
ELF_VERSION_BYTES = b"\x01\x00\x00\x00" # 4 bytes [20:23]
### Unknowns ###
PROGRAM_ENTRY_OFFSET = b"\xb0\x00\x40\x00\x00\x00\x00\x00" # 8 bytes [24:31]
PROGRAM_HEADER_TABLE_OFFSET = b"\x40\x00\x00\x00\x00\x00\x00\x00" # 8 bytes [32-39]
SECTION_HEADER_OFFSET = b"\x00\x00\x00\x00\x00\x00\x00\x00" # 8 bytes [40-47]
### Unknowns ###
FLAGS = b"\x00\x00\x00\x00" # 4 bytes [48-51]
ELF_HEADER_SIZE = b"\x40\x00" # 2 bytes [52-53]
### Unknowns ###
PROGRAM_HEADER_TABLE_SIZE = b"\x38\x00" # 2 bytes [54-55]
NO_OF_PROGRAM_HEADER_TABLE_ENTRIES = b"\x02\x00" # 2 bytes [56-57]
SECTION_HEADER_TABLE_SIZE = b"\x00\x00" # 2 bytes [58-59]
NO_OF_SECTION_HEADER_TABLE_ENTRIES = b"\x00\x00" # 2 bytes [60-61]
### Unknowns ###
SECTION_INDEX_SECTION_HEADER_STRING_TABLE = b"\x00\x00" # 2 bytes [62-63]
## ELF File Header ##

##  Program Segment Headers 1 ##
PROGRAM_SEGMENT_TYPE_1 = b"\x01\x00\x00\x00" # 4 bytes : [64:67]
PROGRAM_SEGMENT_FLAGS_1 = b"\x05\x00\x00\x00" # 4 bytes : [68:71]
### Unknown ###
PROGRAM_SEGMENT_OFFSET_1 = b"\xb0\x00\x00\x00\x00\x00\x00\x00" # 8 bytes : [72:79]
PROGRAM_SEGMENT_VIRTUAL_ADDRESS_1 = b"\xb0\x00\x40\x00\x00\x00\x00\x00" # 8 bytes : [80:87]
PROGRAM_SEGMENT_PHY_ADDRESS_1 = b"\x00\x00\x00\x00\x00\x00\x00\x00" # 8 bytes : [88:95]
PROGRAM_SEGMENT_SIZE_IN_FILE_1 = b"\x2e\x00\x00\x00\x00\x00\x00\x00" # 8 bytes : [96:103]
PROGRAM_SEGMENT_SIZE_IN_MEM_1 = b"\x2e\x00\x00\x00\x00\x00\x00\x00" # 8 bytes : [104:111]
### Unknown ###
PROGRAM_SEGMENT_ALIGNMENT_1 = b"\x00\x10\x00\x00\x00\x00\x00\x00" # 8 bytes : [112:119]
##  Program Segment Headers 1 ##

##  Program Segment Headers 2 (READONLY) ##
PROGRAM_SEGMENT_TYPE_2 = b"\x01\x00\x00\x00" # 4 bytes : [64:67]
PROGRAM_SEGMENT_FLAGS_2 = b"\x04\x00\x00\x00" # 4 bytes : [68:71]
### Unknown ###
PROGRAM_SEGMENT_OFFSET_2 = b"\xde\x00\x00\x00\x00\x00\x00\x00" # 8 bytes : [72:79]
PROGRAM_SEGMENT_VIRTUAL_ADDRESS_2 = b"\xde\x00\x41\x00\x00\x00\x00\x00" # 8 bytes : [80:87]
PROGRAM_SEGMENT_PHY_ADDRESS_2 = b"\x00\x00\x00\x00\x00\x00\x00\x00" # 8 bytes : [88:95]
PROGRAM_SEGMENT_SIZE_IN_FILE_2 = b"\x0c\x00\x00\x00\x00\x00\x00\x00" # 8 bytes : [96:103]
PROGRAM_SEGMENT_SIZE_IN_MEM_2 = b"\x0c\x00\x00\x00\x00\x00\x00\x00" # 8 bytes : [104:111]
### Unknown ###
PROGRAM_SEGMENT_ALIGNMENT_2 = b"\x00\x10\x00\x00\x00\x00\x00\x00" # 8 bytes : [112:119]
##  Program Segment Headers 2 (READONLY) ##

# File Structure #

# Helper #
def elf_file_header():
    e_ident = MAGIC_BYTES + ARCH_BYTE + ENDIAN_BYTE + ELF_VERSION_BYTE + ABI_VERSION_BYTE + PADDING_BYTES    
    header = e_ident
    header += ELF_TYPE + INSTRUCTION_SET + ELF_VERSION_BYTES + PROGRAM_ENTRY_OFFSET 
    header += PROGRAM_HEADER_TABLE_OFFSET + SECTION_HEADER_OFFSET + FLAGS 
    header += ELF_HEADER_SIZE + PROGRAM_HEADER_TABLE_SIZE 
    header += NO_OF_PROGRAM_HEADER_TABLE_ENTRIES + SECTION_HEADER_TABLE_SIZE 
    header += NO_OF_SECTION_HEADER_TABLE_ENTRIES + SECTION_INDEX_SECTION_HEADER_STRING_TABLE
    print("Size of the elf_file_header :: " + str(len(header)))
    return header

def program_segment_header_1():
    header = PROGRAM_SEGMENT_TYPE_1 + PROGRAM_SEGMENT_FLAGS_1
    header += PROGRAM_SEGMENT_OFFSET_1 + PROGRAM_SEGMENT_VIRTUAL_ADDRESS_1
    header += PROGRAM_SEGMENT_PHY_ADDRESS_1 + PROGRAM_SEGMENT_SIZE_IN_FILE_1
    header += PROGRAM_SEGMENT_SIZE_IN_MEM_1 + PROGRAM_SEGMENT_ALIGNMENT_1
    print("Size of the program_header__for_code_section :: " + str(len(header)))
    return header

def program_segment_header_2():
    header = PROGRAM_SEGMENT_TYPE_2 + PROGRAM_SEGMENT_FLAGS_2
    header += PROGRAM_SEGMENT_OFFSET_2 + PROGRAM_SEGMENT_VIRTUAL_ADDRESS_2
    header += PROGRAM_SEGMENT_PHY_ADDRESS_2 + PROGRAM_SEGMENT_SIZE_IN_FILE_2
    header += PROGRAM_SEGMENT_SIZE_IN_MEM_2 + PROGRAM_SEGMENT_ALIGNMENT_2
    print("Size of the program_header__for_data_section :: " + str(len(header)))
    return header

def code_section():
    payload = b"\x48\xc7\xc0\x01\x00\x00\x00"
    payload += b"\x48\xc7\xc7\x01\x00\x00\x00"
    payload += b"\x48\xc7\xc6\xde\x00\x41\x00"
    payload += b"\x48\xc7\xc2\x0c\x00\x00\x00"
    payload += b"\x0f\x05"

    payload += b"\x48\xc7\xc0\x3c\x00\x00\x00"
    payload += b"\x48\xc7\xc7\x00\x00\x00\x00"
    payload += b"\x0f\x05"

    print("Size of the code_section :: " + str(len(payload)))
    return payload

def data_section():
    payload = b"\x48\x65\x6c\x6c\x6f\x2c\x20\x4d\x6f\x6d\x21" + b"\x00"
    print("Size of the data_section :: " + str(len(payload)))
    return payload


def make(filename):
    payload = elf_file_header() + program_segment_header_1()
    payload += program_segment_header_2()
    payload += code_section()
    payload += data_section()
    print("Size of complete elf file :: " + str(len(payload)))

    print(":: Raw Bytes ::")
    print(''.join(f'\\x{byte:02x}' for byte in payload))
    print(":: Raw Bytes ::")
    with open(filename, "wb") as f:
        f.write(payload)

# Helper #

# Engine #
filename = "world"
print("Writing bytes out to filename :: " + filename)
print()
make(filename)
# Engine #
