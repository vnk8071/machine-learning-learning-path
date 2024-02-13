import random


def get_min_max(ints):
    """
    Return a tuple(min, max) out of list of unsorted integers.

    Args:
        ints(list): list of integers containing one or more integers
    """
    if not ints or len(ints) < 2:
        return None
    min_value = ints[0]
    max_value = ints[0]
    for value in ints:
        if value < min_value:
            min_value = value
        if value > max_value:
            max_value = value
    return min_value, max_value


# Example Test Case of Ten Integers

l = [i for i in range(0, 10)]  # a list containing 0 - 9
random.shuffle(l)

# Test Cases 1
print("Pass" if ((0, 9) == get_min_max(l)) else "Fail")

# Test Cases 2
print("Pass" if ((0, 0) == get_min_max([0, 0])) else "Fail")

# Test Cases 3
print("Pass" if ((3, 7) == get_min_max([3, 7])) else "Fail")

# Edge Cases 1
print("Pass" if (None is get_min_max([])) else "Fail")

# Edge Cases 2
print("Pass" if (None is get_min_max(None)) else "Fail")

print("All test cases passed!")
