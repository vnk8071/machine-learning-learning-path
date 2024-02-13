"""
Course: Data Structures & Algorithms
Core: Data Structures
Problem: 6
Code by: KhoiVN
Date: 05/01/2024
"""


class Node:
    def __init__(self, value):
        self.value = value
        self.next = None

    def __repr__(self):
        return str(self.value)


class LinkedList:
    def __init__(self):
        self.head = None

    def __str__(self):
        cur_head = self.head
        out_string = ""
        while cur_head:
            out_string += str(cur_head.value) + " -> "
            cur_head = cur_head.next
        return out_string

    def append(self, value):

        if self.head is None:
            self.head = Node(value)
            return

        node = self.head
        while node.next:
            node = node.next

        node.next = Node(value)

    def size(self):
        size = 0
        node = self.head
        while node:
            size += 1
            node = node.next

        return size


def convert_to_set(linked_list):
    current = linked_list.head
    node_set = set()

    while current:
        node_set.add(current.value)
        current = current.next

    return node_set


def union(list_1, list_2):
    linked_list = LinkedList()
    list_1 = convert_to_set(list_1)
    list_2 = convert_to_set(list_2)
    for item in list_1:
        linked_list.append(item)
    for item in list_2:
        linked_list.append(item)
    return linked_list


def intersection(list_1, list_2):
    linked_list = LinkedList()
    list_1 = convert_to_set(list_1)
    list_2 = convert_to_set(list_2)
    for item in list_1:
        if item in list_2:
            linked_list.append(item)
    return linked_list


# Test case 1

linked_list_1 = LinkedList()
linked_list_2 = LinkedList()

element_1 = [3, 2, 4, 35, 6, 65, 6, 4, 3, 21]
element_2 = [6, 32, 4, 9, 6, 1, 11, 21, 1]

for i in element_1:
    linked_list_1.append(i)

for i in element_2:
    linked_list_2.append(i)

print(union(linked_list_1, linked_list_2))
print(intersection(linked_list_1, linked_list_2))

# Test case 2

linked_list_3 = LinkedList()
linked_list_4 = LinkedList()

element_1 = [3, 2, 4, 35, 6, 65, 6, 4, 3, 23]
element_2 = [1, 7, 8, 9, 11, 21, 1]

for i in element_1:
    linked_list_3.append(i)

for i in element_2:
    linked_list_4.append(i)

print(union(linked_list_3, linked_list_4))
print(intersection(linked_list_3, linked_list_4))


# Test Case 3
assert union(linked_list_1, linked_list_2).size() == 14
assert union(linked_list_3, linked_list_4).size() == 13
assert intersection(linked_list_1, linked_list_2).size() == 3
assert intersection(linked_list_3, linked_list_4).size() == 0

# Edge Case 1
linked_list_5 = LinkedList()
linked_list_6 = LinkedList()

element_1 = [3, 2, 4, 35, 6, 65, 6, 4, 3, 21]
element_2 = []

for i in element_1:
    linked_list_5.append(i)

for i in element_2:
    linked_list_6.append(i)

assert union(linked_list_5, linked_list_6).size() == 7
assert intersection(linked_list_5, linked_list_6).size() == 0

# Edge Case 2
linked_list_7 = LinkedList()
linked_list_8 = LinkedList()

element_1 = []
element_2 = []

for i in element_1:
    linked_list_7.append(i)

for i in element_2:
    linked_list_8.append(i)

assert union(linked_list_7, linked_list_8).size() == 0
assert intersection(linked_list_7, linked_list_8).size() == 0

print("All test cases passed!")
