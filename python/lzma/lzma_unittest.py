from lzma import compress, decompress
import unittest


class TestLZMA(unittest.TestCase):

    def test_lzma(self):
        test_strings = [
            "122122112211122112221122112111212221222111",
            "ABABABAABAB",
            "AABABABABAB",
            "ASDCNNCASSSMCCAMSDMMDSASD",
            "ASDCNNCASSSMCCAMSDMMDSASDASDCNNCASSSMCCAMSDMMDSASD",
            "ASDCNNCASSSMCCAMSDMMDSASDASDCNNCASSSMCCAMSDMMDSASDASDCNNCASSSMCCAMSDMMDSASD",
            "ASDMC1231ASDCM",
            "ASDMC1231ASDCAASD2313DASCASD23235488ASDCASDMC1231ASDCAASD2313DASCASD23235488ASDC",
            "ASDMC1231ASDCAASD2313DASCASD23235488ASDCASDMC1231ASDCAASD2313DASCASD23235488ASDCASDMC1231ASDCAASD2313DASCASD23235488ASDC",
            "ASCII, stands for American Standard Code for Information Interchange. It is a 7-bit character code where each individual bit represents a unique character. This page shows the extended ASCII table which is based on the Windows-1252 character set which is an 8 bit ASCII table with 256 characters and symbols."
        ]
        for test_string in test_strings:
            compressed = compress(test_string)
            decompressed = decompress(compressed)
            self.assertEqual(test_string, decompressed)


if __name__ == "__main__":
    unittest.main()
