# Rearrange Array Elements

The rearrange_digits function has a time complexity of O(n log n), where n is the size of the input list. This is due to the use of the sorted function, which in Python uses a sorting algorithm called Timsort that has a worst-case time complexity of O(n log n). The subsequent for loop has a time complexity of O(n), but since O(n log n) is the dominant term, it's the one we use to express the overall time complexity.

The space complexity of the rearrange_digits function is O(n), because the sorted function returns a new list that contains all of the elements from the input list. The rest of the function only uses a constant amount of space to store the two output numbers and the loop index and value, so the overall space complexity is determined by the space required for the sorted list.
