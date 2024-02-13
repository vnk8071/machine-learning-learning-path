# Router Traversal and Lookup

## The `RouteTrie` class has different time and space complexities for different operations

1. `insert` operation:
   - Time complexity: O(m), where m is the number of parts in the path. This is because we're simply iterating over the path and inserting each part into the trie.
   - Space complexity: O(m). In the worst case, if the path doesn't share any prefix with the paths already in the trie, we need to add m new nodes to the trie.

2. `find` operation:
   - Time complexity: O(m), where m is the number of parts in the path being searched for. This is because we're simply iterating over the path and traversing the trie.
   - Space complexity: O(1). We're not using any additional space that scales with the size of the input.

3. `_split_path` operation:
   - Time complexity: O(m), where m is the length of the path string. This is because we need to iterate over the string to split it into parts.
   - Space complexity: O(m). The `split` function returns a new list that contains all of the parts of the path, so we need an amount of space proportional to the size of the path to store this list.

## The `Router` class has different time and space complexities for different operations

1. `__init__` operation:
   - Time complexity: O(1), as it simply initializes a new `RouteTrie`.
   - Space complexity: O(1), as it uses a constant amount of space to store the `RouteTrie`.

2. `add_handler` operation:
   - Time complexity: O(m), where m is the number of parts in the path. This is because it needs to split the path and insert it into the `RouteTrie`.
   - Space complexity: O(m). In the worst case, if the path doesn't share any prefix with the paths already in the trie, we need to add m new nodes to the trie.

3. `lookup` operation:
   - Time complexity: O(m), where m is the number of parts in the path being searched for. This is because it needs to find the path in the `RouteTrie`.
   - Space complexity: O(1). We're not using any additional space that scales with the size of the input.

4. `split_path` operation:
   - Time complexity: O(m), where m is the length of the path string. This is because we need to iterate over the string to split it into parts.
   - Space complexity: O(m). The `split` function returns a new list that contains all of the parts of the path, so we need an amount of space proportional to the size of the path to store this list.
