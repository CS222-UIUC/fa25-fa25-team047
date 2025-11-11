"""Script to populate the database with initial coding problems."""
from app import create_app
from models import db, Problem

def seed_problems():
    """Add initial problems to the database."""
    app = create_app('development')

    with app.app_context():
        # Clear existing problems (optional, for development)
        # Problem.query.delete()

        problems = [
            {
                'title': 'Two Sum',
                'description': '''Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.

You may assume that each input would have exactly one solution, and you may not use the same element twice.

You can return the answer in any order.

Example 1:
Input: nums = [2,7,11,15], target = 9
Output: [0,1]
Explanation: Because nums[0] + nums[1] == 9, we return [0, 1].

Example 2:
Input: nums = [3,2,4], target = 6
Output: [1,2]

Constraints:
- 2 <= nums.length <= 10^4
- -10^9 <= nums[i] <= 10^9
- -10^9 <= target <= 10^9
- Only one valid answer exists.''',
                'difficulty': 'easy',
                'topic': 'arrays',
                'function_signature': 'def two_sum(nums: List[int], target: int) -> List[int]:',
                'starter_code': '''def two_sum(nums, target):
    # Write your code here
    pass''',
                'sample_test_cases': [
                    {'input': {'nums': [2, 7, 11, 15], 'target': 9}, 'expected': [0, 1]},
                    {'input': {'nums': [3, 2, 4], 'target': 6}, 'expected': [1, 2]},
                    {'input': {'nums': [3, 3], 'target': 6}, 'expected': [0, 1]},
                ],
                'hidden_test_cases': [
                    {'input': {'nums': [1, 2, 3, 4, 5], 'target': 9}, 'expected': [3, 4]},
                    {'input': {'nums': [-1, -2, -3, -4, -5], 'target': -8}, 'expected': [2, 4]},
                ],
                'is_published': True
            },
            {
                'title': 'Valid Palindrome',
                'description': '''A phrase is a palindrome if, after converting all uppercase letters into lowercase letters and removing all non-alphanumeric characters, it reads the same forward and backward. Alphanumeric characters include letters and numbers.

Given a string s, return true if it is a palindrome, or false otherwise.

Example 1:
Input: s = "A man, a plan, a canal: Panama"
Output: true
Explanation: "amanaplanacanalpanama" is a palindrome.

Example 2:
Input: s = "race a car"
Output: false
Explanation: "raceacar" is not a palindrome.

Constraints:
- 1 <= s.length <= 2 * 10^5
- s consists only of printable ASCII characters.''',
                'difficulty': 'easy',
                'topic': 'strings',
                'function_signature': 'def is_palindrome(s: str) -> bool:',
                'starter_code': '''def is_palindrome(s):
    # Write your code here
    pass''',
                'sample_test_cases': [
                    {'input': {'s': 'A man, a plan, a canal: Panama'}, 'expected': True},
                    {'input': {'s': 'race a car'}, 'expected': False},
                    {'input': {'s': ' '}, 'expected': True},
                ],
                'hidden_test_cases': [
                    {'input': {'s': '0P'}, 'expected': False},
                    {'input': {'s': 'ab_a'}, 'expected': True},
                ],
                'is_published': True
            },
            {
                'title': 'Binary Tree Inorder Traversal',
                'description': '''Given the root of a binary tree, return the inorder traversal of its nodes' values.

Example 1:
Input: root = [1,null,2,3]
Output: [1,3,2]

Example 2:
Input: root = []
Output: []

Example 3:
Input: root = [1]
Output: [1]

Constraints:
- The number of nodes in the tree is in the range [0, 100].
- -100 <= Node.val <= 100

Follow up: Recursive solution is trivial, could you do it iteratively?''',
                'difficulty': 'easy',
                'topic': 'trees',
                'function_signature': 'def inorder_traversal(root: Optional[TreeNode]) -> List[int]:',
                'starter_code': '''# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right

def inorder_traversal(root):
    # Write your code here
    pass''',
                'sample_test_cases': [
                    {'input': {'root': [1, None, 2, 3]}, 'expected': [1, 3, 2]},
                    {'input': {'root': []}, 'expected': []},
                    {'input': {'root': [1]}, 'expected': [1]},
                ],
                'hidden_test_cases': [
                    {'input': {'root': [1, 2, 3, 4, 5]}, 'expected': [4, 2, 5, 1, 3]},
                ],
                'is_published': True
            },
            {
                'title': 'Maximum Subarray',
                'description': '''Given an integer array nums, find the subarray with the largest sum, and return its sum.

Example 1:
Input: nums = [-2,1,-3,4,-1,2,1,-5,4]
Output: 6
Explanation: The subarray [4,-1,2,1] has the largest sum 6.

Example 2:
Input: nums = [1]
Output: 1
Explanation: The subarray [1] has the largest sum 1.

Example 3:
Input: nums = [5,4,-1,7,8]
Output: 23
Explanation: The subarray [5,4,-1,7,8] has the largest sum 23.

Constraints:
- 1 <= nums.length <= 10^5
- -10^4 <= nums[i] <= 10^4

Follow up: If you have figured out the O(n) solution, try coding another solution using the divide and conquer approach.''',
                'difficulty': 'medium',
                'topic': 'dynamic programming',
                'function_signature': 'def max_subarray(nums: List[int]) -> int:',
                'starter_code': '''def max_subarray(nums):
    # Write your code here
    pass''',
                'sample_test_cases': [
                    {'input': {'nums': [-2, 1, -3, 4, -1, 2, 1, -5, 4]}, 'expected': 6},
                    {'input': {'nums': [1]}, 'expected': 1},
                    {'input': {'nums': [5, 4, -1, 7, 8]}, 'expected': 23},
                ],
                'hidden_test_cases': [
                    {'input': {'nums': [-1, -2, -3]}, 'expected': -1},
                    {'input': {'nums': [8, -19, 5, -4, 20]}, 'expected': 21},
                ],
                'is_published': True
            },
            {
                'title': 'Longest Common Subsequence',
                'description': '''Given two strings text1 and text2, return the length of their longest common subsequence. If there is no common subsequence, return 0.

A subsequence of a string is a new string generated from the original string with some characters (can be none) deleted without changing the relative order of the remaining characters.

For example, "ace" is a subsequence of "abcde".
A common subsequence of two strings is a subsequence that is common to both strings.

Example 1:
Input: text1 = "abcde", text2 = "ace"
Output: 3
Explanation: The longest common subsequence is "ace" and its length is 3.

Example 2:
Input: text1 = "abc", text2 = "abc"
Output: 3
Explanation: The longest common subsequence is "abc" and its length is 3.

Example 3:
Input: text1 = "abc", text2 = "def"
Output: 0
Explanation: There is no such common subsequence, so the result is 0.

Constraints:
- 1 <= text1.length, text2.length <= 1000
- text1 and text2 consist of only lowercase English characters.''',
                'difficulty': 'medium',
                'topic': 'dynamic programming',
                'function_signature': 'def longest_common_subsequence(text1: str, text2: str) -> int:',
                'starter_code': '''def longest_common_subsequence(text1, text2):
    # Write your code here
    pass''',
                'sample_test_cases': [
                    {'input': {'text1': 'abcde', 'text2': 'ace'}, 'expected': 3},
                    {'input': {'text1': 'abc', 'text2': 'abc'}, 'expected': 3},
                    {'input': {'text1': 'abc', 'text2': 'def'}, 'expected': 0},
                ],
                'hidden_test_cases': [
                    {'input': {'text1': 'ezupkr', 'text2': 'ubmrapg'}, 'expected': 2},
                    {'input': {'text1': 'oxcpqrsvwf', 'text2': 'shmtulqrypy'}, 'expected': 2},
                ],
                'is_published': True
            },
            {
                'title': 'Binary Search',
                'description': '''Given an array of integers nums which is sorted in ascending order, and an integer target, write a function to search target in nums. If target exists, then return its index. Otherwise, return -1.

You must write an algorithm with O(log n) runtime complexity.

Example 1:
Input: nums = [-1,0,3,5,9,12], target = 9
Output: 4
Explanation: 9 exists in nums and its index is 4

Example 2:
Input: nums = [-1,0,3,5,9,12], target = 2
Output: -1
Explanation: 2 does not exist in nums so return -1

Constraints:
- 1 <= nums.length <= 10^4
- -10^4 < nums[i], target < 10^4
- All the integers in nums are unique.
- nums is sorted in ascending order.''',
                'difficulty': 'easy',
                'topic': 'binary search',
                'function_signature': 'def search(nums: List[int], target: int) -> int:',
                'starter_code': '''def search(nums, target):
    # Write your code here
    pass''',
                'sample_test_cases': [
                    {'input': {'nums': [-1, 0, 3, 5, 9, 12], 'target': 9}, 'expected': 4},
                    {'input': {'nums': [-1, 0, 3, 5, 9, 12], 'target': 2}, 'expected': -1},
                ],
                'hidden_test_cases': [
                    {'input': {'nums': [5], 'target': 5}, 'expected': 0},
                    {'input': {'nums': [2, 5], 'target': 5}, 'expected': 1},
                ],
                'is_published': True
            },
        ]

        # Add problems to database
        for prob_data in problems:
            # Check if problem already exists
            existing = Problem.query.filter_by(title=prob_data['title']).first()
            if not existing:
                problem = Problem(**prob_data)
                db.session.add(problem)
                print(f"Added problem: {prob_data['title']}")
            else:
                print(f"Problem already exists: {prob_data['title']}")

        db.session.commit()
        print(f"\nSuccessfully seeded {len(problems)} problems!")

if __name__ == '__main__':
    seed_problems()
