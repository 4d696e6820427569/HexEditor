#!/usr/bin/python3

import sys
import codecs
from io import DEFAULT_BUFFER_SIZE
from pathlib import Path
from functools import partial

class bcolors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_usage():
    print("Usage: ./hexdump [file_name]")

def read_file():
    if len(sys.argv) < 2:
        print_usage()
        return

    path = Path(sys.argv[1])
    with path.open('rb') as file:
        reader = partial(file.read1, DEFAULT_BUFFER_SIZE)
        file_iterator = iter(reader, bytes())
        for chunk in file_iterator:
            yield from chunk

def is_ascii(b):
    return b < 128

def is_printable(b):
    return chr(b).isprintable() and is_ascii(b)

def get_hex_str(_bytes):
    _hex = ""
    for b in _bytes:
        _hex += format(b, '02x')
    return _hex

def get_ascii_str(_bytes):
    _ascii = ""
    for b in _bytes:
        if is_printable(b):
            _ascii += chr(b)
        else:
            _ascii += "."
    return _ascii

def map_hex_ascii(_bytes):
    hex_to_ascii = []
    for b in _bytes:
        _hex_value = format(b, '02x')
        if is_printable(b):
            _ascii_value = chr(b)
        else:
            _ascii_value = "."
        hex_to_ascii.append((_hex_value, _ascii_value))
    return hex_to_ascii

def print_dump_data(dump_map, byte_chunk = 16, highlight = True):
    byte_count = 0
    while byte_count < len(dump_map):
        if byte_count % byte_chunk == 0:
            print()
            if highlight:
                print(f"{bcolors.RED}{byte_count:08x}:{bcolors.ENDC}", end = " ")
            else:
                print(f"{byte_count:08x}:", end = " " )

        init_byte_count = byte_count
        for i in range(byte_chunk):
            if init_byte_count + i < len(dump_map):
                if highlight:
                    print(f"{bcolors.GREEN}{dump[init_byte_count + i][0]}{bcolors.ENDC}", end = " ")
                else:
                    print(f"{dump[init_byte_count + i][0]}", end = " ")
                byte_count += 1
            else:
                print("  ", end = " ")


        for i in range(byte_chunk):
            if init_byte_count + i < len(dump_map):
                if highlight:
                    print(f"{bcolors.BLUE}{dump[init_byte_count + i][1]}{bcolors.ENDC}", end = "")
                else:
                    print(f"{dump[init_byte_count + i][1]}", end = "")

if __name__ == "__main__":
    _bytes = read_file()
    dump = map_hex_ascii(_bytes)
    if len(sys.argv) == 3 and sys.argv[2] == '-nh':
        print_dump_data(dump, highlight = False)
    else:
        print_dump_data(dump)
