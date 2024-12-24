from enum import Enum
from functools import cache

class Direction(Enum):
    UP = 0, -1
    DOWN = 0, 1
    LEFT = -1, 0
    RIGHT = 1, 0

    def __init__(self, dx, dy):
        self.dx, self.dy = dx, dy

    def __str__(self):
        if self == Direction.UP:
            return "^"
        elif self == Direction.DOWN:
            return "v"
        elif self == Direction.LEFT:
            return "<"
        elif self == Direction.RIGHT:
            return ">"

class Key(Enum):
    ACTIVATE = "A"
    ONE = "1"
    TWO = "2"
    THREE = "3"
    FOUR = "4"
    FIVE = "5"
    SIX = "6"
    SEVEN = "7"
    EIGHT = "8"
    NINE = "9"
    ZERO = "0"
    UP = str(Direction.UP)
    DOWN = str(Direction.DOWN)
    LEFT = str(Direction.LEFT)
    RIGHT = str(Direction.RIGHT)
        
class Keypad:
    KEYS = []

    @classmethod
    def get_key_pos(cls, key):
        for y, row in enumerate(cls.KEYS):
            for x, k in enumerate(row):
                if k == key:
                    return x, y
        return None, None

    @classmethod      
    def get_key_at(cls, x, y):
        return cls.KEYS[y][x] if 0 <= x < cls.get_width() and 0 <= y < cls.get_height() else None
    
    @classmethod
    def get_width(cls):
        return len(cls.KEYS[0])
    
    @classmethod
    def get_height(cls):
        return len(cls.KEYS)
    
    @classmethod
    @cache
    def moves_to(cls, start, target):
        start_x, start_y = cls.get_key_pos(start)
        target_x, target_y = cls.get_key_pos(target)
        if start_x is None or target_x is None:
            raise ValueError(f"Invalid key for {cls.__name__}: {start} or {target}")
        
        dx = min(max(target_x - start_x, -1), 1)
        dy = min(max(target_y - start_y, -1), 1)

        x_first = cls.get_key_at(target_x, start_y) is not None
        x_moves = ""
        if dx != 0:
            for x in range(start_x, target_x, dx):
                x_moves += str(Direction((dx, 0)))
                if cls.get_key_at(x, start_y) is None:
                    x_first = False

        y_moves = ""
        if dy != 0:
            for _ in range(start_y, target_y, dy):
                y_moves += str(Direction((0, dy)))
        return x_moves + y_moves if x_first else y_moves + x_moves
    
    @classmethod
    @cache
    def key_in(cls, input):
        cur_key = Key.ACTIVATE
        moves = ""
        for key in input:
            key = Key(key)
            moves += cls.moves_to(cur_key, key) + Key.ACTIVATE.value
            cur_key = key
        return moves

class NumericKeypad(Keypad):
    KEYS = [
        [Key.SEVEN, Key.EIGHT, Key.NINE],
        [Key.FOUR, Key.FIVE, Key.SIX],
        [Key.ONE, Key.TWO, Key.THREE],
        [None, Key.ZERO, Key.ACTIVATE]
    ]

class DirectionalKeypad(Keypad):
    KEYS = [
        [None, Key.UP, Key.ACTIVATE],
        [Key.LEFT, Key.DOWN, Key.RIGHT]
    ]

class MyKeypad:
    def __init__(self, file = None):
        if file:
            self.inputs = open(file).read().splitlines()

    @classmethod
    def from_list(cls, inputs):
        keypad = cls()
        keypad.inputs = inputs
        return keypad
    
    @staticmethod
    @cache
    def extract_int(line):
        return int("".join(filter(str.isdigit, line)))

    @staticmethod
    @cache
    def get_complexity(input, moves):
        return len(moves) * MyKeypad.extract_int(input)

    @staticmethod
    @cache
    def key_in(input, robots):
        moves = NumericKeypad.key_in(input)
        for _ in range(robots):
            moves = DirectionalKeypad.key_in(moves)
        return moves

    @cache
    def total_complexity(self, robots):
        complexity = 0
        for input in self.inputs:
            moves = MyKeypad.key_in(input, robots)
            complexity += MyKeypad.get_complexity(input, moves)
        return complexity

class Test:
    ONE_PASS = {
        "029A": "<A^A>^^AvvvA"
    }
    TWO_PASSES = {
        "029A": "v<<A>>^A<A>AvA<^AA>A<vAAA>^A"
    }
    FULL_RESULTS = {
        "inputs": {
            "029A": {
                "moves": "<vA<AA>>^AvAA<^A>A<v<A>>^AvA^A<vA>^A<v<A>^A>AAvA^A<v<A>A>^AAAvA<^A>A",
                "complexity": 1972,
                "int": 29
            },
            "980A": {
                "moves": "<v<A>>^AAAvA^A<vA<AA>>^AvAA<^A>A<v<A>A>^AAAvA<^A>A<vA>^A<A>A",
                "complexity": 58800,
                "int": 980
            },
            "179A": {
                "moves": "<v<A>>^A<vA<A>>^AAvAA<^A>A<v<A>>^AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A",
                "complexity": 12172,
                "int": 179
            },
            "456A": {
                "moves": "<v<A>>^AA<vA<A>>^AAvAA<^A>A<vA>^A<A>A<vA>^A<A>A<v<A>A>^AAvA<^A>A",
                "complexity": 29184,
                "int": 456
            },
            "379A": {
                "moves": "<v<A>>^AvA^A<vA<AA>>^AAvA<^A>AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A",
                "complexity": 24256,
                "int": 379
            }
        },
        "complexity": 126384
    }

    @classmethod
    def run(cls):
        inputs = list(cls.FULL_RESULTS["inputs"].keys())
        keypad = MyKeypad.from_list(inputs)
        for input, result in cls.ONE_PASS.items():
            assert keypad.key_in(input, 0) == result
        for input, result in cls.TWO_PASSES.items():
            assert keypad.key_in(input, 1) == result

        for input, data in cls.FULL_RESULTS["inputs"].items():
            try:
                moves = keypad.key_in(input, 2)
                #assert moves == data["moves"]
                assert MyKeypad.extract_int(input) == data["int"]
                assert MyKeypad.get_complexity(input, moves) == data["complexity"]
            except AssertionError:
                print(f"Full test failed on {input}")
                print("Expected:")
                print(f"\t{data['moves']}")
                print(f"\t{data['int']}")
                print(f"\t{data['complexity']}")
                print("Got:")
                print(f"\t{moves}")
                print(f"\t{MyKeypad.extract_int(input)}")
                print(f"\t{MyKeypad.get_complexity(input, moves)}")
                return
        
        assert keypad.total_complexity(2) == cls.FULL_RESULTS["complexity"]

Test.run()
keypad = MyKeypad("21/input.txt")
print(keypad.total_complexity(2))
print(keypad.total_complexity(25))