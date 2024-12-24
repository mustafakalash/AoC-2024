from itertools import product

P1_OPERATORS = [
    lambda x, y: x + y,
    lambda x, y: x * y
]

P2_OPERATORS = [
    lambda x, y: int(str(x) + str(y))
]

def test_possibilities(possibilities, operands, test):
    for possibility in possibilities:
        result = operands[0]
        for i in range(len(possibility)):
            result = possibility[i](result, operands[i + 1])
        if result == test:
            return test
            
    return 0

with open("7/input.txt") as f:
    p1_calibration_sum = 0
    p2_calibration_sum = 0
    for line in f:
        test, operands = line.strip().split(":")
        test = int(test)
        operands = list(map(lambda operand: int(operand), operands.strip().split(" ")))

        p1_possiblities = product(P1_OPERATORS, repeat = len(operands) - 1)
        p1_calibration_sum += test_possibilities(p1_possiblities, operands, test)

        p2_possiblities = product(P1_OPERATORS + P2_OPERATORS, repeat = len(operands) - 1)
        p2_calibration_sum += test_possibilities(p2_possiblities, operands, test)

    print(f"Part 1: {p1_calibration_sum}\nPart 2: {p2_calibration_sum}")
                

    
