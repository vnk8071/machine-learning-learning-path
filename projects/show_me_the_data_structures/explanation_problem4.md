# Group that represents a group of users

Time Complexity: The time complexity of the is_user_in_group(user, group) function is O(n), where n is the total number of users and groups. This is because in the worst-case scenario, the function needs to check each user in each group and subgroup. The function uses recursion to traverse all groups and subgroups.

Space Complexity: The space complexity of the is_user_in_group(user, group) function is also O(n), where n is the total number of groups. This is because in the worst-case scenario, the function will have to recurse through each group and subgroup, which will add to the call stack. The depth of the recursion equals the depth of the group hierarchy, which in the worst case can be as large as the number of groups.
