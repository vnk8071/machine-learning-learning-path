# blockchain with the ability to append new blocks

Time Complexity:

- `Block.__init__(self, timestamp, data, previous_hash)`: The time complexity is O(1) because it only involves assigning values to instance variables and calculating a hash, which is a constant-time operation for fixed-size inputs.
- `BlockChain.append(self, data)`: The time complexity is O(1) because it involves creating a new block and appending it to the list of blocks, both of which are constant-time operations.

Space Complexity:

- `Block.__init__(self, timestamp, data, previous_hash)`: The space complexity is O(1) because it only involves storing a fixed number of instance variables.
- `BlockChain.append(self, data)`: The space complexity is O(n), where n is the number of blocks in the blockchain. This is because each block is stored in a list, and the size of the list grows linearly with the number of blocks.
