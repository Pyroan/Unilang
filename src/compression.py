# does its best to compress the given program as much as possible
def compress_program(prog: str) -> str:
    # Welcome to stringland!
    prog = list(prog)
    cmpr = []
    i = 0
    while i < len(prog):
        # find the longest string of valid base ops starting at 
        j = 0
        while i+j < len(prog) and 0x60 <= ord(prog[i+j]) < 0x80 and j < 3: # don't judge me
            j += 1
        
        if j > 1:
            cmpr.append(compress_snippet(prog[i:i+j]))
            i += j - 1
        else:
            cmpr.append(prog[i])
            i += 1
    return ''.join(cmpr)

def decompress_program(prog: str) -> str:
    decompressed = []
    for i in len(prog):
        if 0x60 <= ord(i) < 0x80:
            decompressed.append(i)
        else:
            decompressed += list(decompress_char(i))
    return ''.join(decompressed)

# Look i'm gonna limit it to 3 chars for right now please don't @ me.
def compress_snippet(prog: str) -> str:
    if len(prog) > 3:
        return prog
    compressed = 0
    reversed_prog = list(reversed(prog))
    for i in range(len(reversed_prog)):
        c = ord(reversed_prog[i]) - 0x5f
        compressed += c * (0x20 ** i)
    return chr(compressed + 0x5f)

def decompress_char(char) -> str:
    snippet = []
    codepoint = ord(char) - 0x5f
    while codepoint > 0:
        snippet.append(chr(codepoint % 32 + 0x5f))
        codepoint //= 0x20
    return ''.join(reversed(snippet))