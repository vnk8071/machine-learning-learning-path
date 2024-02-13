# Trie Data Structure

## The `TrieNode` class has different time and space complexities for different operations

1. `__init__` operation:
   - Time complexity: O(1), as it simply initializes a new node with an empty dictionary and a couple of boolean/None values.
   - Space complexity: O(1), as it uses a constant amount of space to store the initialized values.

2. `insert` operation:
   - Time complexity: O(1), as it simply adds a new entry to the dictionary.
   - Space complexity: O(1), as it only creates a single new `TrieNode`.

3. `suffixes` operation:
   - Time complexity: O(n), where n is the total number of nodes in the subtree rooted at this node. This is because it needs to traverse all nodes in the subtree to find all suffixes.
   - Space complexity: O(m), where m is the total number of complete words in the subtree. This is because it needs to store all complete words in the `suffixes` list. In the worst case, every node in the subtree is a complete word, so m could be as large as n.

## The `Trie` class has different time and space complexities for different operations

1. `insert` operation:
   - Time complexity: O(m), where m is the length of the word being inserted. This is because we're simply iterating over the word and inserting each character into the trie.
   - Space complexity: O(m). In the worst case, if the word doesn't share any prefix with the words already in the trie, we need to add m new nodes to the trie.

2. `find` operation:
   - Time complexity: O(m), where m is the length of the word being searched for. This is because we're simply iterating over the word and traversing the trie.
   - Space complexity: O(1). We're not using any additional space that scales with the size of the input.

3. `suffixes` operation:
   - Time complexity: O(n), where n is the total number of characters in all words stored in the trie. This is because in the worst case, we might need to traverse the entire trie to find all suffixes.
   - Space complexity: O(n). In the worst case, we might need to store all characters in the trie in the `suffixes` list.
