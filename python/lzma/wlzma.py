from typing import Dict


"""
- This works with 0-255 ASCII values
- The range can be increased by changing the ASCII_CUTOFF value. But be mindful of space complexity.
- It encode atleast 2 characters by encoding the current character (or phrase)
    and the next character
- More efficient than the 'clzma.py' implementation in terms of compression ratio
- Efficiency due to better dictionary building

- Does fail for large files and as dictionary size gets over 0x110000
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
    i = 0
    while i in range(len_input_string):
        phrase += input_string[i]
        next_char = input_string[i+1] if i+1 < len_input_string else ''
        if len(next_char) == 0:
            compressed += phrase
            i += 1
            break
        if (phrase + next_char) not in book:
            compressed += phrase if len(phrase) == 1 else book[phrase]
            book[phrase + next_char] = getBookVal(len(book))
            phrase = ''
        i += 1
    # print(f"C Book: {book}")
    return compressed


def decompress(compressed: str) -> str:
    # Book is used by LZMA to store the phrase and the corresponding code
    book: Dict[str, str] = {}
    phrase_fc = compressed[0]   # first character of the first phrase
    cur_char = phrase_fc        # current character
    output = phrase_fc
    i = 0
    while i in range(len(compressed)-1):
        next_char = compressed[i+1]
        if ord(next_char) >= ASCII_CUTOFF and next_char not in book:
            decoded = book[cur_char] if cur_char in book else cur_char
            decoded += phrase_fc
        else:
            decoded = book[next_char] if next_char in book else next_char
        output += decoded
        phrase_fc = decoded[0]
        if ord(cur_char) >= ASCII_CUTOFF:
            book[getBookVal(i)] = book[cur_char] + phrase_fc
        else:
            book[getBookVal(i)] = cur_char + phrase_fc
        i += 1
        cur_char = next_char
    # print(f"D Book: {book}")
    return output


def main():
    input_string = "ABABABAA"
    print(f"\nOriginal value:\n'{input_string}'")
    compressed = compress(input_string)
    print(f"\nCompressed:\n'{compressed}'")
    print(f"\nCompression Ratio:\n{len(compressed)/len(input_string)}")

    decompressed = decompress(compressed)
    print(f"\nDecompressed value:\n'{decompressed}'")
    print(
        f"\nOriginal and Decompressed are same:\n{input_string == decompressed}")


if __name__ == "__main__":
    main()
