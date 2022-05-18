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
                i -= 1  # so we don't skip the one we're looking at
        else:
            # Playing catchup with the missing next_chr...
            # (bad)
            if next_chr > 0:
                cmpr.append(chr(next_chr + 0x5f))
                next_chr = 0
                j = 0
            cmpr.append(prog[i])
        i += 1
    # Playing catchup again for end of string...
    # (still bad)
    if next_chr > 0:
        cmpr.append(chr(next_chr + 0x5f))

    return ''.join(reversed(cmpr))


def decompress_program(prog: str) -> str:
    decompressed = []
    for i in prog:
        if ord(i) < 0x80:
            decompressed.append(i)
        else:
            decompressed += list(decompress_char(i))
    return ''.join(decompressed)


def decompress_char(char) -> str:
    snippet = []
    codepoint = ord(char) - 0x5f
    while codepoint > 0:
        codepoint -= 1
        next_char = codepoint % 0x20 + 0x60
        snippet.append(chr(next_char))
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

    other_nonchars = []
    for i in range(0x11):
        other_nonchars += [0x10000*i + 0xfffe, 0x10000*i + 0xffff]

    if codepoint in other_nonchars:
        return False

    return True
