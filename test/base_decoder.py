import base64
import zlib

data = """

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

"""

byte_array = base64.b64decode(data.strip().encode())

print(byte_array[0] == 0x78, byte_array[1] == 0xDA)

# print(base64.b64decode(data.strip().encode()))
