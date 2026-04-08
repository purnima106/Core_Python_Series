#O(1) space

arr = [1,2,3,4,5]

total = 0

for x in arr:
    total += x
    
print(total)

#eg 2: O(n)

arr = [1,2,3,4,5]

new_arr = []

for x in arr:
    new_arr.append(x)

print(new_arr)

#eg 3: Recursion (stack memory)

def func(n):
    if n == 0:
        return
    print(n)
    func(n - 1)

func(3)