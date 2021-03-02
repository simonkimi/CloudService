import base64
import zlib

data = """

eNp9UctuwjAQ/JeVesvBr/jBsY8DEuICag9tD6kxrdWQpMRBSCj/3rXDI3DgYtkzszO76wO4v843G1eF1xomB+j8CibAFOWCGcgu9FMiKCFEcEaRqboNTGgGZW1/XeQI9Pf0Z+YZC2LY+wGiZmRBMmhDsQ1Lv3FISCqk4ZRoLK5WVyDP9W1WjKIY1WeDLxv5njB+wc46McY+M1i5UPhyWq2HfbRuWxUxGT46bdQaT2EMntxanCr4ULppikcft3MlXrnB5vZNvGmq4oBFG2aRfNk3cxejjMw1qiq3vyEYF0rGRfz4Zp5WTM1o1ARxpa6hZY1hObmUJYAyBGxdls4GX1c4Qi4esOevovV2cfKXcb/Nzr35QZETBQmY1W3AfqjM0zOJIZdSscQ3Q4Hkhg/vo15QkZ6DXutkh9so6+3RQxidao7go/9edNa6th1o/HHFoe//AdimyI4=

"""

byte_array = base64.b64decode(data.strip().encode())

print(zlib.decompress(base64.b64decode(data.strip().encode())).decode())
