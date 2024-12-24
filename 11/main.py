from functools import cache

class Line:
    def __init__(self, file):
        with open(file) as f:
            self.stones = [int(value) for value in f.read().strip().split()]

    @cache
    def blink(self, times, value = None):
        if value is None:
            count = 0
            for stone in self.stones:
                count += self.blink(times, stone)
            return count
        
        if times == 0:
            return 1
        
        if value == 0:
            return self.blink(times - 1, 1)
        elif len(str(value)) & 1:
            return self.blink(times - 1, value * 2024)
        else:
            val_str = str(value)
            mid = len(val_str) // 2
            left = int(val_str[:mid])
            right = int(val_str[mid:])
            return self.blink(times - 1, left) + self.blink(times - 1, right)

line = Line("11/input.txt")
print("Part 1:", line.blink(25), "stones")
print("Part 2:", line.blink(75), "stones")