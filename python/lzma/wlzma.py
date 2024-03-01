from typing import Dict


"""
- This works with 0-255 ASCII values
- The range can be increased by changing the ASCII_CUTOFF value. But be mindful of space complexity.
- It encode atleast 2 characters by encoding the current character (or phrase)
    and the next character
- More efficient than the 'clzma.py' implementation in terms of compression ratio
- Efficiency due to better dictionary building
"""


ASCII_CUTOFF = 256


def getBookVal(number: int) -> str:
    number += ASCII_CUTOFF  # to avoid ASCII values
    return chr(number)


def compress(input_string: str) -> str:
    book: Dict[str, str] = {}
    compressed: str = ""
    phrase: str = ""
    len_input_string = len(input_string)
    for i in range(len_input_string):
        phrase += input_string[i]
        next_char = input_string[i+1] if i+1 < len_input_string else ''
        if len(next_char) == 0:
            compressed += phrase
            break
        if (phrase + next_char) not in book:
            compressed += phrase if len(phrase) == 1 else book[phrase]
            book[phrase + next_char] = getBookVal(len(book))
            phrase = ''
        else:
            continue
    return compressed


def decompress(compressed: str) -> str:
    # Book is used by LZMA to store the phrase and the corresponding code
    book: Dict[str, str] = {}
    decompressed: str = ""
    phrase: str = ""
    len_compressed = len(compressed)
    i = 0
    while i in range(len_compressed):
        phrase = compressed[i]
        next_char = compressed[i+1] if i+1 < len_compressed else ''
        # Output based on phrase
        if ord(phrase) < ASCII_CUTOFF:
            output = phrase
        else:
            output = book[phrase]
        decompressed += output
        # If we have reached the end of the compressed string, exit
        if len(next_char) == 0:
            break
        # If the next character is ASCII, then save it in the book
        try:
            if ord(next_char) < ASCII_CUTOFF:
                book[getBookVal(len(book))] = output + next_char
            else:
                # If the next character is not ASCII, then find the corresponding
                # value in the book and save output + the first character of it
                book[getBookVal(len(book))] = output + book[next_char][0]
        except KeyError as e:
            print(f"Decompressed: {decompressed}")
            print(f"Output: {output}")
            print(f"next char: {next_char}")
            print(f"d Book: {book}")
            # throw error
            raise Exception(f"KeyError: {e}")
        i += 1
    return decompressed


def main():
    # Array of test strings made of alphanumeric
    # the air was thin and the temperature plunged below freezing"
    input_string = "ABABABAA"
    print(f"Original value: {input_string}")
    compressed = compress(input_string)
    print(f"Compressed: '{compressed}'")
    print(f"Compression Ratio: {len(compressed)/len(input_string)}")

    decompressed = decompress(compressed)
    print(f"Decompressed value: '{decompressed}'")
    print(
        f"Original and Decompressed are same: {input_string == decompressed}")


if __name__ == "__main__":
    main()
