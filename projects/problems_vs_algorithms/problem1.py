def sqrt(number):
    """
    Calculate the floored square root of a number

    Args:
        number(int): Number to find the floored squared root
    Returns:
        int: Floored Square Root
    """
    if number < 0:
        return None
    if number == 0 or number == 1:
        return number
    start = 1
    end = number
    while start <= end:
        middle = (start + end) // 2
        if middle * middle == number:
            return middle
        elif middle * middle < number:
            start = middle + 1
            result = middle
        else:
            end = middle - 1
    return result


# Test Cases 1
assert 3 == sqrt(9), "Test Case 1 Failed, expected 3"
assert 4 == sqrt(16), "Test Case 3 Failed, expected 4"

# Test Cases 2
assert 0 == sqrt(0), "Test Case 2 Failed, expected 0"
assert 1 == sqrt(1), "Test Case 4 Failed, expected 1"

# Test Cases 3
assert 5 == sqrt(27), "Test Case 5 Failed, expected 5"
assert 5 == sqrt(30), "Test Case 6 Failed, expected 5"

# Edge Cases 1
assert 100 == sqrt(10003), "Test Case 7 Failed, expected 100"

# Edge Cases 2
assert None is sqrt(-1), "Test Case 8 Failed, expected None"

print("All test cases passed!")
