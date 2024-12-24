import re

with open("3/input.txt") as f:
    memory = f.read()
    instrs = re.findall(r"mul\((\d{1,3}),(\d{1,3})\)|(do\(\))|(don't\(\))", memory)

    p1_prod_sum = 0
    p2_prod_sum = 0
    enabled = True
    for instr in instrs:
        if instr[2] == "do()":
            enabled = True
        elif instr[3] == "don't()":
            enabled = False
        elif enabled:
            p2_prod_sum += int(instr[0]) * int(instr[1])

        if len(instr[0]):
            p1_prod_sum += int(instr[0]) * int(instr[1])

    print(f"Part 1: {p1_prod_sum}", f"Part 2: {p2_prod_sum}", sep="\n")