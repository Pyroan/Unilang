# does its best to compress the given program as much as possible
# an annoying part of this implementation is that you have a string
# like 'abcd', the output will look something like 'a_' and not '_d'
def compress_program(prog: str) -> str:
    # Welcome to stringland!
    # the way we compress characters necessitates that the program be backwards.
    # sorry.
    prog = list(reversed(prog))
    cmpr = []
    i = 0
    
    next_chr = 0
    j = 0
    while i < len(prog):
        if is_base_op(ord(prog[i])):
            digit = (ord(prog[i]) - 0x5f) * (0x20**j)
            if is_legal_char(next_chr + digit + 0x5f):
                next_chr += digit
                j += 1
            else:
                cmpr.append(chr(next_chr + 0x5f))
                next_chr = 0
                j = 0
                i -= 1 # so we don't skip the one we're looking at
        else:
            # Playing catchup with the missing next_chr...
            # (bad)
            if next_chr > 0:
                cmpr.append(chr(next_chr + 0x5f))
                next_chr = 0
                j = 0
            cmpr.append(prog[i])
        i += 1
    # Playing catchup again...
    if next_chr > 0:
        cmpr.append(chr(next_chr + 0x5f))

    return ''.join(reversed(cmpr))

def decompress_program(prog: str) -> str:
    decompressed = []
    for i in len(prog):
        if 0x60 <= ord(i) < 0x80:
            decompressed.append(i)
        else:
            decompressed += list(decompress_char(i))
    return ''.join(decompressed)

def decompress_char(char) -> str:
    snippet = []
    codepoint = ord(char) - 0x5f
    while codepoint > 0:
        snippet.append(chr(codepoint % 32 + 0x5f))
        codepoint //= 0x20
    return ''.join(reversed(snippet))

# Return true if the given codepoint is a valid unilang base op
def is_base_op(codepoint: int):
    return 0x60 <= codepoint < 0x80

# Return false if code point is...
# 0. outside the unicode range (bigger than 0x10ffff)
# 1. in a desginated Private-Use range
# 2. a Noncharacter
# More information available at http://www.unicode.org/faq/private_use.html
# Allegedly two of the private-use ranges include valid characters but i'm
# going to ignore that for now.
def is_legal_char(codepoint: int):
    if codepoint >= 0x100000:
        return False
    # Private use ranges
    if 0xe000 <= codepoint <= 0xf8ff:
        return False
    if 0xf0000 <= codepoint <= 0xffffd:
        return False
    if 0x100000 <= codepoint <= 0x10fffd:
        return False
    # Noncharacters
    if 0xfdd0 <= codepoint <= 0xfdef:
        return False
    # TODO generate this list programmatically
    other_nonchars = [
        0xfffe,  0xffff,  0x1fffe, 0x1ffff, 0x2fffe, 0x2ffff, 0x3fffe, 0x3ffff,
        0x4fffe, 0x4ffff, 0x5fffe, 0x5ffff, 0x6fffe, 0x6ffff, 0x7fffe, 0x7ffff,
        0x8fffe, 0x8ffff, 0x9fffe, 0x9ffff, 0xafffe, 0xaffff, 0xbfffe, 0xbffff,
        0xcfffe, 0xcffff, 0xdfffe, 0xdffff, 0xefffe, 0xeffff, 0xffffe, 0xfffff,
        0x10fffe, 0x10ffff 
    ]
    if codepoint in other_nonchars:
        return False
    
    return True