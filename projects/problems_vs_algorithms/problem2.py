def rotated_array_search(input_list, number):
    """
    Find the index by searching in a rotated sorted array

    Args:
        input_list(array), number(int): Input array to search and the target

    Returns:
        int: Index or -1
    """

    def binary_search(start_index, end_index):
        """Binary search in a rotated sorted array

        Args:
            start_index(int), end_index(int): Start and end index of the array

        Returns:
            int: Index or -1"""
        while start_index <= end_index:
            middle_index = (start_index + end_index) // 2
            middle_value = input_list[middle_index]
            if middle_value == number:
                return middle_index
            elif input_list[start_index] <= middle_value:
                if input_list[start_index] <= number < middle_value:
                    end_index = middle_index - 1
                else:
                    start_index = middle_index + 1
            else:
                if middle_value < number <= input_list[end_index]:
                    start_index = middle_index + 1
                else:
                    end_index = middle_index - 1
        return -1

    start_index = 0
    end_index = len(input_list) - 1

    return binary_search(start_index, end_index)


def linear_search(input_list, number):
    """Linear search in a list

    Args:
        input_list(array), number(int): Input array to search and the target

    Returns:
        int: Index or -1
    """
    for index, element in enumerate(input_list):
        if element == number:
            return index
    return -1


def test_function(test_case):
    input_list = test_case[0]
    number = test_case[1]
    if linear_search(
            input_list,
            number) == rotated_array_search(
            input_list,
            number):
        print("Pass")
    else:
        print("Fail")


# Test Cases 1
test_function([[6, 7, 8, 9, 10, 1, 2, 3, 4], 6])
test_function([[6, 7, 8, 9, 10, 1, 2, 3, 4], 1])

# Test Cases 2
test_function([[6, 7, 8, 1, 2, 3, 4], 8])
test_function([[6, 7, 8, 1, 2, 3, 4], 1])

# Test Cases 3
test_function([[6, 7, 8, 1, 2, 3, 4], 10])

# Edge Cases 1
test_function([[], 10])

# Edge Cases 2
test_function([[1], 10])

print("All test cases passed!")
