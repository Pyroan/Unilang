import unittest
from src.compression import *

class TestCompression(unittest.TestCase):
    def test_compressSnippet(self):
        cases = {
            'a': 'a',
            '``': '\u0080',
            '`a': '\u0081',
            'aa': '\u00a1',
            '\u007f\u007f': '\u047f',
            '\u007f\u007f\u007f': '\u847f',
            'abc': '\u08c3'
        }
        for i, o in cases.items():
            self.assertEqual(compress_snippet(i), o)

    @unittest.skip
    def test_compressProgram(self):
        self.fail()

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
            

    # Test if all codepoints from 0000 to FFFF are valid
    # We wanna test codepoints past that eventually but heck it.
    @unittest.skip
    def test_decompressAllUnicode(self):
        self.fail()


if __name__ == '__main__':
    unittest.main()