from enum import Enum
from copy import deepcopy
from time import sleep

class Facing(Enum):
    NORTH = "^"
    EAST = ">"
    SOUTH = "v"
    WEST = "<"

    def __str__(self):
        return self.value

    def turn(self):
        if self == Facing.NORTH:
            return Facing.EAST
        elif self == Facing.EAST:
            return Facing.SOUTH
        elif self == Facing.SOUTH:
            return Facing.WEST
        elif self == Facing.WEST:
            return Facing.NORTH
        
    def coord_ahead(self, x, y):
        if self == Facing.NORTH:
            return x - 1, y
        elif self == Facing.EAST:
            return x, y + 1
        elif self == Facing.SOUTH:
            return x + 1, y
        elif self == Facing.WEST:
            return x, y - 1

class Map:
    def __init__(self, file_name):
        self.load_map(file_name)
        self.width = len(self[0])
        self.height = len(self)
    
    def load_map(self, file_name):
        self._map = []

        with open(file_name) as f:
            for x, line in enumerate(f):
                self._map.append([])
                for y, char in enumerate(line.strip()):
                    type = Position.Type.OBSTACLE if char == Position.Type.OBSTACLE.value else Position.Type.EMPTY
                    self[x].append(Position(x, y, type))

                    if char in [str(facing) for facing in Facing]:
                        self.guard_position = (x, y, Facing(char))
    
    def is_valid_position(self, x, y):
        return 0 <= x < self.height and 0 <= y < self.width
    
    def is_obstacle(self, x, y):
        return self[x][y].type in (Position.Type.OBSTACLE, Position.Type.TEST_OBSTACLE)
    
    def run(self, verbose = False):
        init_guard_position = self.guard_position
        visited = set()

        if verbose:
            print(self, end = "")

        while True:
            x, y, facing = self.guard_position
            self.guard_position = init_guard_position
            self[x][y].visited.add(facing)
            visited.add(self[x][y])

            ahead_x, ahead_y = facing.coord_ahead(x, y)

            if not self.is_valid_position(ahead_x, ahead_y):
                if verbose:
                    print()

                return False, visited
            
            if self[ahead_x][ahead_y].was_visited(facing):
                if verbose:
                    print()

                return True, visited

            if self.is_obstacle(ahead_x, ahead_y):
                facing = facing.turn()
            else:
                x = ahead_x
                y = ahead_y

            if verbose:
                move_caret_up(self.height)
                print(self, end = "")
                sleep(0.005)

            self.guard_position = (x, y, facing)

    def count_visited(self):
        return sum([1 for row in self for pos in row if pos.was_visited()])
    
    def __str__(self):
        string = ""
        guard_x, guard_y, guard_facing = self.guard_position
        for x in range(self.height):
            for y in range(self.width):
                if (x, y) == (guard_x, guard_y):
                    string += str(guard_facing)
                else:
                    string += str(self[x][y])
            string += "\n"

        return string

    def __getitem__(self, key):
        return self._map[key]
    
    def __setitem__(self, key, value):
        self._map[key] = value
    
    def __iter__(self):
        return iter(self._map)
    
    def __len__(self):
        return len(self._map)

class Position:
    class Type(Enum):
        EMPTY = "."
        OBSTACLE = "#"
        TEST_OBSTACLE = "O"

    def __init__(self, x, y, type):
        self.x = x
        self.y = y
        self.type = type
        self.visited = set()

    def was_visited(self, facing = None):
        return len(self.visited) > 0 if facing is None else facing in self.visited

    def __str__(self):
        if self.was_visited() and not self.type == Position.Type.TEST_OBSTACLE:
            if Facing.NORTH in self.visited or Facing.SOUTH in self.visited:
                if not Facing.EAST in self.visited and not Facing.WEST in self.visited:
                    return "|"
                else:
                    return "+"
            elif Facing.EAST in self.visited or Facing.WEST in self.visited:
                return "-"
        else:
            return self.type.value
        
def move_caret_up(lines = 1):
    print("\033[F" * lines, end = "")

map = Map("6/input")
map_copy = deepcopy(map)
_, visited = map_copy.run(True)
print("=" * map.width)
print()

loop_spots = checked = 0
for pos in visited:
    checked += 1

    if (pos.x, pos.y) == map.guard_position[:2]:
        continue

    map_copy = deepcopy(map)
    map_copy[pos.x][pos.y].type = Position.Type.TEST_OBSTACLE

    if map_copy.run()[0]:
        loop_spots += 1
        print(" " * 50, end = "\r")
        print(map_copy)
        print("-" * map.width)
        print()

    print(f"Checked: {checked}/{len(visited)}", f"Loop spots: {loop_spots}", end = "\r")

print(f"Part 1: {len(visited)}, part 2: {loop_spots}", " " * 50)


