from lzma import compress, decompress


def main():
    # Array of test strings made of alphanumeric
    input_string = " ASDMC1231  ASDCAASD231 3DASCASD2323 5488ASDCASDMC 1231ASDCAA SD2313DAS CASD2 3 2 3 5 488ASDC"

    compressed = compress(input_string)
    decompressed = decompress(compressed)
    print(f"Original value: {input_string}")
    if input_string != decompressed:
        print(f"Original Length: {len(input_string)}")
        print(f"Compressed value: {compressed}")
        print(f"Compressed Length: {len(compressed)}")
        print(f"Decompressed value: {decompressed}")
        print(f"Decompressed Length: {len(decompressed)}")
    print(
        f"Original and Decompressed are same: {input_string == decompressed}")
    print("----")


if __name__ == "__main__":
    main()

# ASDMC1236A2D5M
