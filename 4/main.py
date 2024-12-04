from enum import Enum
from time import sleep

class Direction(Enum):
    NORTH = (0, -1)
    SOUTH = (0, 1)
    EAST = (1, 0)
    WEST = (-1, 0)
    NORTH_EAST = (1, -1)
    NORTH_WEST = (-1, -1)
    SOUTH_EAST = (1, 1)
    SOUTH_WEST = (-1, 1)

    def flip(self):
        return Direction((-self.value[0], -self.value[1]))
    
class WordSearch:
    def __init__(self, file):
        self._word_search = []

        with open(file) as f:
            for x, line in enumerate(f):
                self._word_search.append([])
                for y, char in enumerate(line.strip()):
                    self._word_search[x].append(Letter(char, (x, y)))

    def get_letter(self, pos):
        return self._word_search[pos[0]][pos[1]]
    
    def get_letter_in_dir(self, letter, direction):
        x = letter.pos[0] + direction[0]
        y = letter.pos[1] + direction[1]

        if x < 0 or y < 0 or x >= len(self._word_search) or y >= len(self._word_search[x]):
            return None

        return self.get_letter((x, y))

    def get_word_in_dir(self, letter, direction):
        letters = [letter]

        for _ in range(Letter.order.index(letter.letter), len(Letter.order)):            
            new_letter = self.get_letter_in_dir(letter, direction)
            if new_letter is not None and letter.connects_to(new_letter):
                letter = new_letter
                letters.append(letter)
                
        return letters

    def __str__(self):
        return "\n".join(["".join([str(letter) for letter in row]) for row in self._word_search])

    def __iter__(self):
        for row in self._word_search:
            for letter in row:
                yield letter

class Letter:
    X = "X"
    M = "M"
    A = "A"
    S = "S"
    order = [X, M, A, S]

    def connects_to(self, letter):
        return Letter.order.index(self.letter) + 1 == Letter.order.index(letter.letter)
                
    def __init__(self, letter, pos):
        self.letter = letter
        self.pos = pos
        self.used = False
    
    def __str__(self):
        return self.letter if self.used else "."

class Solution:
    p1_word_search = None
    p2_word_search = None
    p1_count = 0
    p2_count = 0

    @staticmethod
    def solve(file):
        Solution.p1_word_search = WordSearch(file)
        Solution.p2_word_search = WordSearch(file)

        for letter in Solution.p1_word_search:
            if letter.letter == Letter.X:
                for direction in Direction:
                    word = Solution.p1_word_search.get_word_in_dir(letter, direction.value)
                    if len(word) == len(Letter.order):
                        for used_letter in word:
                            used_letter.used = True
                        Solution.p1_count += 1

            elif letter.letter == Letter.A:
                letter = Solution.p2_word_search.get_letter(letter.pos)
                words = []
                for corner_dir in [Direction.NORTH_EAST, Direction.NORTH_WEST, Direction.SOUTH_EAST, Direction.SOUTH_WEST]:
                    corner = Solution.p2_word_search.get_letter_in_dir(letter, corner_dir.value)
                    if corner is None or corner.letter != Letter.M:
                        continue
                    word = Solution.p2_word_search.get_word_in_dir(corner, corner_dir.flip().value)

                    if len(word) == len(Letter.order[Letter.order.index(Letter.M):]):
                        words.append(word)

                if len(words) == 2:
                    for used_word in words:
                        for used_letter in used_word:
                            used_letter.used = True

                    Solution.p2_count += 1
        
        Solution.display_results()

    @staticmethod
    def display_results():
        print(Solution.p1_word_search)
        print(f"XMAS found: {Solution.p1_count}")
        print(Solution.p2_word_search)
        print(f"X-MAS found: {Solution.p2_count}")

Solution.solve("4/input")