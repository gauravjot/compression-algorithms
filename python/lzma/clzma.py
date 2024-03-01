from typing import Tuple, Dict

"""
- This uses greek letters to encode compressed values
- The dictionary can have single input string characters which
    make it not very efficient
- The compression ratio is usually not very good
"""

custom_numbering_c_i: Dict[str, int] = {
    "α": 0,
    "β": 1,
    "γ": 2,
    "δ": 3,
    "ε": 4,
    "ζ": 5,
    "η": 6,
    "θ": 7,
    "ι": 8,
    "κ": 9
}

custom_numbering_i_c: Dict[int, str] = {
    0: "α",
    1: "β",
    2: "γ",
    3: "δ",
    4: "ε",
    5: "ζ",
    6: "η",
    7: "θ",
    8: "ι",
    9: "κ"
}


def doBase10ToCustomNum(number: int) -> str:
    result: str = ""
    if number == 0:
        return "α"
    while number > 0:
        result = custom_numbering_i_c[number % 10] + result
        number = number // 10
    return result


def compress(input_string: str) -> str:
    book: Dict[str, str] = {}
    compressed: str = ""
    phrase: str = ""
    for char in input_string:
        phrase += char
        if phrase in book:
            continue
        book, compressed_phrase = _compress_phrase(book, phrase)
        compressed += compressed_phrase
        phrase = ''
    compressed += phrase
    # print(f"C Book: {book}")
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
        phrase += compressed[i:i+1]
        i += 1
        if phrase in book:
            continue
        try:
            if len(phrase) > 1:
                prefix = phrase[:-1]
                decompressed_val_prefix = book[prefix]
                decompressed_val = decompressed_val_prefix + phrase[-1]
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
    return decompressed


# Book is used by LZMA to store the phrase and the corresponding code
# Returns book and compressed value for phrase
def _compress_phrase(book: Dict[str, int], phrase: str) -> Tuple[Dict[str, int], str]:
    new_code: str = doBase10ToCustomNum(len(book))

    if len(phrase) > 1:
        prefix: str = phrase[:-1]
        # Prefix should be in book, we get the code for it
        prefix_code: int = book[prefix]
        # We get the compressed value for the phrase
        compressed: str = f"{prefix_code}{phrase[-1]}"
    else:
        compressed: str = phrase
    if phrase not in book:
        book[phrase] = new_code
    return book, compressed


def main():
    # Array of test strings made of alphanumeric
    input_string = "In the shadow of Mount Everest, where the air was thin and the temperature plunged below freezing"
    print(f"Original value: {input_string}")
    compressed = compress(input_string)
    print(f"Compressed: {compressed}")
    print(f"Compression Ratio: {len(compressed)/len(input_string)}")

    decompressed = decompress(compressed)
    print(f"Decompressed value: {decompressed}")
    print(
        f"Original and Decompressed are same: {input_string == decompressed}")


if __name__ == "__main__":
    main()
