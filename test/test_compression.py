import unittest
from src.compression import *

@unittest.skip
class TestConsistency(unittest.TestCase):
    def test_consistency(self):
        cases = []
        for i in cases:
            self.assertEqual(
                decompress_program(compress_program(i)), i
            )
    
    # Calling compression on a compressed string should do nothing
    def test_multiple_compress(self):
        cases = []
        for i in cases:
            self.assertEqual(
                compress_program(i),
                compress_program(compress_program(i))
            )
    
    # Calling decompression on a decompressed string _really_ shouldn't do anything.
    def test_multiple_decompress(self):
        cases = []
        for i in cases:
            self.assertEqual(decompress_program(i), i)


class TestCompression(unittest.TestCase):
    def test_compressProgram(self):
        cases = {
            'a': 'a',
            '``': '\u0080',
            '`a': '\u0081',
            'aa': '\u00a1',
            '\u007f\u007f': '\u047f',
            '\u007f\u007f\u007f': '\u847f',
            'abc': '\u08c3',

            '345ab1vv3v': '345\u00a21\u03563v',
            'aaaaa': 'a\U000108a1', # this is bad depending on our goals

        }
        for i, o in cases.items():
            self.assertEqual(compress_program(i), o)

class TestDecompression(unittest.TestCase):
    def test_decompressChar(self):
        cases = {
            '\u00a1': 'aa',
            '\u00a2': 'ab'
        }
        for i, o in cases.items():
            self.assertEqual(decompress_char(i), o)

    def test_decompressProgram(self):
        cases = {}
        for i, o in cases.items():
            self.assertEqual(decompress_char(i), o)


if __name__ == '__main__':
    unittest.main()