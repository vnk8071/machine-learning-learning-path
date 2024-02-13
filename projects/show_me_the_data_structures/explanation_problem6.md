# inked list and provides functions to find the union and intersection of two linked lists

Time Complexity:

- `LinkedList.append(value)`: The time complexity is O(n), where n is the number of nodes in the linked list. This is because in the worst-case scenario, the function needs to traverse the entire list to find the last node.
- `LinkedList.size()`: The time complexity is O(n), where n is the number of nodes in the linked list. This is because the function needs to traverse the entire list to count the nodes.
- `convert_to_set(linked_list)`: The time complexity is O(n), where n is the number of nodes in the linked list. This is because the function needs to traverse the entire list to add each node to the set.
- `union(list_1, list_2)` and `intersection(list_1, list_2)`: The time complexity is O(n + m), where n and m are the number of nodes in list_1 and list_2, respectively. This is because the functions need to convert each list to a set and then iterate over the sets.

Space Complexity:

- `LinkedList.append(value) and LinkedList.size()`: The space complexity is O(1) because these functions only use a constant amount of space to store temporary variables.
- `convert_to_set(linked_list)`: The space complexity is O(n), where n is the number of nodes in the linked list. This is because the function creates a set that contains all the nodes in the list.
- `union(list_1, list_2)` and `intersection(list_1, list_2)`: The space complexity is O(n + m), where n and m are the number of nodes in list_1 and list_2, respectively. This is because the functions create a new linked list to store the result, and the size of the result can be up to n + m nodes.
