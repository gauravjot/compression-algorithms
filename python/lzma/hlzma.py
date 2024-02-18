from typing import Tuple, Dict

custom_numbering_c_i: Dict[str, int] = {
    "Q": 0,
    "R": 1,
    "S": 2,
    "T": 3,
    "U": 4,
    "V": 5,
    "W": 6,
    "X": 7,
    "Y": 8,
    "Z": 9
}

custom_numbering_i_c: Dict[int, str] = {
    0: "Q",
    1: "R",
    2: "S",
    3: "T",
    4: "U",
    5: "V",
    6: "W",
    7: "X",
    8: "Y",
    9: "Z"
}


def doBase10ToCustomNum(number: int) -> str:
    result: str = ""
    if number == 0:
        return "Q"
    while number > 0:
        result = custom_numbering_i_c[number % 10] + result
        number = number // 10
    return result


def compress(input_string: str) -> str:
    book: Dict[str, str] = {}
    compressed: str = ""
    phrase: str = ""
    hex_list = convertStrToHex(input_string).split(":")
    for char in hex_list:
        phrase += char
        if phrase in book:
            continue
        book, compressed_phrase = _compress_phrase(book, phrase, len(char))
        compressed += compressed_phrase
        phrase = ''
    compressed += phrase
    # print(f"Book: {book}")
    return compressed


def decompress(compressed: str) -> str:
    """
    Decompress the input string using LZMA algorithm
    """
    # Book is used by LZMA to store the phrase and the corresponding code
    book: Dict[str, str] = {}
    decompressed: str = ""
    phrase: str = ""
    i: int = 0
    while i < len(compressed):
        """
            If we don't encounter Q-Z then it is hex
        """
        if compressed[i] not in custom_numbering_c_i:
            # hex can be of length upto 4 but we are supporting it 2
            phrase += compressed[i:i+2]
            i += 2
        else:
            phrase += compressed[i:i+1]
            i += 1

        """
            We have encoded hex
        """
        if phrase in book:
            continue
        try:
            if len(phrase) > 2:
                prefix = phrase[:-2]
                decompressed_val_prefix = book[prefix]
                decompressed_val = decompressed_val_prefix + phrase[-2:]
            else:
                decompressed_val = phrase
            book[doBase10ToCustomNum(len(book))] = decompressed_val
            decompressed += decompressed_val
            phrase = ''
        except KeyError as e:
            print(f"d Book: {book}")
            # throw error
            raise Exception(f"KeyError: {e}")
    # print(f"d Book: {book}")
    return convertHexToStr(decompressed)


# Book is used by LZMA to store the phrase and the corresponding code
# Returns book and compressed value for phrase
def _compress_phrase(book: Dict[str, int], phrase: str, last_char_len) -> Tuple[Dict[str, int], str]:
    new_code: str = doBase10ToCustomNum(len(book))

    if len(phrase[:-last_char_len]) > 1:
        prefix: str = phrase[:-last_char_len]
        # Prefix should be in book, we get the code for it
        prefix_code: int = book[prefix]
        # We get the compressed value for the phrase
        compressed: str = f"{prefix_code}{phrase[-last_char_len:]}"
    else:
        compressed: str = phrase
    if phrase not in book:
        book[phrase] = new_code
    return book, compressed


def convertStrToHex(s):
    return ":".join("{:02x}".format(ord(c)) for c in s)


def convertHexToStr(s):
    return "".join(chr(int(s[i:i+2], 16)) for i in range(0, len(s), 2))


def main():
    # Array of test strings made of alphanumeric
    input_string = "Hello world! This is a test string."
    print(f"Original value: {input_string}")
    print(f"Hex: {convertStrToHex(input_string)}")
    compressed = compress(input_string)
    print(f"Compressed: {compressed}")
    print(f"Compression Ratio: {len(compressed)/len(input_string)}")

    decompressed = decompress(compressed)
    print(f"Decompressed value: {decompressed}")
    print(
        f"Original and Decompressed are same: {input_string == decompressed}")


if __name__ == "__main__":
    main()
