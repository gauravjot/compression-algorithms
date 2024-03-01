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
    # print(f"C Book: {book}")
    return compressed


def decompress(compressed: str) -> str:
    # Book is used by LZMA to store the phrase and the corresponding code
    decompressed: str = ""
    book: Dict[int, str] = {}
    for i in range(ASCII_CUTOFF):
        book[i] = chr(i)
    old_code = ord(compressed[0])
    str1 = book[old_code]
    str2 = str1[0]
    decompressed += str1
    count = ASCII_CUTOFF
    for i in range(len(compressed)-1):
        next_char = ord(compressed[i+1])
        if next_char not in book:
            str1 = book[old_code]
            str1 += str2
        else:
            str1 = book[next_char]
        decompressed += str1
        str2 = str1[0]
        book[count] = book[old_code] + str2
        count += 1
        old_code = next_char
    # print(f"D Book: {book}")
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
