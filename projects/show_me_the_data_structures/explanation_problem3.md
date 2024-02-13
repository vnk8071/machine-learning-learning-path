# Huffman Encoding and Decoding

Time Complexity:

- `huffman_encoding(data)`: The time complexity is O(n log n), where n is the number of unique characters in the data. This is because the function uses a priority queue (implemented as a heap) to build the Huffman tree. Inserting an element into a heap takes O(log n) time, and we do this for each unique character.
- `huffman_decoding(data, tree)`: The time complexity is O(m), where m is the length of the encoded data. This is because we traverse the Huffman tree for each bit in the encoded data.

Space Complexity:

- `huffman_encoding(data)`: The space complexity is O(n), where n is the number of unique characters in the data. This is because we create a node for each unique character and store these nodes in a heap. In addition, we create a dictionary to store the Huffman codes.
- `huffman_decoding(data, tree)`: The space complexity is O(n), where n is the number of unique characters in the data. This is because we need to store the Huffman tree. The decoded data also takes up space, but its size is equivalent to the original data, so it doesn't increase the space complexity.
