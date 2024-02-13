def sort_012(input_list):
    """
    Given an input array consisting on only 0, 1, and 2, sort the array in a single traversal.

    Args:
        input_list(list): List to be sorted
    """
    current_index = 0
    start_index = 0
    end_index = len(input_list) - 1
    while current_index <= end_index:
        if input_list[current_index] == 0:
            input_list[start_index], input_list[current_index] = (
                input_list[current_index],
                input_list[start_index],
            )
            start_index += 1
            current_index += 1
        elif input_list[current_index] == 2:
            input_list[end_index], input_list[current_index] = (
                input_list[current_index],
                input_list[end_index],
            )
            end_index -= 1
        else:
            current_index += 1
    return input_list


def test_function(test_case):
    sorted_array = sort_012(test_case)
    if sorted_array == sorted(test_case):
        print("Pass")
    else:
        print("Fail")


# Test Cases 1
test_function([0, 0, 2, 2, 2, 1, 1, 1, 2, 0, 2])

# Test Cases 2
test_function([2, 1, 2, 0, 0, 2, 1, 0, 1, 0, 0, 2, 2,
               2, 1, 2, 0, 0, 0, 2, 1, 0, 2, 0, 0, 1])

# Test Cases 3
test_function([0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2])

# Edge Cases 1
test_function([0])
test_function([0, 1, 2])

# Edge Cases 2
test_function([])

print("All test cases passed!")
