with open("1/input.txt") as f:
    list1 = []
    list2 = []
    for line in f:
        nums = line.split("   ")
        list1.append(int(nums[0]))
        list2.append(int(nums[1]))

    list1.sort()
    list2.sort()
    
    sum = 0
    sim = 0
    for i in range(len(list1)):
        sum += abs(list1[i] - list2[i])
        sim += list1[i] * list2.count(list1[i])

    print(f"Part 1: {sum}")
    print(f"Part 2: {sim}")