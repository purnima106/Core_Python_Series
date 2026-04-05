# O(1) - Constant Time
arr = [1, 2, 3, 4, 5]
print(arr[0])
 # O(1) - Constant Time - No matter how large the array is, the time taken to access the first element is always the same. 
 # This is because the computer can directly access the first element of the array without having to iterate through the array.
 # This is the best case scenario for accessing an element in an array.

#O(n) - Linear Time
arr = [1, 2, 3, 4, 5]
for x in arr:
    print(x)
# O(n) - Linear Time - The time taken to iterate through the array is directly proportional to the size of the array.

#O(n^2) - Quadratic Time
arr = [1, 2, 3, 4, 5]
for i in arr:
    for j in arr:
        print(i, j)
# O(n^2) - Quadratic Time - The time taken to iterate through the array is proportional to the square of the size of the array.

#O(log n) - Binary Search
arr = [1, 2, 3, 4, 5]

low = 0
high = len(arr) - 1
target = 4

while low <= high:
    mid = (low + high) // 2

    if arr[mid] == target:
        print(f"Target found at index {mid}")
        break
    elif arr[mid] < target:
        low = mid + 1
    else:
        high = mid - 1
# O(log n) - Binary Search - The time taken to find the target in the array is proportional to the logarithm of the size of the array.

#O(n log n) - Merge Sort,Sorting
arr = [5,6,4,3,2,1]

arr.sort()
print(arr)

# #O(n log n) - Merge Sort,Sorting
# arr = [5,6,4,3,2,1]

# def merge_sort(arr):
#     if len(arr) > 1:
#         mid = len(arr) // 2
#         left = arr[:mid]
#         right = arr[mid:]

#         merge_sort(left)
#         merge_sort(right)
        
# | Pattern       | Big O      |
# | ------------- | ---------- |
# | Direct access | O(1)       |
# | One loop      | O(n)       |
# | Nested loops  | O(n²)      |
# | Halving data  | O(log n)   |
# | Sorting       | O(n log n) |


