import unittest
from src.compression import decompress_program, compress_program


class TestConsistency(unittest.TestCase):
    def test_consistency(self):
        cases = [
            '345ab1vv3v',
            'ncvc1qw94asjkc2m93p1asj2d1cj3p1a1cj',
            '`!dlroW ,olleH`\u007f'
        ]
        for i in cases:
            self.assertEqual(
                decompress_program(compress_program(i)), i
            )
    
    # Calling compression on a compressed string should do nothing
    def test_multiple_compress(self):
        cases = [
            '345ab1vv3v',
            'ncvc1qw94asjkc2m93p1asj2d1cj3p1a1cj',
            '`!dlroW ,olleH`\u007f'
        ]
        for i in cases:
            self.assertEqual(
                compress_program(i),
                compress_program(compress_program(i))
            )
    
    # Calling decompression on a decompressed string _really_ shouldn't do anything.
    def test_multiple_decompress(self):
        cases = [
            '345ab1vv3v'
            'ncvc1qw94asjkc2m93p1asj2d1cj3p1a1cj',
            '`!dlroW ,olleH`\u007f'
        ]
        for i in cases:
            self.assertEqual(decompress_program(decompress_program(i)), i)


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
    def test_decompressProgram(self):
        cases = {
            '\u00a1': 'aa',
            '\u00a2': 'ab',
            '\u0081': '`a',
            '\u00bf': 'a\u007f',
            '\u0461': '\u007fa',
            '\u009f': '`\u007f',
            '\u0460': '\u007f`'
        }
        for i, o in cases.items():
            self.assertEqual(decompress_program(i), o)

if __name__ == '__main__':
    unittest.main()