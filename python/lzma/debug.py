from lzma import compress, decompress


def main():
    # Array of test strings made of alphanumeric
    input_string = "ASDMC1231ASDCAASD2313DASCASD23235488ASDCASDMC1231ASDCAASD2313DASCASD23235488ASDC"

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
