"""
Course: Data Structures & Algorithms
Core: Data Structures
Problem: 2
Code by: KhoiVN
Date: 04/01/2024
"""

import os


def find_files(suffix, path):
    """
    Find all files beneath path with file name suffix.

    Note that a path may contain further subdirectories
    and those subdirectories may also contain further subdirectories.

    There are no limit to the depth of the subdirectories can be.

    Args:
        suffix(str): suffix if the file name to be found
        path(str): path of the file system

    Returns:
        suffix_path_list(list): a list of paths
    """
    suffix_path_list = []

    if not os.path.isdir(path):
        return suffix_path_list

    list_walk_directory = list(os.walk(path))

    for directory in list_walk_directory:
        for file in directory[2]:
            if file.endswith(suffix):
                suffix_path_list.append(os.path.join(directory[0], file))
    return suffix_path_list


# Test Case 1
test_case_1 = find_files(".c", "./testdir")
assert sorted(test_case_1) == sorted(
    [
        "./testdir/subdir1/a.c",
        "./testdir/subdir3/subsubdir1/b.c",
        "./testdir/t1.c",
        "./testdir/subdir5/a.c",
    ]
), f"Test Case 1 Failed, expected {test_case_1}"

# Test Case 2
test_case_2 = find_files(".c", "./testdir/subdir1")
assert sorted(test_case_2) == sorted(
    ["./testdir/subdir1/a.c"]
), f"Test Case 2 Failed, expected {test_case_2}"

# Test Case 3
test_case_3 = find_files(".c", "./testdir/subdir3/subsubdir1")
assert sorted(test_case_3) == sorted(
    ["./testdir/subdir3/subsubdir1/b.c"]
), f"Test Case 3 Failed, expected {test_case_3}"

# Edge Case 1
edge_case_1 = find_files(".", "./testdir/subdir5")
assert sorted(edge_case_1) == [], f"Edge Case 1 Failed, expected {edge_case_1}"

# Edge Case 2
edge_case_2 = find_files("c", "./testdir/s")
assert sorted(edge_case_2) == [], f"Edge Case 2 Failed, expected {edge_case_2}"

print("All test cases passed!")
