from typing import Tuple, Dict

"""
This is useful to distinguish between a number and a phrase
    although it has a cost of 1 character added to the compressed string
"""
numeric_escape: str = "Ø"


def compress(input_string: str) -> str:
    """
    Compress the input string using LZMA algorithm
        - Book is used by LZMA to store the phrase and the corresponding code
    """
    book: Dict[str, int] = {"": 0}
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
            if len(phrase) > 0 and phrase not in book:
                book, compressed_phrase = _compress_phrase(
                    book, phrase)
                compressed += compressed_phrase
            elif len(phrase) > 0:
                compressed += phrase
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
        # if len(book) > 110 and len(book) < 120:
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
    Decompress the input string using LZMA algorithm
    """
    # Book is used by LZMA to store the phrase and the corresponding code
    book: Dict[int, str] = {0: ""}
    decompressed: str = ""
    phrase: str = ""
    vals_in_book: list[str] = []
    numeric_escape_next_char: bool = False
    for char in compressed:
        """
        If the character is numeric_escape then
            - we set the flag to True
            - we just ignore the numeric_escape character
            - decompress the phrase before it
            - and continue to the next character that we simply
                add to the decompressed string and book
        """
        if char == numeric_escape:
            numeric_escape_next_char = True
            if len(phrase) > 0:
                # Decompress the phrase before
                book, decompressed_phrase, vals_in_book = _decompress_phrase(
                    book, phrase, vals_in_book)
                decompressed += decompressed_phrase
                phrase = ''
            continue
        phrase += char
        if numeric_escape_next_char:
            numeric_escape_next_char = False
            decompressed += phrase
            book[len(book)] = phrase
            vals_in_book.append(phrase)
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
        book, decompressed_phrase, vals_in_book = _decompress_phrase(
            book, phrase, vals_in_book)
        decompressed += decompressed_phrase
        # if (len(book) > 124):
        #     print(f"Book: {book}")
        #     print(f"Decompress Phrase: {phrase}")
        #     print(f"Decompressed: {decompressed}")
        #     print("----")
        phrase = ''
    decompressed += phrase
    # print(f"D Book: {book}")
    return decompressed


def _decompress_phrase(book: Dict[int, str], compressed_phrase: str, vals_in_book: list[str]) -> Tuple[Dict[int, str], str, list[str]]:
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
    if decompressed_value not in vals_in_book:
        vals_in_book.append(decompressed_value)
        book[new_code] = decompressed_value

    return book, decompressed_value, vals_in_book


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
    if len(phrase) > 1:
        prefix: str = phrase[:-1]
        # Prefix should be in book, we get the code for it
        prefix_code: int = book[prefix]
        # We get the compressed value for the phrase
        compressed: str = f"{prefix_code}{phrase[-1]}"
        # Save the phrase in book
        book[phrase] = new_code
    else:
        # Save the phrase in book
        book[phrase] = new_code
        compressed: str = phrase
        # Do numeric escape if the phrase is a number
        if phrase.isnumeric():
            compressed = f"{numeric_escape}{compressed}"
    return book, compressed
