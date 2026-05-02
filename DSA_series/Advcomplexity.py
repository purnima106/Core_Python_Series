# #1. Factorial — Linear Recursion (O(n))

# def fact(n):
#     if n == 0:
#         return 1
#         #both tines are---base lines(stopping condition) prevents from infinite recusrion
#     return n * fact(n - 1)

# n = 4
# result = fact(n)

# print("Factorial of", n, "is:", result)

# #time comp...is O(n)--4 → 3 → 2 → 1 → 0---Total = 5 calls ≈ n


# #2. Fibonacci

# def fib(n):
#     if n <= 1:
#         return n
#     return fib(n-1) + fib(n-2)

# n = 5
# for i in range(n):
#     print(f"fib({i}) =", fib(i))


#rewriting the ques again

# nums = [2, 7]
# target = 9

# seen = {}

# for i in range(len(nums)):
#     num = nums[i]
#     needed = target - num

#     print("num:", num, "needed:", needed)

# n = 10

# a = 0
# b = 1

# for i in range(n):
#     print(a)
#     next_num = a + b
#     a = b
#     b = next_num

# Complexity

# 👉 Time = O(n)
# 👉 Space = O(1) 

# n = 8

# fib = [0, 1]

# for i in range(2, n):
#     fib.append(fib[i-1] + fib[i-2])

# print(fib)

# space- O(n)

# nums = [1, 2, 3, 4]

# for i in range(1, len(nums)):
#     nums[i] = nums[i] + nums[i - 1]
# print(nums)

# Complexity

# 👉 Time = O(n) (loop runs once)

# 👉 Space = O(1) ✅ (very important)

# nums = [3,2,3]

# def majority(nums):
#     count = {}

#     for x in nums:
#         if x in count:
#             count[x] += 1
#         else:
#             count[x] = 1

#     for key in count:
#         if count[key] > len(nums) // 2:
#             return key

# print(majority([3,2,3]))

# Complexity
# Time → O(n)
# Space → O(n)

# Richest Customer Wealth

def richest(accounts):
    max_money = 0

    for person in accounts:
        total = sum(person)

        if total > max_money:
            max_money = total

    return max_money


print(richest([[1,2,3],[3,2,1]]))

