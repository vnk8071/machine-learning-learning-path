"""
Course: Data Structures & Algorithms
Core: Data Structures
Problem: 5
Code by: KhoiVN
Date: 05/01/2024
"""

import hashlib
import time


class Block:

    def __init__(self, timestamp, data, previous_hash):
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calc_hash()

    def calc_hash(self):
        sha = hashlib.sha256()
        hash_str = self.data.encode("utf-8")
        sha.update(hash_str)
        return sha.hexdigest()

    def __repr__(self):
        return (
            f"Block({self.timestamp}, {self.data}, {self.previous_hash}, {self.hash})"
        )


class BlockChain:
    def __init__(self):
        self.head = None
        self.tail = None
        self.block = []

    def append(self, data):
        if self.block:
            previous_hash = self.block[-1].hash
        else:
            previous_hash = None

        block = Block(time.time(), data, previous_hash)
        self.block.append(block)

    def __repr__(self):
        return f"BlockChain({self.block})"


# Add your own test cases: include at least three test cases
# and two of them must include edge cases, such as null, empty or very
# large values

block_chain = BlockChain()
block_chain.append("Algorithms")
block_chain.append("Data Structures")
block_chain.append("KhoiVN")

# Test Case 1
assert (
    block_chain.block[0].data == "Algorithms"
), f"Test Case 1 Failed, expected {block_chain.block[0].data}"
assert (
    block_chain.block[1].data == "Data Structures"
), f"Test Case 1 Failed, expected {block_chain.block[1].data}"
assert (
    block_chain.block[2].data == "KhoiVN"
), f"Test Case 1 Failed, expected {block_chain.block[2].data}"

# Test Case 2
assert (
    block_chain.block[0].previous_hash is None
), f"Test Case 2 Failed, expected {block_chain.block[0].previous_hash}"
assert (
    block_chain.block[1].previous_hash
    == "3c34d938281ebe9c3c41c91c11178d9527cd460911135a01f553bcc9b4fc859d"
), f"Test Case 2 Failed, expected {block_chain.block[1].previous_hash}"
assert (
    block_chain.block[2].previous_hash
    == "21692e8647432d796d4aa5d60544feb7c120954721795c19adebfbc8f13516bb"
), f"Test Case 2 Failed, expected {block_chain.block[2].previous_hash}"

# Test Case 3
assert (
    block_chain.block[0].timestamp < block_chain.block[1].timestamp
), f"Test Case 3 Failed, expected {block_chain.block[0].timestamp} < {block_chain.block[1].timestamp}"
assert (
    block_chain.block[1].timestamp < block_chain.block[2].timestamp
), f"Test Case 3 Failed, expected {block_chain.block[1].timestamp} < {block_chain.block[2].timestamp}"

# Edge Test Case 1
block_chain = BlockChain()
block_chain.append("")
block_chain.append("")
assert (
    block_chain.block[0].data == ""
), f"Edge Test Case 1 Failed, expected {block_chain.block[0].data}"
assert (
    block_chain.block[1].data == ""
), f"Edge Test Case 1 Failed, expected {block_chain.block[1].data}"

# Edge Test Case 2
block_chain = BlockChain()
block_chain.append("A" * 10**6)
block_chain.append("B" * 10**6)
assert (
    block_chain.block[0].data == "A" * 10**6
), f"Edge Test Case 2 Failed, expected {block_chain.block[0].data}"
assert (
    block_chain.block[1].data == "B" * 10**6
), f"Edge Test Case 2 Failed, expected {block_chain.block[1].data}"

print("All test cases passed!")
