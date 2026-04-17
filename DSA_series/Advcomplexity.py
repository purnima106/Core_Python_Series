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

nums = [2, 7]
target = 9

seen = {}

for i in range(len(nums)):
    num = nums[i]
    needed = target - num

    print("num:", num, "needed:", needed)


