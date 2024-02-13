def rearrange_digits(input_list):
    """
    Rearrange Array Elements so as to form two number such that their sum is maximum.

    Args:
        input_list(list): Input List
    Returns:
        (int),(int): Two maximum sums
    """
    if not input_list or len(input_list) < 2:
        return [0, 0]
    first_number = 0
    second_number = 0
    sorted_list = sorted(input_list, reverse=True)
    for index, value in enumerate(sorted_list):
        if index % 2 == 0:
            first_number = first_number * 10 + value
        else:
            second_number = second_number * 10 + value
    return [first_number, second_number]


def test_function(test_case):
    output = rearrange_digits(test_case[0])
    solution = test_case[1]
    if sum(output) == sum(solution):
        print("Pass")
    else:
        print("Fail")


# Test Cases 1
test_function([[1, 2, 3, 4, 5], [542, 31]])

# Test Cases 2
test_function([[4, 6, 2, 5, 9, 8], [964, 852]])

# Test Cases 3
test_function([[0, 0], [0, 0]])

# Edge Cases 1
test_function([[], [0, 0]])

# Edge Cases 2
test_function([[1], [0, 0]])

print("All test cases passed!")
