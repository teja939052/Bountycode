"""LeetCode metadata overlay — Part 1: Arrays, Hashing, Two Pointers, Sliding Window.

Each key is a curated question slug from the seed files. The overlay enriches the
final store entry with a full LeetCode statement, constraints, expected complexity,
follow-up and per-example explanations so the problem page renders like LeetCode.
"""

LEETCODE_META = {
    "nc-two-sum": {
        "leetcode_number": 1,
        "statement": "Given an array of integers `nums` and an integer `target`, return indices of the two numbers such that they add up to `target`.\n\nYou may assume that each input would have exactly one solution, and you may not use the same element twice.\n\nYou can return the answer in any order.",
        "constraints": [
            "2 <= nums.length <= 10^4",
            "-10^9 <= nums[i] <= 10^9",
            "-10^9 <= target <= 10^9",
            "Only one valid answer exists.",
        ],
        "follow_up": "Can you come up with an algorithm that is less than O(n^2) time complexity?",
        "expected_time_complexity": "O(n)",
        "expected_space_complexity": "O(n)",
        "example_explanations": {
            0: "nums[0] + nums[1] == 9, so we return [0, 1].",
            1: "nums[1] + nums[2] == 6, so we return [1, 2].",
        },
    },
    "nc-contains-duplicate": {
        "leetcode_number": 217,
        "statement": "Given an integer array `nums`, return `true` if any value appears at least twice in the array, and return `false` if every element is distinct.",
        "constraints": [
            "1 <= nums.length <= 10^5",
            "-10^9 <= nums[i] <= 10^9",
        ],
        "expected_time_complexity": "O(n)",
        "expected_space_complexity": "O(n)",
        "example_explanations": {
            0: "The value 1 appears twice, so the answer is true.",
        },
    },
    "nc-valid-anagram": {
        "leetcode_number": 242,
        "statement": "Given two strings `s` and `t`, return `true` if `t` is an anagram of `s`, and `false` otherwise.\n\nAn Anagram is a word or phrase formed by rearranging the letters of a different word or phrase, typically using all the original letters exactly once.",
        "constraints": [
            "1 <= s.length, t.length <= 5 * 10^4",
            "s and t consist of lowercase English letters.",
        ],
        "follow_up": "What if the inputs contain Unicode characters? How would you adapt your solution to such a case?",
        "expected_time_complexity": "O(s + t)",
        "expected_space_complexity": "O(s)",
        "example_explanations": {
            0: "nagaram rearranges to anagram, so the answer is true.",
            1: "rat cannot be rearranged to form car, so the answer is false.",
        },
    },
    "nc-group-anagrams": {
        "leetcode_number": 49,
        "statement": "Given an array of strings `strs`, group the anagrams together. You can return the answer in any order.\n\nAn Anagram is a word or phrase formed by rearranging the letters of a different word or phrase, typically using all the original letters exactly once.",
        "constraints": [
            "1 <= strs.length <= 10^4",
            "0 <= strs[i].length <= 100",
            "strs[i] consists of lowercase English letters.",
        ],
        "expected_time_complexity": "O(n * k) where n = len(strs) and k = max length of a string",
        "expected_space_complexity": "O(n * k)",
        "example_explanations": {
            0: "eat, tea and ate are anagrams of each other, as are tan and nat; bat stands alone.",
        },
    },
    "nc-top-k-frequent-elements": {
        "leetcode_number": 347,
        "statement": "Given an integer array `nums` and an integer `k`, return the `k` most frequent elements. You may return the answer in any order.",
        "constraints": [
            "1 <= nums.length <= 10^5",
            "-10^4 <= nums[i] <= 10^4",
            "k is in the range [1, the number of unique elements in the array].",
            "It is guaranteed that the answer is unique.",
        ],
        "follow_up": "Your algorithm's time complexity must be better than O(n log n), where n is the array's size.",
        "expected_time_complexity": "O(n)",
        "expected_space_complexity": "O(n)",
        "example_explanations": {
            0: "1 appears three times, 2 appears twice, and 3 appears once. The top two are [1, 2].",
            1: "1 appears once; only one element is requested.",
        },
    },
    "nc-product-array-except-self": {
        "leetcode_number": 238,
        "statement": "Given an integer array `nums`, return an array `answer` such that `answer[i]` is equal to the product of all the elements of `nums` except `nums[i]`.\n\nThe product of any prefix or suffix of `nums` is guaranteed to fit in a 32-bit integer.\n\nYou must write an algorithm that runs in O(n) time and without using the division operation.",
        "constraints": [
            "2 <= nums.length <= 10^5",
            "-30 <= nums[i] <= 30",
            "The product of any prefix or suffix of nums is guaranteed to fit in a 32-bit integer.",
        ],
        "follow_up": "Can you solve the problem in O(1) extra space complexity? (The output array does not count as extra space for space complexity analysis.)",
        "expected_time_complexity": "O(n)",
        "expected_space_complexity": "O(1) excluding the output array",
        "example_explanations": {
            0: "answer[0] = 1*2*3*4 = 24, answer[1] = 1*2*3*4 = 12, and so on.",
        },
    },
    "nc-encode-decode-strings": {
        "leetcode_number": 271,
        "statement": "Design an algorithm to encode a list of strings to a string. The encoded string is then sent over the network and decoded back to the original list of strings.\n\nPlease implement `encode` and `decode`.",
        "constraints": [
            "1 <= strs.length <= 200",
            "0 <= strs[i].length <= 200",
            "strs[i] contains any possible characters out of 256 valid ASCII characters.",
        ],
        "expected_time_complexity": "O(total characters)",
        "expected_space_complexity": "O(total characters)",
        "example_explanations": {
            0: "The two strings are length-prefixed and packed into one string; decoding reverses the process.",
        },
    },
    "nc-longest-consecutive-sequence": {
        "leetcode_number": 128,
        "statement": "Given an unsorted array of integers `nums`, return the length of the longest consecutive elements sequence.\n\nYou must write an algorithm that runs in O(n) time.",
        "constraints": [
            "0 <= nums.length <= 10^5",
            "-10^9 <= nums[i] <= 10^9",
        ],
        "expected_time_complexity": "O(n)",
        "expected_space_complexity": "O(n)",
        "example_explanations": {
            0: "The longest consecutive sequence is [1, 2, 3, 4], of length 4.",
        },
    },
    "nc-valid-sudoku": {
        "leetcode_number": 36,
        "statement": "Determine if a `9 x 9` Sudoku board is valid. Only the filled cells need to be validated according to the following rules:\n\n1. Each row must contain the digits 1-9 without repetition.\n2. Each column must contain the digits 1-9 without repetition.\n3. Each of the nine `3 x 3` sub-boxes of the grid must contain the digits 1-9 without repetition.\n\nNote:\n- A Sudoku board (partially filled) could be valid but is not necessarily solvable.\n- Only the filled cells need to be validated according to the mentioned rules.",
        "constraints": [
            "board.length == 9",
            "board[i].length == 9",
            "board[i][j] is a digit 1-9 or '.'.",
        ],
        "expected_time_complexity": "O(9 x 9)",
        "expected_space_complexity": "O(9 x 9)",
        "example_explanations": {
            0: "Every row, column, and 3x3 box is free of repeated digits.",
            1: "The digit 8 repeats in the first 3x3 box, so the board is invalid.",
        },
    },
    "nc-find-duplicate-number": {
        "leetcode_number": 287,
        "statement": "Given an array of integers `nums` containing `n + 1` integers where each integer is in the range `[1, n]` inclusive.\n\nThere is only one repeated number in `nums`, return this repeated number.\n\nYou must solve the problem without modifying the array `nums` and uses only constant extra space.",
        "constraints": [
            "1 <= n <= 10^5",
            "nums.length == n + 1",
            "1 <= nums[i] <= n",
            "All the integers in nums appear only once except for precisely one integer which appears two or more times.",
        ],
        "follow_up": "How can we prove that at least one duplicate number must exist in nums? Can you solve the problem in linear runtime complexity?",
        "expected_time_complexity": "O(n)",
        "expected_space_complexity": "O(1)",
        "example_explanations": {
            0: "2 appears twice, so it is the repeated number.",
        },
    },
    "nc-missing-number": {
        "leetcode_number": 268,
        "statement": "Given an array `nums` containing `n` distinct numbers in the range `[0, n]`, return the only number in the range that is missing from the array.",
        "constraints": [
            "n == nums.length",
            "1 <= n <= 10^4",
            "0 <= nums[i] <= n",
            "All the numbers of nums are unique.",
        ],
        "follow_up": "Could you implement a solution using only O(1) extra space complexity and O(n) runtime complexity?",
        "expected_time_complexity": "O(n)",
        "expected_space_complexity": "O(1)",
        "example_explanations": {
            0: "8 is the missing number in the range [0, 9].",
            1: "2 is the missing number.",
        },
    },
    "nc-single-number": {
        "leetcode_number": 136,
        "statement": "Given a non-empty array of integers `nums`, every element appears twice except for one. Find that single one.\n\nYou must implement a solution with a linear runtime complexity and use only constant extra space.",
        "constraints": [
            "1 <= nums.length <= 3 * 10^4",
            "-3 * 10^4 <= nums[i] <= 3 * 10^4",
            "Each element in the array appears twice except for one element which appears exactly once.",
        ],
        "expected_time_complexity": "O(n)",
        "expected_space_complexity": "O(1)",
        "example_explanations": {
            0: "4 appears exactly once; every other element appears twice.",
        },
    },
    "nc-palindrome-number": {
        "leetcode_number": 9,
        "statement": "Given an integer `x`, return `true` if `x` is a palindrome, and `false` otherwise.",
        "constraints": [
            "-2^31 <= x <= 2^31 - 1",
        ],
        "follow_up": "Could you solve it without converting the integer to a string?",
        "expected_time_complexity": "O(log x)",
        "expected_space_complexity": "O(1)",
        "example_explanations": {
            0: "121 reads as 121 from left to right and from right to left.",
            1: "From left to right, it reads -121. From right to left, it becomes 121-. Therefore it is not a palindrome.",
            2: "From left to right, it reads 10. From right to left, it becomes 01. Therefore it is not a palindrome.",
        },
    },
    "nc-plus-one": {
        "leetcode_number": 66,
        "statement": "You are given a large integer represented as an integer array `digits`, where each `digits[i]` is the `i-th` digit of the integer. The digits are ordered from most significant to least significant in left-to-right order. The large integer does not contain any leading 0's.\n\nIncrement the large integer by one and return the resulting array of digits.",
        "constraints": [
            "1 <= digits.length <= 100",
            "0 <= digits[i] <= 9",
            "digits does not contain any leading 0's.",
        ],
        "expected_time_complexity": "O(n)",
        "expected_space_complexity": "O(1)",
        "example_explanations": {
            0: "The array represents the integer 4321. Incrementing by one gives 4322.",
        },
    },
    "nc-multiply-strings": {
        "leetcode_number": 43,
        "statement": "Given two non-negative integers `num1` and `num2` represented as strings, return the product of `num1` and `num2`, also represented as a string.\n\nNote: You must not use any built-in BigInteger library or convert the inputs to integer directly.",
        "constraints": [
            "1 <= num1.length, num2.length <= 200",
            "num1 and num2 consist of digits only.",
            "Both num1 and num2 do not contain any leading zero, except the number 0 itself.",
        ],
        "expected_time_complexity": "O(n * m)",
        "expected_space_complexity": "O(n + m)",
        "example_explanations": {
            0: "123 * 456 = 56088.",
        },
    },
    "nc-best-time-buy-sell-stock": {
        "leetcode_number": 121,
        "statement": "You are given an array `prices` where `prices[i]` is the price of a given stock on the `i-th` day.\n\nYou want to maximize your profit by choosing a single day to buy one stock and choosing a different day in the future to sell that stock.\n\nReturn the maximum profit you can achieve from this transaction. If you cannot achieve any profit, return `0`.",
        "constraints": [
            "1 <= prices.length <= 10^5",
            "0 <= prices[i] <= 10^4",
        ],
        "expected_time_complexity": "O(n)",
        "expected_space_complexity": "O(1)",
        "example_explanations": {
            0: "Buy on day 2 (price 1) and sell on day 5 (price 6), profit = 6 - 1 = 5.",
            1: "Prices only decrease, so no profitable transaction exists.",
        },
    },
    "nc-rotate-image": {
        "leetcode_number": 48,
        "statement": "You are given an `n x n` 2D `matrix` representing an image, rotate the image by 90 degrees (clockwise).\n\nYou have to rotate the image in-place, which means you have to modify the input 2D matrix directly. Do NOT allocate another 2D matrix and do the rotation.",
        "constraints": [
            "n == matrix.length == matrix[i].length",
            "1 <= n <= 20",
            "-1000 <= matrix[i][j] <= 1000",
        ],
        "expected_time_complexity": "O(n^2)",
        "expected_space_complexity": "O(1)",
        "example_explanations": {
            0: "The matrix is rotated clockwise by 90 degrees.",
        },
    },
    "nc-spiral-matrix": {
        "leetcode_number": 54,
        "statement": "Given an `m x n` `matrix`, return all elements of the `matrix` in spiral order.",
        "constraints": [
            "m == matrix.length",
            "n == matrix[i].length",
            "1 <= m, n <= 10",
            "-100 <= matrix[i][j] <= 100",
        ],
        "expected_time_complexity": "O(m * n)",
        "expected_space_complexity": "O(m * n) for the output",
        "example_explanations": {
            0: "The elements are visited in a clockwise spiral.",
        },
    },
    "nc-set-matrix-zeroes": {
        "leetcode_number": 73,
        "statement": "Given an `m x n` integer matrix `matrix`, if an element is `0`, set its entire row and column to `0`'s.\n\nYou must do it in place.",
        "constraints": [
            "m == matrix.length",
            "n == matrix[0].length",
            "1 <= m, n <= 200",
            "-2^31 <= matrix[i][j] <= 2^31 - 1",
        ],
        "follow_up": "A straightforward solution using O(mn) space is probably not a good idea. A simple improvement uses O(m + n) space, but still not the best solution. Could you devise a constant space solution?",
        "expected_time_complexity": "O(m * n)",
        "expected_space_complexity": "O(1)",
        "example_explanations": {
            0: "The zero in the middle zeros out its entire row and column.",
        },
    },
    "nc-valid-palindrome": {
        "leetcode_number": 125,
        "statement": "A phrase is a palindrome if, after converting all uppercase letters into lowercase letters and removing all non-alphanumeric characters, it reads the same forward and backward. Alphanumeric characters include letters and numbers.\n\nGiven a string `s`, return `true` if it is a palindrome, or `false` otherwise.",
        "constraints": [
            "1 <= s.length <= 2 * 10^5",
            "s consists only of printable ASCII characters.",
        ],
        "expected_time_complexity": "O(n)",
        "expected_space_complexity": "O(1)",
        "example_explanations": {
            0: "After removing non-alphanumeric characters and lowercasing, the string reads 'amanaplanacanalpanama', which is a palindrome.",
            1: "After cleanup the string reads 'raceacar', which is not a palindrome.",
        },
    },
    "nc-two-sum-ii": {
        "leetcode_number": 167,
        "statement": "Given a 1-indexed array of integers `numbers` that is already sorted in non-decreasing order, find two numbers such that they add up to a specific `target` number. Let these two numbers be `numbers[index1]` and `numbers[index2]` where `1 <= index1 < index2 <= numbers.length`.\n\nReturn the indices of the two numbers, `index1` and `index2`, added by one as an integer array `[index1, index2]` of length 2.\n\nThe tests are generated such that there is exactly one solution. You may not use the same element twice.\n\nYour solution must use only constant extra space.",
        "constraints": [
            "2 <= numbers.length <= 3 * 10^4",
            "-1000 <= numbers[i] <= 1000",
            "numbers is sorted in non-decreasing order.",
            "-1000 <= target <= 1000",
            "The tests are generated such that there is exactly one solution.",
        ],
        "expected_time_complexity": "O(n)",
        "expected_space_complexity": "O(1)",
        "example_explanations": {
            0: "The sum of 2 and 7 is 9. Their 1-indexed positions are [1, 2].",
        },
    },
    "nc-3sum": {
        "leetcode_number": 15,
        "statement": "Given an integer array nums, return all the triplets `[nums[i], nums[j], nums[k]]` such that `i != j`, `i != k`, and `j != k`, and `nums[i] + nums[j] + nums[k] == 0`.\n\nNotice that the solution set must not contain duplicate triplets.",
        "constraints": [
            "3 <= nums.length <= 3000",
            "-10^5 <= nums[i] <= 10^5",
        ],
        "expected_time_complexity": "O(n^2)",
        "expected_space_complexity": "O(n)",
        "example_explanations": {
            0: "The only distinct triplets summing to zero are [-1, -1, 2] and [-1, 0, 1].",
        },
    },
    "nc-container-with-most-water": {
        "leetcode_number": 11,
        "statement": "You are given an integer array `height` of length `n`. There are `n` vertical lines drawn such that the two endpoints of the `i-th` line are `(i, 0)` and `(i, height[i])`.\n\nFind two lines that together with the x-axis form a container, such that the container contains the most water.\n\nReturn the maximum amount of water a container can store.\n\nNotice that you may not slant the container.",
        "constraints": [
            "n == height.length",
            "2 <= n <= 10^5",
            "0 <= height[i] <= 10^4",
        ],
        "expected_time_complexity": "O(n)",
        "expected_space_complexity": "O(1)",
        "example_explanations": {
            0: "The lines at indices 1 and 6 bound a container of height 7 and width 5, holding 35 units of water.",
        },
    },
    "nc-trapping-rain-water": {
        "leetcode_number": 42,
        "statement": "Given `n` non-negative integers representing an elevation map where the width of each bar is `1`, compute how much water it can trap after raining.",
        "constraints": [
            "n == height.length",
            "1 <= n <= 2 * 10^4",
            "0 <= height[i] <= 10^5",
        ],
        "expected_time_complexity": "O(n)",
        "expected_space_complexity": "O(1)",
        "example_explanations": {
            0: "The elevations trap 6 units of water in total.",
        },
    },
    "nc-longest-substring-no-repeat": {
        "leetcode_number": 3,
        "statement": "Given a string `s`, find the length of the longest substring without repeating characters.",
        "constraints": [
            "0 <= s.length <= 5 * 10^4",
            "s consists of English letters, digits, symbols and spaces.",
        ],
        "expected_time_complexity": "O(n)",
        "expected_space_complexity": "O(min(n, 128))",
        "example_explanations": {
            0: "The answer is 'abc', with the length of 3.",
            1: "The answer is 'b', with the length of 1.",
        },
    },
    "nc-longest-repeating-char-replacement": {
        "leetcode_number": 424,
        "statement": "You are given a string `s` and an integer `k`. You can choose any character of the string and change it to any other uppercase English character. You can perform this operation at most `k` times.\n\nReturn the length of the longest substring containing the same letter you can get after performing the above operations.",
        "constraints": [
            "1 <= s.length <= 10^5",
            "s consists of only uppercase English letters.",
            "0 <= k <= s.length",
        ],
        "expected_time_complexity": "O(n)",
        "expected_space_complexity": "O(26)",
        "example_explanations": {
            0: "Replace the two 'A's with two 'B's, or vice versa, to get 'BBBBBB' of length 6.",
        },
    },
    "nc-permutation-in-string": {
        "leetcode_number": 567,
        "statement": "Given two strings `s1` and `s2`, return `true` if `s2` contains a permutation of `s1`, or `false` otherwise.\n\nIn other words, return `true` if one of `s1`'s permutations is the substring of `s2`.",
        "constraints": [
            "1 <= s1.length, s2.length <= 10^4",
            "s1 and s2 consist of lowercase English letters.",
        ],
        "expected_time_complexity": "O(n)",
        "expected_space_complexity": "O(1)",
        "example_explanations": {
            0: "'ba' is a permutation of 'ab', and it appears as a substring of 'eidbaooo'.",
            1: "Neither permutation of 'ab' ('ab' or 'ba') appears as a substring of 'eidboaoo'.",
        },
    },
    "nc-minimum-window-substring": {
        "leetcode_number": 76,
        "statement": "Given two strings `s` and `t` of lengths `m` and `n` respectively, return the minimum window substring of `s` such that every character in `t` (including duplicates) is included in the window. If there is no such substring, return the empty string `\"\"`.\n\nThe testcases will be generated such that the answer is unique.",
        "constraints": [
            "m == s.length",
            "n == t.length",
            "1 <= m, n <= 10^5",
            "s and t consist of uppercase and lowercase English letters.",
        ],
        "follow_up": "Could you find an algorithm that runs in O(m + n) time?",
        "expected_time_complexity": "O(m + n)",
        "expected_space_complexity": "O(m + n)",
        "example_explanations": {
            0: "'BANC' is the minimum window covering all letters of 'ABC'.",
        },
    },
    "nc-minimum-size-subarray-sum": {
        "leetcode_number": 209,
        "statement": "Given an array of positive integers `nums` and a positive integer `target`, return the minimal length of a subarray whose sum is greater than or equal to `target`. If there is no such subarray, return `0` instead.",
        "constraints": [
            "1 <= target <= 10^9",
            "1 <= nums.length <= 10^5",
            "1 <= nums[i] <= 10^4",
        ],
        "follow_up": "If you have figured out the O(n) solution, try coding another solution of which the time complexity is O(n log(n)).",
        "expected_time_complexity": "O(n)",
        "expected_space_complexity": "O(1)",
        "example_explanations": {
            0: "The subarray [4, 3] has the minimum length under the problem constraint.",
        },
    },
    "nc-sliding-window-maximum": {
        "leetcode_number": 239,
        "statement": "You are given an array of integers `nums`, there is a sliding window of size `k` which is moving from the very left of the array to the very right. You can only see the `k` numbers in the window. Each time the sliding window moves right by one position.\n\nReturn the max sliding window.",
        "constraints": [
            "1 <= nums.length <= 10^5",
            "-10^4 <= nums[i] <= 10^4",
            "1 <= k <= nums.length",
        ],
        "expected_time_complexity": "O(n)",
        "expected_space_complexity": "O(k)",
        "example_explanations": {
            0: "The window slides across the array and the maximum of each window is [3, 3, 5, 5, 6, 7].",
        },
    },
    "nc-koko-eating-bananas": {
        "leetcode_number": 875,
        "statement": "Koko loves to eat bananas. There are `n` piles of bananas, the `i-th` pile has `piles[i]` bananas. The guards have gone and will come back in `h` hours.\n\nKoko can decide her bananas-per-hour eating speed of `k`. Each hour, she chooses some pile of bananas and eats `k` bananas from that pile. If the pile has less than `k` bananas, she eats all of them instead and will not eat any more bananas during this hour.\n\nKoko likes to eat slowly but still wants to finish eating all the bananas before the guards return.\n\nReturn the minimum integer `k` such that she can eat all the bananas within `h` hours.",
        "constraints": [
            "1 <= piles.length <= 10^4",
            "piles.length <= h <= 10^9",
            "1 <= piles[i] <= 10^9",
        ],
        "expected_time_complexity": "O(n log max(piles))",
        "expected_space_complexity": "O(1)",
        "example_explanations": {
            0: "At speed 4, Koko eats the piles in 3 + 2 + 2 + 2 = 9 hours, within the 8-hour limit.",
        },
    },
    "nc-binary-search": {
        "leetcode_number": 704,
        "statement": "Given an array of integers `nums` which is sorted in ascending order, and an integer `target`, write a function to search `target` in `nums`. If `target` exists, then return its index. Otherwise, return `-1`.\n\nYou must write an algorithm with `O(log n)` runtime complexity.",
        "constraints": [
            "1 <= nums.length <= 10^4",
            "-10^4 < nums[i], target < 10^4",
            "All the integers in nums are unique.",
            "nums is sorted in ascending order.",
        ],
        "expected_time_complexity": "O(log n)",
        "expected_space_complexity": "O(1)",
        "example_explanations": {
            0: "9 is at index 4.",
            1: "-1 is not present in the array.",
        },
    },
    "nc-search-2d-matrix": {
        "leetcode_number": 74,
        "statement": "You are given an `m x n` integer matrix `matrix` with the following two properties:\n\n- Each row is sorted in non-decreasing order.\n- The first integer of each row is greater than the last integer of the previous row.\n\nGiven an integer `target`, return `true` if `target` is in `matrix` or `false` otherwise.\n\nYou must write a solution in `O(log(m * n))` time complexity.",
        "constraints": [
            "m == matrix.length",
            "n == matrix[i].length",
            "1 <= m, n <= 100",
            "-10^4 <= matrix[i][j], target <= 10^4",
        ],
        "expected_time_complexity": "O(log(m * n))",
        "expected_space_complexity": "O(1)",
        "example_explanations": {
            0: "The target 3 is present in the matrix.",
        },
    },
    "nc-search-rotated-sorted-array": {
        "leetcode_number": 33,
        "statement": "There is an integer array `nums` sorted in ascending order (with distinct values).\n\nPrior to being passed to your function, `nums` is possibly rotated at an unknown pivot index `k` such that the resulting array is `[nums[k], nums[k+1], ..., nums[n-1], nums[0], nums[1], ..., nums[k-1]]` (0-indexed).\n\nGiven the array `nums` after the possible rotation and an integer `target`, return the index of `target` if it is in `nums`, or `-1` if it is not in `nums`.\n\nYou must write an algorithm with `O(log n)` runtime complexity.",
        "constraints": [
            "1 <= nums.length <= 5000",
            "-10^4 <= nums[i] <= 10^4",
            "All values of nums are unique.",
            "nums is an ascending array that is possibly rotated.",
            "-10^4 <= target <= 10^4",
        ],
        "expected_time_complexity": "O(log n)",
        "expected_space_complexity": "O(1)",
        "example_explanations": {
            0: "The target 0 is at index 4.",
        },
    },
    "nc-find-min-rotated-sorted-array": {
        "leetcode_number": 153,
        "statement": "Suppose an array of length `n` sorted in ascending order is rotated between `1` and `n` times. For example, the array `nums = [0,1,2,4,5,6,7]` might become:\n\n- `[4,5,6,7,0,1,2]` if it was rotated `4` times.\n- `[0,1,2,4,5,6,7]` if it was rotated `7` times.\n\nNotice that rotating an array `[a[0], a[1], a[2], ..., a[n-1]]` 1 time results in the array `[a[n-1], a[0], a[1], a[2], ..., a[n-2]]`.\n\nGiven the sorted rotated array `nums` of unique elements, return the minimum element of this array.\n\nYou must write an algorithm that runs in `O(log n)` time.",
        "constraints": [
            "n == nums.length",
            "1 <= n <= 5000",
            "-5000 <= nums[i] <= 5000",
            "All the integers of nums are unique.",
            "nums is sorted and rotated between 1 and n times.",
        ],
        "expected_time_complexity": "O(log n)",
        "expected_space_complexity": "O(1)",
        "example_explanations": {
            0: "The minimum element of [3,4,5,1,2] is 1.",
            1: "The minimum element of [4,5,6,7,0,1,2] is 0.",
        },
    },
    "nc-find-peak-element": {
        "leetcode_number": 162,
        "statement": "A peak element is an element that is strictly greater than its neighbors.\n\nGiven a 0-indexed integer array `nums`, find a peak element, and return its index. If the array contains multiple peaks, return the index to any of the peaks.\n\nYou may imagine that `nums[-1] = nums[n] = -infinity`. In other words, an element is always considered to be strictly greater than a neighbor that is outside the array.\n\nYou must write an algorithm that runs in `O(log n)` time.",
        "constraints": [
            "1 <= nums.length <= 1000",
            "-2^31 <= nums[i] <= 2^31 - 1",
            "nums[i] != nums[i + 1] for all valid i.",
        ],
        "expected_time_complexity": "O(log n)",
        "expected_space_complexity": "O(1)",
        "example_explanations": {
            0: "3 is a peak element, and your function should return the index number 2.",
        },
    },
    "nc-median-two-sorted-arrays": {
        "leetcode_number": 4,
        "statement": "Given two sorted arrays `nums1` and `nums2` of size `m` and `n` respectively, return the median of the two sorted arrays.\n\nThe overall run time complexity should be `O(log (m+n))`.",
        "constraints": [
            "nums1.length == m",
            "nums2.length == n",
            "0 <= m <= 1000",
            "0 <= n <= 1000",
            "1 <= m + n <= 2000",
            "-10^6 <= nums1[i], nums2[i] <= 10^6",
        ],
        "expected_time_complexity": "O(log(m + n))",
        "expected_space_complexity": "O(1)",
        "example_explanations": {
            0: "The merged array is [1, 2, 3], so the median is 2.",
            1: "The merged array is [1, 2, 3, 4], so the median is (2 + 3) / 2 = 2.5.",
        },
    },
    "nc-jump-game": {
        "leetcode_number": 55,
        "statement": "You are given an integer array `nums`. You are initially positioned at the array's first index, and each element in the array represents your maximum jump length at that position.\n\nReturn `true` if you can reach the last index, or `false` otherwise.",
        "constraints": [
            "1 <= nums.length <= 10^4",
            "0 <= nums[i] <= 10^5",
        ],
        "expected_time_complexity": "O(n)",
        "expected_space_complexity": "O(1)",
        "example_explanations": {
            0: "Jump 1 step from index 0 to 1, then 3 steps to the last index.",
        },
    },
    "nc-jump-game-ii": {
        "leetcode_number": 45,
        "statement": "You are given a 0-indexed array of integers `nums` of length `n`. You are initially positioned at `nums[0]`.\n\nEach element `nums[i]` represents the maximum length of a forward jump from index `i`. In other words, if you are at `nums[i]`, you can jump to any `nums[i + j]` where `1 <= j <= nums[i]` and `i + j < n`.\n\nReturn the minimum number of jumps to reach `nums[n - 1]`. The test cases are generated such that you can reach `nums[n - 1]`.",
        "constraints": [
            "1 <= nums.length <= 10^4",
            "0 <= nums[i] <= 1000",
            "It is guaranteed that you can reach nums[n - 1].",
        ],
        "expected_time_complexity": "O(n)",
        "expected_space_complexity": "O(1)",
        "example_explanations": {
            0: "Jump 1 step, then 3 steps: two jumps reach the end.",
        },
    },
    "nc-gas-station": {
        "leetcode_number": 134,
        "statement": "There are `n` gas stations along a circular route, where the amount of gas at the `i-th` station is `gas[i]`.\n\nYou have a car with an unlimited gas tank and it costs `cost[i]` of gas to travel from the `i-th` station to its next `(i + 1)-th` station. You begin the journey with an empty tank at one of the gas stations.\n\nGiven two integer arrays `gas` and `cost`, return the starting gas station's index if you can travel around the circuit once in the clockwise direction, otherwise return `-1`. If there exists a solution, it is guaranteed to be unique.",
        "constraints": [
            "n == gas.length == cost.length",
            "1 <= n <= 10^5",
            "0 <= gas[i], cost[i] <= 10^4",
        ],
        "expected_time_complexity": "O(n)",
        "expected_space_complexity": "O(1)",
        "example_explanations": {
            0: "Start at station 3: fill 4, spend 1, arrive at 0 with 3; fill 1, spend 2 -> 2; fill 2, spend 3 -> 1; fill 3, spend 4 -> 0. All stations visited.",
        },
    },
    "nc-hand-of-straights": {
        "leetcode_number": 846,
        "statement": "Alice has some number of cards and she wants to rearrange the cards into groups so that each group is of size `groupSize`, and consists of `groupSize` consecutive cards.\n\nGiven an integer array `hand` where `hand[i]` is the value written on the `i-th` card and an integer `groupSize`, return `true` if she can rearrange the cards, or `false` otherwise.",
        "constraints": [
            "1 <= hand.length <= 10^4",
            "0 <= hand[i] <= 10^9",
            "1 <= groupSize <= hand.length",
        ],
        "expected_time_complexity": "O(n log n)",
        "expected_space_complexity": "O(n)",
        "example_explanations": {
            0: "Group 1: [1, 2, 3], Group 2: [2, 3, 4], Group 3: [3, 4, 5].",
        },
    },
    "nc-maximum-subarray": {
        "leetcode_number": 53,
        "statement": "Given an integer array `nums`, find the subarray with the largest sum, and return its sum.",
        "constraints": [
            "1 <= nums.length <= 10^5",
            "-10^4 <= nums[i] <= 10^4",
        ],
        "follow_up": "If you have figured out the O(n) solution, try coding another solution using the divide and conquer approach, which is more subtle.",
        "expected_time_complexity": "O(n)",
        "expected_space_complexity": "O(1)",
        "example_explanations": {
            0: "The subarray [4, -1, 2, 1] has the largest sum 6.",
        },
    },
    "nc-maximum-product-subarray": {
        "leetcode_number": 152,
        "statement": "Given an integer array `nums`, find a subarray that has the largest product, and return the product.\n\nThe test cases are generated so that the answer will fit in a 32-bit integer.",
        "constraints": [
            "1 <= nums.length <= 2 * 10^4",
            "-10 <= nums[i] <= 10",
            "The answer is guaranteed to fit in a 32-bit integer.",
        ],
        "expected_time_complexity": "O(n)",
        "expected_space_complexity": "O(1)",
        "example_explanations": {
            0: "The subarray [2, 3] has the largest product 6.",
        },
    },
    "st-rotate-array": {
        "leetcode_number": 189,
        "statement": "Given an integer array `nums`, rotate the array to the right by `k` steps, where `k` is non-negative.",
        "constraints": [
            "1 <= nums.length <= 10^5",
            "-2^31 <= nums[i] <= 2^31 - 1",
            "0 <= k <= 10^5",
        ],
        "follow_up": "Try to come up with as many solutions as you can. There are at least three different ways to solve this problem. Could you do it in-place with O(1) extra space?",
        "expected_time_complexity": "O(n)",
        "expected_space_complexity": "O(1)",
        "example_explanations": {
            0: "Rotating [1,2,3,4,5,6,7] right by 3 gives [5,6,7,1,2,3,4].",
        },
    },
    "st-move-zeroes": {
        "leetcode_number": 283,
        "statement": "Given an integer array `nums`, move all `0`'s to the end of it while maintaining the relative order of the non-zero elements.\n\nNote that you must do this in-place without making a copy of the array.",
        "constraints": [
            "1 <= nums.length <= 10^4",
            "-2^31 <= nums[i] <= 2^31 - 1",
        ],
        "follow_up": "Could you minimize the total number of operations done?",
        "expected_time_complexity": "O(n)",
        "expected_space_complexity": "O(1)",
        "example_explanations": {
            0: "Zeros are moved to the end while non-zero order is preserved: [1,3,12,0,0].",
        },
    },
    "nc-happy-number": {
        "leetcode_number": 202,
        "statement": "Write an algorithm to determine if a number `n` is happy.\n\nA happy number is a number defined by the following process:\n\n- Starting with any positive integer, replace the number by the sum of the squares of its digits.\n- Repeat the process until the number equals 1 (where it will stay), or it loops endlessly in a cycle which does not include 1.\n- Those numbers for which this process ends in 1 are happy.\n\nReturn `true` if `n` is a happy number, and `false` if not.",
        "constraints": [
            "1 <= n <= 2^31 - 1",
        ],
        "expected_time_complexity": "O(log n)",
        "expected_space_complexity": "O(log n)",
        "example_explanations": {
            0: "1^2 + 9^2 = 82, 8^2 + 2^2 = 68, 6^2 + 8^2 = 100, 1^2 + 0^2 + 0^2 = 1. Happy!",
            1: "The process enters an infinite cycle (2 -> 4 -> 16 -> 37 -> 58 -> 89 -> 145 -> 42 -> 20 -> 4), never reaching 1.",
        },
    },
    "nc-pow": {
        "leetcode_number": 50,
        "statement": "Implement `pow(x, n)`, which calculates `x` raised to the power `n` (i.e., `x^n`).",
        "constraints": [
            "-100.0 < x < 100.0",
            "-2^31 <= n <= 2^31 - 1",
            "n is an integer.",
            "Either x is not zero or n > 0.",
            "-10^4 <= x^n <= 10^4",
        ],
        "expected_time_complexity": "O(log n)",
        "expected_space_complexity": "O(log n)",
        "example_explanations": {
            0: "2.0 raised to 10 equals 1024.0.",
        },
    },
    "nc-reverse-integer": {
        "leetcode_number": 7,
        "statement": "Given a signed 32-bit integer `x`, return `x` with its digits reversed. If reversing `x` causes the value to go outside the signed 32-bit integer range `[-2^31, 2^31 - 1]`, then return `0`.\n\nAssume the environment does not allow you to store 64-bit integers (signed or unsigned).",
        "constraints": [
            "-2^31 <= x <= 2^31 - 1",
        ],
        "expected_time_complexity": "O(log x)",
        "expected_space_complexity": "O(1)",
        "example_explanations": {
            0: "123 reversed is 321.",
            1: "-123 reversed is -321.",
        },
    },
}
