"""
Course: Data Structures & Algorithms
Core: Data Structures
Problem: 3
Code by: KhoiVN
Date: 04/01/2024
"""

import sys
import heapq
from collections import Counter


class Node:
    def __init__(self, value=None, freq=0, left=None, right=None):
        self.value = value
        self.freq = freq
        self.left = left
        self.right = right

    def __lt__(self, other):
        return self.freq < other.freq

    def build_code(self, prefix="", code={}):
        if self.value:
            code[self.value] = prefix
        if self.left:
            self.left.build_code(prefix + "0", code)
        if self.right:
            self.right.build_code(prefix + "1", code)
        return code

    def encode_data(self, data):
        return "".join([self.build_code()[char] for char in data])

    def __repr__(self) -> str:
        return f"Node({self.value}, {self.freq})"


def huffman_encoding(data="AAAAAAABBBCCCCCCCDDEEEEEE"):
    if not data or len(data) == 0:
        return "", None
    counter = Counter(data)
    if len(counter) == 1:
        return "0" * len(data), Node(None, len(data))
    list_node = [Node(value, freq) for value, freq in counter.items()]
    heapq.heapify(list_node)

    while len(list_node) > 1:
        left = heapq.heappop(list_node)
        right = heapq.heappop(list_node)
        parent = Node(None, left.freq + right.freq, left, right)
        heapq.heappush(list_node, parent)

    tree = list_node[0]
    code = tree.encode_data(data)

    return code, tree


def huffman_decoding(data, tree):
    result = ""
    node = tree
    for bit in data:
        if bit == "0":
            node = node.left
        else:
            node = node.right
        if node.value:
            result += node.value
            node = tree
    return result


code, tree = huffman_encoding("AAAAAAABBBCCCCCCCDDEEEEEE")

# Test Case 1
assert (
    code == "1010101010101000100100111111111111111000000010101010101"
), f"Test Case 1 Failed, expected {code}"
assert tree.value is None, f"Test Case 1 Failed, expected {tree.value}"


result = huffman_decoding(code, tree)
# Test Case 2
assert result == "AAAAAAABBBCCCCCCCDDEEEEEE", f"Test Case 2 Failed, expected {result}"
assert len(result) == 25, f"Test Case 2 Failed, expected {len(result)}"

# Test Case 3
assert huffman_encoding("") == (
    "", None), "Test Case 3 Failed, expected ('', None)"
assert huffman_decoding("", None) == "", "Test Case 3 Failed, expected ''"


# Edge Case 1
assert huffman_encoding(None) == (
    "", None), "Edge Case 1 Failed, expected ('', None)"
assert huffman_decoding("", None) == "", "Edge Case 1 Failed, expected ''"

# Edge Case 2
assert huffman_encoding("A" * 10)[0] == "0" * \
    10, "Edge Case 2 Failed, expected '0'*10"
assert huffman_decoding("0" * 0, Node(None, 0)
                        ) == "", "Edge Case 2 Failed, expected ''"

print("All test cases passed!")

if __name__ == "__main__":
    codes = {}

    a_great_sentence = "The bird is the word"

    print("The size of the data is: {}\n".format(
        sys.getsizeof(a_great_sentence)))
    print("The content of the data is: {}\n".format(a_great_sentence))

    encoded_data, tree = huffman_encoding(a_great_sentence)

    print(
        "The size of the encoded data is: {}\n".format(
            sys.getsizeof(int(encoded_data, base=2))
        )
    )
    print("The content of the encoded data is: {}\n".format(encoded_data))

    decoded_data = huffman_decoding(encoded_data, tree)

    print(
        "The size of the decoded data is: {}\n".format(
            sys.getsizeof(decoded_data)))
    print("The content of the encoded data is: {}\n".format(decoded_data))
