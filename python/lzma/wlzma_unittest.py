from wlzma import compress, decompress
import time
import unittest
import os


class TestLZMA(unittest.TestCase):

    def test_binary_numeric(self):
        s = "122122112211122112221122112111212221222111"
        perform_test(s, self)

    def test_alphabet_string1(self):
        s = "ABABABAABAB"
        perform_test(s, self)

    def test_alphabet_string2(self):
        s = "ASDCNNCASSSMCCAMSDMMDSASDASDCNNCASSSMCCAMSDMMDSASD"
        perform_test(s, self)

    def test_alphabet_string3(self):
        s = "ASDCNNCASSSMCCAMSDMMDSASDASDCNNCASSSMCCAMSDMMDSASDASDCNNCASSSMCCAMSDMMDSASD"
        perform_test(s, self)

    def test_alphanumeric_string1(self):
        s = "ASDMC1231ASDCAASD2313DASCASD23235488ASDCASDMC1231ASDCAASD2313DASCASD23235488ASDCASDMC1231ASDCAASD2313DASCASD23235488ASDC"
        perform_test(s, self)

    def test_alphanumeric_string2(self):
        s = "ASDMC1231ASDCAASD2313DASCASD23235488ASDCASDMC1231ASDCAASD2313DASCASD23235488ASDC"
        perform_test(s, self)

    def test_alphanumeric_with_space_string1(self):
        s = "ASDM C1231 ASDCA ASD23 13DASCASD232354 88ASDCASDMC1231AS DCAASD  2313DASC ASD2323548 8ASDC    ASDM C1231ASDCAA  SD2313D ASCASD23235488ASDC "
        perform_test(s, self)

    def test_alphanumeric_with_space_string2(self):
        s = " ASDMC1231  ASDCAASD231 3DASCASD2323 5488ASDCASDMC 1231ASDCAA SD2313DAS CASD2 3 2 3 5 488ASDC"
        perform_test(s, self)

    def test_complex1(self):
        s = "ASCII, stands for American Standard Code for Information Interchange. It is a 7-bit character code where each individual bit represents a unique character. This page shows the extended ASCII table which is based on the Windows-1252 character set which is an 8 bit ASCII table with 256 characters and symbols."
        perform_test(s, self)

    def test_complex2(self):
        s = "In the heart of the sprawling city, nestled between skyscrapers and bustling streets, lay a forgotten park. Its once vibrant foliage now wilted with neglect, whispered secrets of days gone by. Hannah found solace in its overgrown paths, weaving through memories as tangled as the ivy that adorned its crumbling walls. Each step brought echoes of laughter and tears, mingling with the rustle of fallen leaves. Here, beneath the watchful gaze of weathered statues, she found sanctuary from the chaos of the world, a place where time stood still and dreams took flight on the wings of forgotten whispers."
        perform_test(s, self)

    def test_complex3(self):
        s = "In the neon-lit streets of Sector 7B, where the echoes of a thousand footsteps merged with the hum of machinery, stood an old diner, its sign flickering like a heartbeat on the edge of oblivion. The air crackled with the energy of a city that never slept, each moment measured in the pulse of digital displays and the blur of passing cars. Behind the counter, Sam poured cups of steaming coffee, the aroma mingling with the sharp tang of grease and dreams deferred. The diner was a haven for lost souls and weary travelers, where stories unfolded like chapters in a book, each booth a sanctuary from the relentless march of time. Amidst the clatter of dishes and the drone of conversation, Sam found solace in the rhythm of the night, where numbers danced like fireflies in the darkness, guiding lost souls home."
        perform_test(s, self)

    def test_complex4(self):
        s = "In the shadow of Mount Everest, where the air was thin and the temperature plunged below freezing, a team of climbers embarked on a journey to conquer the world's tallest peak. With a base camp situated at an altitude of 5,000 meters, they braved avalanches and crevasses in their quest to reach the summit, their determination unwavering despite the odds."
        perform_test(s, self)

    def test_large_file1(self):
        test_file("test_files/ai_generated1.txt", self)

    def test_large_file2(self):
        test_file("test_files/ohms_law.txt", self)

    def test_large_file3(self):
        test_file("test_files/psychology.txt", self)

    def test_large_file4(self):
        test_file("test_files/bigfile.txt", self)

    def test_large_file5(self):
        test_file("test_files/bigfile2.txt", self)

    def test_large_file6(self):
        test_file("test_files/bigfile10.txt", self)


"""
    Helper functions
"""


def perform_test(test_string: str, self):
    print("\n======================================================================")
    print(f"Test: {self.id()}")
    print("----------------------------------------------------------------------\n")

    # track time
    start_time = time.time()
    compressed = compress(test_string)
    time2 = time.time()
    print("Compression done in\t: {:.10f}s".format(time2 - start_time))
    print(f"Compression Ratio\t: {compression_ratio(test_string, compressed)}")
    decompressed = decompress(compressed)
    print("Decompression done in\t: {:.10f}s".format(time.time() - time2))
    result = test_string == decompressed
    print("Total Time\t\t: {:.10f}s".format(time.time() - start_time))

    if result:
        print(f"Test passed\n")

    self.assertTrue(result)

    return (
        test_string == decompressed,
        compression_ratio(test_string, compressed),
        time.time() - start_time
    )


def test_file(file_path: str, self):
    with open(os.path.join(os.path.dirname(__file__), file_path), "r") as f:
        test_string = f.read()
        perform_test(test_string, self)


def compression_ratio(original: str, compressed: str) -> float:
    return len(compressed) / len(original)


def doesContainASCII(s: str) -> bool:
    return all(ord(c) < 256 for c in s)


if __name__ == "__main__":
    unittest.main()
