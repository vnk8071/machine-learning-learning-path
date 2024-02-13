"""
Course: Data Structures & Algorithms
Core: Data Structures
Problem: 4
Code by: KhoiVN
Date: 05/01/2024
"""


class Group(object):
    def __init__(self, _name):
        self.name = _name
        self.groups = []
        self.users = []

    def add_group(self, group):
        self.groups.append(group)

    def add_user(self, user):
        self.users.append(user)

    def get_groups(self):
        return self.groups

    def get_users(self):
        return self.users

    def get_name(self):
        return self.name


parent = Group("parent")
child = Group("child")
sub_child = Group("subchild")

sub_child_user = "sub_child_user"
sub_child.add_user(sub_child_user)

child.add_group(sub_child)
parent.add_group(child)


def is_user_in_group(user, group):
    """
    Return True if user is in the group, False otherwise.

    Args:
        user(str): user name/id
        group(class:Group): group to check user membership against
    """
    if not isinstance(group, Group):
        return False
    if user in group.get_users():
        return True
    for sub_group in group.get_groups():
        if is_user_in_group(user, sub_group):
            return True
    return False


# Test Case 1
assert is_user_in_group(sub_child_user, parent), "Test Case 1 Failed"
assert is_user_in_group(sub_child_user, child), "Test Case 1 Failed"

# Test Case 2
assert is_user_in_group(None, parent) == False, "Test Case 2 Failed"
assert is_user_in_group("", parent) == False, "Test Case 2 Failed"

# Test Case 3
assert is_user_in_group("sub_child_user", parent), "Test Case 3 Failed"
assert is_user_in_group("sub_child_user", sub_child), "Test Case 3 Failed"

# Edge Case 1
assert is_user_in_group("sub_child_user", None) == False, "Edge Case 1 Failed"
assert is_user_in_group("sub_child_user", "") == False, "Edge Case 1 Failed"

# Edge Case 2
assert is_user_in_group("sub_child_user", parent), "Edge Case 2 Failed"

print("All test cases passed!")
