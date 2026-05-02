# #Two Sum Problem
# nums = [2,7,11,15]
# target = 9

# for i in range(len(nums)):
#     for j in range(i+1, len(nums)):
#         if nums[i] + nums[j] == target:
#             print(i , j)



# numss = [2,7,11,15]

# target = 9

# seen = {} #Empty dictionary. This will store numbers we have seen

# for i in range (len(numss)):
#     nums = numss[i]
#     needed = target - nums

#     if needed in seen:
#         print(seen[needed], 1)

#     seen[nums] = i

#Contains Duplicate Problem

# nums = [1 ,2,3,1]

# for i in range(len(nums)):
#     for j in range(i+1, len(nums)):
#         for j in range(i+1,len(nums)):
#             if nums[i] == nums[j]:
#                 print("Duplicate Found")


nums = [1,2,3,4,1]

seen = set()
for x in nums:
    if x in seen:
        print("Duplicate Found")
        break
    seen.add(x)