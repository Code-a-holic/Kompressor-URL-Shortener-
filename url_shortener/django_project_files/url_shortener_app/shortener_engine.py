from binascii import crc32, hexlify


def encoding(url_input):
    string_in_bytes = bytes(url_input, encoding="utf-8")
    integer = crc32(string_in_bytes)
    integer_in_bytes = integer.to_bytes(4, byteorder="big")
    hex_bytes = hexlify(integer_in_bytes)

    return hex_bytes.decode('utf-8')

