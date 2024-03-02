# Compression Algorithm

This implements the Lempel-Ziv-Welch (LZW) compression algorithm. It is a lossless compression algorithm that is used to compress data. It is a dictionary-based compression algorithm that works by replacing repeated occurrences of data with references to a single copy of that data existing earlier in the uncompressed data stream.

## Disclaimer - Experimental Use Only

Please do not use these algorithms to compress your files. This is a learning exercise and the algorithms are not optimized for real-world usage. There are many better compression algorithms available that are optimized for speed and compression ratio. For example, the `lzma` module in Python is a better choice for compressing files.

I have implemented these to understand how compression works and to learn about the challenges of implementing a compression algorithm. I am not responsible for any data loss or corruption if you decide to use these for personal use.

## Implementation

There are three implementations/approaches of the algorithm that are provided in [python/lzma](python/lzma/) directory. The implementations are:

### 1. LZW with ASCII input

This works for ASCII 0-255 characters. It uses characters 256 onwards to represent the dictionary entries and thus offers a high compression ratio. In the current state of implementation, it has a ceiling of 1,114,111 total dictionary entries that can be represented which makes it not suitable for large files.

The implementation is in [python/lzma/wlzma.py](python/lzma/wlzma.py).

#### Future work

In future implementations, I will cap the single dictionary encode to 4096 and then start using 2 characters instead to overcome this ceiling. If we assume that most texts are comprised using 52 lowercase and uppercase alphabets, 10 digits, 20 commonly used symbols, and one space, we can choose 2 from 83 (sum) in 3403 ways. Using 4096 (2^12^) will give us enough breathing room to encode most of the possible two-character combinations.

Now if we are to use two characters for encoding, for example, 256 257 for a pattern, then we will have 7,370,880 available dictionary keys to use for encoding (ways to choose 2 from 3840). Once that is exhausted, we can move on to using 3 characters (e.g. 256 257 258) giving us 9,429,812,480 ways to choose them. The tradeoff with bigger encoded strings is that the compression ratio will be lower but it will allow the algorithm to scale to any size of the problem.

**Still Saving Space**: 2^12^ - 2^8^ (3840) means that we will use between 9 bits and up to 12 bits to encode at least two 8-bit characters that take 16 bits (if considered saved as pure ASCII) of space combined.

**Challenges**: The main challenge is to distinguish when we have used a single encoded character and when we have used two.

For example, if we use 256 to encode 'AB' and then we use 256 257 to encode 'DEG', during decompression for 256 257 we need to accurately determine that it is 'DEG' and not 'AB' 257. I can use a delimeter to separate the two encoded characters but that will increase the size of the encoded string and lower the compression ratio.

#### Memory Complications

As the dictionary grows, the space required to store the dictionary will also grow. Therefore, this algorithm can become very memory intensive and may have poor performance for systems with low memory.

#### References

-   [Lempel–Ziv–Welch](https://en.wikipedia.org/wiki/Lempel%E2%80%93Ziv%E2%80%93Welch) - Wikipedia
-   [LZW (Lempel–Ziv–Welch) Compression technique](https://www.geeksforgeeks.org/lzw-lempel-ziv-welch-compression-technique/) - C++ Implementation - GeeksforGeeks

### 2. Limpel-Ziv with Custom Numbering

This approach was based on the idea that we can use a numbering system to encode characters and represent compressed values instead of using 256 onwards to represent the dictionary entries. This will allow us to encode any character and not be limited to 256 characters. The implementation is in [python/lzma/clzma.py](python/lzma/clzma.py).

This algorithm thus works for any filesize but produces a poorer compression ratio as you are required to choose a base for numbering (for example 0-9 is base 10, and saving 11 will require 2 bytes). Therefore, this can often produce a larger file than the original and **is not recommended for use**. This is also slower than the ASCII implementation described above.

**Challenges**: The main challenge is to distinguish when we have used a single encoded character and when we have used two as well as if the text contains any of the symbols used in custom numbering. For example, in this repository implementation, we have used Greek letters to accomplish this. If the text contains Greek letters, the decompression will fail.

#### References

-   [The Beauty of Lempel-Ziv Compression](https://www.youtube.com/watch?v=RV5aUr8sZD0) - Art of the Problem - YouTube

### 3. Limpel-Ziv with Hex Encoding for ASCII

To tackle the challenges of custom numbering, I have implemented a hex-encoding version of the algorithm. This works by translating the input to hex and then using our custom numbering system to encode hex. As 0-255 ASCII hex is base 16, it only uses 4 bits to represent a character. We can then use custom numbering, for example, Q-Z to represent compressed hex values. This implementation is still a work in progress and does not save hex in ideal 4-bits in [python/lzma/hlzma.py](python/lzma/hlzma.py).

#### Require work

This requires more work to see how it will perform in terms of compression ratio and speed. This will require saving the compressed file as binary to gain the space benefits which is not part of implementation yet.

## Usage

To use any of the algorithms, simply run the Python files. You may change the input by editing `main` function in the source file. No external libraries are required to run the code.
