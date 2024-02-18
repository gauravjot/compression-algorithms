from typing import Tuple, Dict

custom_numbering_g_i: Dict[str, int] = {
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
custom_numbering_i_g: Dict[int, str] = {
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


def convertIntToCustom(number: int) -> str:
    result: str = ""
    if number == 0:
        return "α"
    while number > 0:
        result = custom_numbering_i_g[number % 10] + result
        number = number // 10
    return result


def compress(input_string: str) -> str:
    """
    Compress the input string using LZMA algorithm
        - Book is used by LZMA to store the phrase and the corresponding code
    """
    book: Dict[str, int] = {"": 0, " ": 1}
    compressed: str = ""
    phrase: str = ""
    for char in input_string:
        """
        If the character is a number and not in book
            then we do numeric escape and add it to the compressed string
        """
        if char.isnumeric() and char not in book:
            # print(f"{phrase},{char}")
            """
            We first check for prior phrase if it exists
                then we compress it first
            """
            if len(phrase) > 0:
                book, compressed_phrase = _compress_phrase(book, phrase)
                compressed += compressed_phrase
            """
            Now that it is a single char that is a number
                we compress it which it will do numeric escape
            """
            book, compressed_phrase = _compress_phrase(book, char)
            compressed += compressed_phrase
            phrase = ''
            continue
        phrase += char
        if phrase in book:
            continue
        """
        The program encountered a brand new phrase, so we will compress
            it and add to the book
        """
        book, compressed_phrase = _compress_phrase(book, phrase)
        compressed += compressed_phrase
        # if len(book) > 17:
        #     print(f"Book: {book} {len(book)}")
        #     print(f"Phrase: '{phrase}'")
        #     print(f"Compressed: '{compressed}'")
        #     print("----")
        phrase = ''
    compressed += phrase
    # print("----")
    # print(f"Book: {len(book)}")
    # print(f"C Book: {book}")
    return compressed


def decompress(compressed: str) -> str:
    """

    """
    # Book is used by LZMA to store the phrase and the corresponding code
    book: Dict[int, str] = {0: "", 1: " "}
    bookInv: Dict[str, int] = {"": 0, " ": 1}
    decompressed: str = ""
    phrase: str = ""
    numeric_escape_next_char: bool = False
    for char in compressed:
        """

        """
        if char == numeric_escape:
            numeric_escape_next_char = True
            if len(phrase) > 0:
                # Decompress the phrase before
                book, decompressed_phrase, bookInv = _decompress_phrase(
                    book, phrase, bookInv)
                decompressed += decompressed_phrase
                phrase = ''
            continue
        # Add the character to the phrase
        phrase += char
        if numeric_escape_next_char:
            numeric_escape_next_char = False
            decompressed += phrase
            book[len(book)] = phrase
            bookInv[phrase] = len(book)
            phrase = ''
            continue
        """
        If we find a numeric phrase here, then that is a code in book
            and we continue till we find a phrase that is not in book
        """
        if phrase.isnumeric() and int(phrase) in book:
            continue
        """
        Decompress and add it to book
        """
        book, decompressed_phrase, bookInv = _decompress_phrase(
            book, phrase, bookInv)
        decompressed += decompressed_phrase
        # if (len(book) > 15):
        #     print("----")
        #     print(f"Book: {book}")
        #     print(f"Decompress Phrase: {phrase}")
        #     print(f"Decompressed: {decompressed}")
        phrase = ''
    decompressed += phrase
    # print(f"D Book: {book}")
    # print("----")
    return decompressed


def _decompress_phrase(book: Dict[int, str], compressed_phrase: str, bookInv: Dict[str, int]) -> Tuple[Dict[int, str], str, Dict[str, int]]:
    new_code: int = len(book)

    """
    If the compressed phrase is more than 1 character long then we get
    the prefix and get the decompressed value for it from the book.

    Then we add the last character (which is uncompressed) of the compressed
    phrase to the decompressed value and add value it to the book.

    The else case happens because the compressed phrase is actually uncompressed
    """
    if len(compressed_phrase) > 1:
        # eg 1A
        prefix: int = int(compressed_phrase[:-1])
        value_prefix: str = book[prefix]
        decompressed_value: str = value_prefix + compressed_phrase[-1]
    else:
        decompressed_value: str = compressed_phrase

    """
    If the decompressed value is not in the book then we add it to the book
    otherwise we ignore it to avoid duplicates
    """
    if decompressed_value not in bookInv:
        book[new_code] = decompressed_value
        bookInv[decompressed_value] = new_code

    return book, decompressed_value, bookInv


# Book is used by LZMA to store the phrase and the corresponding code
# Returns book and compressed value for phrase
def _compress_phrase(book: Dict[str, int], phrase: str) -> Tuple[Dict[str, int], str]:
    new_code: int = len(book)

    """
    Get phrase without the last character if it's more than 1 character long.

    Assuming a phrase is 'ABB', we check for code of 'AB' in book. If code is
    2 then the compressed value becomes '2B' and we save 'ABB' as 3 in book.

    But if phrase is 'A', we save it as a code in book and return.
    """
    # TODO: Bug, compression cannot be a plain number
    # If it does, then numeric escape the last number
    if len(phrase) > 1:
        prefix: str = phrase[:-1]
        # Prefix should be in book, we get the code for it
        prefix_code: int = book[prefix]
        # We get the compressed value for the phrase
        compressed: str = f"{prefix_code}{phrase[-1]}"
    else:
        compressed: str = phrase
        # Do numeric escape if the phrase is a number
        if phrase.isnumeric():
            compressed = f"{numeric_escape}{compressed}"
    if phrase not in book:
        book[phrase] = new_code
    return book, compressed
