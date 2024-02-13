# Show me the data structures

## Data Structure Questions

For this project, you will answer the six questions laid out in the next sections. The questions cover a variety of topics related to the data structures you've learned in this course. You will write up a clean and efficient answer in Python, as well as a text explanation of the efficiency of your code and your design choices.

## Problem 1: Least Recently Used Cache

A Least Recently Used (LRU) Cache is a type of cache in which we remove the least recently used entry when the cache memory reaches its limit. For the current problem, consider both get and set operations as an use operation.

Your job is to use an appropriate data structure to implement a LRU cache which has the following methods:

- `set(key, value)`: set the value if the key is not present in the cache. If the cache is at capacity, remove the oldest entry.
- `get(key)`: return the value if the key is present in the cache, otherwise return -1.

Code in `problem_1.py` and explanation in `explanation_problem_1.md`

## Problem 2: File Recursion

For this problem, the goal is to write code for finding all files under a directory (and all directories beneath it) that end with ".c"

Code in `problem_2.py` and explanation in `explanation_problem_2.md`

## Problem 3: Huffman Coding

Huffman coding is a compression algorithm that can be used to compress lists of characters. The algorithm uses a binary tree to assign variable-length codes to each character. The more frequent the character, the shorter the code used to represent it. The binary tree is constructed in such a way that the code assigned to each character is the prefix of any other code assigned to any other character.

Code in `problem_3.py` and explanation in `explanation_problem_3.md`

## Problem 4: Active Directory

In Windows Active Directory, a group can consist of user(s) and group(s) themselves. We can construct this hierarchy as such. Where User is represented by str representing their ids.

Code in `problem_4.py` and explanation in `explanation_problem_4.md`

## Problem 5: Blockchain

A Blockchain is a sequential chain of records, similar to a linked list. Each block contains some information and how it is connected related to the other blocks in the chain. Each block contains a cryptographic hash of the previous block, a timestamp, and transaction data. For our blockchain, we will be using a SHA-256 hash, the Greenwich Mean Time when the block was created, and text strings as the data.

Code in `problem_5.py` and explanation in `explanation_problem_5.md`

## Problem 6: Union and Intersection of Two Linked Lists

Your task for this problem is to fill out the union and intersection functions. The union of two sets A and B is the set of elements which are in A, in B, or in both A and B. The intersection of two sets A and B, denoted by A ∩ B, is the set of all objects that are members of both the sets A and B.

Code in `problem_6.py` and explanation in `explanation_problem_6.md`
