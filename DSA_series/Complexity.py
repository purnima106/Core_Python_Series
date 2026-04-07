# #O(n)

# arr = [1,2,3,4,5]

# for x in arr:
#     print(x)

# #O(n + m)

# users = [1,2,3,4,5]
# products = ["A", "B", "C","D", "E"]

# for u in users:
#     print(u)

# for p in products:
#     print(p)

# #O(n²)

# arr = [1,2,3,4,5]

# for i in arr:
#     for j in arr:
#         print(i, j)

arr = [1, 2, 3, 4]

for i in range(len(arr)):
    for j in range(i):
        print(i, j)

#O(log n)

n = 16

while n > 1:
    print(n)
    n = n //2

#Recursion O(n)

n = 16
def func(n):
    if n == 0:
        return 
    print(n)
    func(n - 1)