# Problems vs. Algorithms

## Data Structure Questions

For this project, you will answer the seven questions laid out in the next sections. The questions cover a variety of topics related to the basic algorithms you've learned in this course. You will write up a clean and efficient answer in Python, as well as a text explanation of the efficiency of your code and your design choices.

## Problem 1: Square Root of an Integer

Find the square root of the integer without using any Python library. You have to find the floor value of the square root.

For example if the given number is 16, then the answer would be 4.

If the given number is 27, the answer would be 5 because sqrt(5) = 5.196 whose floor value is 5.

The expected time complexity is O(log(n))

Code in `problem_1.py` and explanation in `explanation_problem_1.md`

## Problem 2: Search in a Rotated Sorted Array

You are given a sorted array which is rotated at some random pivot point.

Example: [0, 1, 2, 4, 5, 6, 7] might become [4, 5, 6, 7, 0, 1, 2]

You are given a target value to search. If found in the array return its index, otherwise return -1.

You can assume there are no duplicates in the array and your algorithm's runtime complexity must be in the order of O(log n).

Example:

Input: nums = [4, 5, 6, 7, 0, 1, 2], target = 0, Output: 4

Code in `problem_2.py` and explanation in `explanation_problem_2.md`

## Problem 3: Rearrange Array Digits

Rearrange Array Elements so as to form two number such that their sum is maximum. Return these two numbers. You can assume that all array elements are in the range [0, 9]. The number of digits in both the numbers cannot differ by more than 1. You're not allowed to use any sorting function that Python provides and the expected time complexity is O(nlog(n)).

For example, the input [1, 2, 3, 4, 5] will return 531, 42.

Code in `problem_3.py` and explanation in `explanation_problem_3.md`

## Problem 4: Sort 0, 1, 2

Given an input array consisting on only 0, 1, and 2, sort the array in a single traversal. You're not allowed to use any sorting function that Python provides.

Note: O(n) does not necessarily mean single-traversal. For e.g. if you traverse the array twice, that would still be an O(n) solution but it will not count as single traversal.

Code in `problem_4.py` and explanation in `explanation_problem_4.md`

## Problem 5: Autocomplete with Tries

We've learned about Tries earlier in this course, its time to implement one. Implement a trie with insert, search, and startsWith methods.

Code in `problem_5.py` and explanation in `explanation_problem_5.md`

## Problem 6: Unsorted Integer Array

In this problem, we will look for smallest and largest integer from a list of unsorted integers. The code should run in O(n) time. Do not use Python's inbuilt functions to find min and max.

Code in `problem_6.py` and explanation in `explanation_problem_6.md`

## Problem 7: Request Routing in a Web Server with a Trie

For this exercise we are going to implement an HTTPRouter like you would find in a typical web server using the Trie data structure we learned previously.

There are many different implementations of HTTP Routers such as regular expressions or simple string matching, but the Trie is an excellent and very efficient data structure for this purpose.

The purpose of an HTTP Router is to take a URL path like "/", "/about", or "/blog/2019-01-15/my-awesome-post" and figure out what content to return. In a dynamic web server, the content will often come from a block of code called a handler.

Code in `problem_7.py` and explanation in `explanation_problem_7.md`
