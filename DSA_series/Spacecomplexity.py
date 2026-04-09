# #O(1) space

# arr = [1,2,3,4,5]

# total = 0

# for x in arr:
#     total += x
    
# print(total)

# #eg 2: O(n)

# arr = [1,2,3,4,5]

# new_arr = []

# for x in arr:
#     new_arr.append(x)

# print(new_arr)

# #eg 3: Recursion (stack memory)

# def func(n):
#     if n == 0:
#         return
#     print(n)
#     func(n - 1)

# func(3)

#eg 4: Space vs Time

nums = [1,2,3,4,5]

print(nums)
print(nums[-2:])

def func(arr):
    if len(arr) == 0:
        return
    print(arr[0])
    print(arr[1:])

func(nums)

x = nums[0]
y = nums[1]
z = nums[2]

print(x,y,z)





