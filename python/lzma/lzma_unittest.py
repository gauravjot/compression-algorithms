from lzma import compress, decompress
import time
import unittest


class TestLZMA(unittest.TestCase):

    def test_binary_numeric(self):
        test_string = "122122112211122112221122112111212221222111"
        result, compression_ratio, time_delta = perform_test(test_string)
        if result:
            print_stats(self.id(), test_string,
                        compression_ratio, time_delta)
        self.assertTrue(result, f"\n\tTest failed for string: \n{test_string}")

    def test_alphabet_string1(self):
        test_string = "ABABABAABAB"
        result, compression_ratio, time_delta = perform_test(test_string)
        if result:
            print_stats(self.id(), test_string,
                        compression_ratio, time_delta)
        self.assertTrue(result, f"\n\tTest failed for string: \n{test_string}")

    def test_alphabet_string2(self):
        test_string = "ASDCNNCASSSMCCAMSDMMDSASDASDCNNCASSSMCCAMSDMMDSASD"
        result, compression_ratio, time_delta = perform_test(test_string)
        if result:
            print_stats(self.id(), test_string,
                        compression_ratio, time_delta)
        self.assertTrue(result, f"\n\tTest failed for string: \n{test_string}")

    def test_alphabet_string3(self):
        test_string = "ASDCNNCASSSMCCAMSDMMDSASDASDCNNCASSSMCCAMSDMMDSASDASDCNNCASSSMCCAMSDMMDSASD"
        result, compression_ratio, time_delta = perform_test(test_string)
        if result:
            print_stats(self.id(), test_string,
                        compression_ratio, time_delta)
        self.assertTrue(result, f"\n\tTest failed for string: \n{test_string}")

    def test_alphanumeric_string1(self):
        test_string = "ASDMC1231ASDCAASD2313DASCASD23235488ASDCASDMC1231ASDCAASD2313DASCASD23235488ASDCASDMC1231ASDCAASD2313DASCASD23235488ASDC"
        result, compression_ratio, time_delta = perform_test(test_string)
        if result:
            print_stats(self.id(), test_string,
                        compression_ratio, time_delta)
        self.assertTrue(result, f"\n\tTest failed for string: \n{test_string}")

    def test_alphanumeric_string2(self):
        test_string = "ASDMC1231ASDCAASD2313DASCASD23235488ASDCASDMC1231ASDCAASD2313DASCASD23235488ASDC"
        result, compression_ratio, time_delta = perform_test(test_string)
        if result:
            print_stats(self.id(), test_string,
                        compression_ratio, time_delta)
        self.assertTrue(result, f"\n\tTest failed for string: \n{test_string}")

    def test_alphanumeric_with_space_string1(self):
        test_string = "ASDM C1231 ASDCA ASD23 13DASCASD232354 88ASDCASDMC1231AS DCAASD  2313DASC ASD2323548 8ASDC    ASDM C1231ASDCAA  SD2313D ASCASD23235488ASDC "
        result, compression_ratio, time_delta = perform_test(test_string)
        if result:
            print_stats(self.id(), test_string,
                        compression_ratio, time_delta)
        self.assertTrue(result, f"\n\tTest failed for string: \n{test_string}")

    def test_alphanumeric_with_space_string2(self):
        test_string = " ASDMC1231  ASDCAASD231 3DASCASD2323 5488ASDCASDMC 1231ASDCAA SD2313DAS CASD2 3 2 3 5 488ASDC"
        result, compression_ratio, time_delta = perform_test(test_string)
        if result:
            print_stats(self.id(), test_string,
                        compression_ratio, time_delta)
        self.assertTrue(result, f"\n\tTest failed for string: \n{test_string}")

    def test_complex1(self):
        test_string = "ASCII, stands for American Standard Code for Information Interchange. It is a 7-bit character code where each individual bit represents a unique character. This page shows the extended ASCII table which is based on the Windows-1252 character set which is an 8 bit ASCII table with 256 characters and symbols."
        result, compression_ratio, time_delta = perform_test(test_string)
        if result:
            print_stats(self.id(), test_string,
                        compression_ratio, time_delta)
        self.assertTrue(result, f"\n\tTest failed for string: \n{test_string}")


"""
    Helper functions
"""


def compression_ratio(original: str, compressed: str) -> float:
    return len(compressed) / len(original)


def perform_test(test_string: str):
    # track time
    start_time = time.time()
    compressed = compress(test_string)
    decompressed = decompress(compressed)

    return (
        test_string == decompressed,
        compression_ratio(test_string, compressed),
        time.time() - start_time
    )


def print_stats(test_name: str, test_string: str, compression_ratio: float, time_delta: float):
    print("\n======================================================================")
    print(f"Test passed : {test_name}")
    print("----------------------------------------------------------------------\n")
    print(f"String\t\t\t: {test_string}")
    print(f"Compression Ratio\t: {compression_ratio}")
    print("Time\t\t\t: {:.10f}s\n".format(time_delta))


if __name__ == "__main__":
    unittest.main()
