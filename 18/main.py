from enum import Enum
import heapq

class Direction(Enum):
    UP = 0, -1
    DOWN = 0, 1
    RIGHT = 1, 0
    LEFT = -1, 0

    def __init__(self, x, y):
        self.x = x
        self.y = y

class Coordinate:
    def __init__(self, x, y, region):
        self.x = x
        self.y = y
        self.region = region

        self.corrupted = False
        self.g = 0
        self.parent = None

    def get_exits(self):
        for direction in Direction:
            x = self.x + direction.x
            y = self.y + direction.y
            coord = self.region.get_coord(x, y)
            if coord is not None and not coord.corrupted:
                yield coord

    def get_h(self):
        return abs(self.x - self.region.exit.x) + abs(self.y - self.region.exit.y)
    
    def get_f(self):
        return self.g + self.get_h()
    
    def __lt__(self, other):
        return self.get_f() < other.get_f()

class Region:
    def __init__(self, size, file):
        self.size = size

        self.rebuild_grid()

        self.falling_bytes = []
        with open(file) as f:
            for coordinate in f:
                x, y = map(int, coordinate.strip().split(","))
                self.falling_bytes.append((x, y))

    def get_coord(self, x, y):
        if 0 <= x < self.size and 0 <= y < self.size:
            return self.grid[y][x]
        return None
    
    def build_path(self):
        current = self.exit
        self.path = [current]
        while current.parent:
            self.path.append(current.parent)
            current = current.parent
        self.path.reverse()

    def get_steps(self):
        return len(self.path) - 1
    
    def __str__(self):
        result = ""
        for row in self.grid:
            for coord in row:
                if coord in self.path:
                    result += "O"
                elif coord.corrupted:
                    result += "#"
                else:
                    result += "."
            result += "\n"
        return result
    
    def rebuild_grid(self):
        self.grid = []
        self.path = []
        for y in range(self.size):
            self.grid.append([])
            for x in range(self.size):
                self.grid[y].append(Coordinate(x, y, self))
        self.start = self.grid[0][0]
        self.exit = self.grid[self.size - 1][self.size - 1]

    def simulate_fall(self, fallen_bytes):
        for x, y in self.falling_bytes[:fallen_bytes]:
            self.grid[y][x].corrupted = True

    def find_cutoff(self):
        self.rebuild_grid()
        self.find_path()
        fallen_bytes = 0
        while self.get_steps() >= 0 and fallen_bytes < len(self.falling_bytes) + 1:
            fallen_bytes += 1
            x, y = self.falling_bytes[fallen_bytes - 1]
            if self.get_coord(x, y) in self.path:
                self.rebuild_grid()
                self.simulate_fall(fallen_bytes)
                self.find_path()

        return self.falling_bytes[fallen_bytes - 1] if fallen_bytes < len(self.falling_bytes) + 1 else None
    
    def find_path(self):
        open_list = []
        heapq.heappush(open_list, self.start)
        closed_list = set()
        while open_list:
            current_coord = heapq.heappop(open_list)
            if current_coord == self.exit:
                self.build_path()
                break
            closed_list.add(current_coord)
            for exit in current_coord.get_exits():
                if exit in closed_list:
                    continue

                if exit in open_list:
                    if exit.g > current_coord.g:
                        continue

                if exit.parent:
                    if exit.g < current_coord.g + 1:
                        continue

                exit.g = current_coord.g + 1
                exit.parent = current_coord
                heapq.heappush(open_list, exit)

region = Region(71, "18/input")
region.simulate_fall(1024)
region.find_path()
print(region)
part_1 = region.get_steps()
part_2 = region.find_cutoff()
print(part_1, part_2)
