from enum import Enum
import bisect
from itertools import groupby
import heapq

class TileType(Enum):
    TRACK = "."
    WALL = "#"
    START = "S"
    END = "E"

class Direction(Enum):
    UP = 0, -1
    DOWN = 0, 1
    LEFT = -1, 0
    RIGHT = 1, 0

    def __init__(self, x, y):
        self.x = x
        self.y = y

class Tile:
    def __init__(self, type, x, y, track):
        self.type = type
        self.x = x
        self.y = y
        self.track = track

    def get_exits(self, can_cheat = False):
        for direction in Direction:
            x, y = direction.x, direction.y
            tile = self.track.get_tile(self.x + x, self.y + y)
            if tile and (can_cheat or tile.type is not TileType.WALL):
                yield tile

    def __str__(self):
        return str(self.type.value)

class Node:
    def __init__(self, tile, target, parent = None):
        self.tile = tile
        self.target = target
        self.parent = parent
        if parent:
            self.g = parent.g + 1
        else:
            self.g = 0

    def get_h(self):
        return abs(self.tile.x - self.target.x) + abs(self.tile.y - self.target.y)
    
    def get_f(self):
        return self.g + self.get_h()

    def __lt__(self, other):
        return self.get_f() < other.get_f()
    
    def __eq__(self, other):
        return self.tile == other.tile
    
    def __hash__(self):
        return hash(self.tile)
    
class Cheat:
    def __init__(self, start, end, shortcut, track):
        self.start = start
        self.end = end
        self.shortcut = shortcut
        self.track = track

        start_i = track.path.index(start)
        end_i = track.path.index(end)
        self.path = self.track.path[:start_i] + shortcut + self.track.path[end_i + 1:]
        self.time = len(track.path) - len(self.path)

        if self not in track.cheats:
            bisect.insort(track.cheats, self)

    def __eq__(self, other):
        return self.start == other.start and self.end == other.end

    def __lt__(self, other):
        return self.time < other.time

class Track:
    def __init__(self, file):
        self.track = []

        with open(file) as f:
            for y, line in enumerate(f):
                self.track.append([])
                for x, char in enumerate(line.strip()):
                    type = TileType(char)
                    self.track[y].append(Tile(type, x, y, self))
                    if type == TileType.START:
                        self.start = self.get_tile(x, y)
                    elif type == TileType.END:
                        self.end = self.get_tile(x, y)

        self.build_path()

    def build_path(self):
        tile = self.start
        self.path = [tile]
        while tile is not self.end:
            for tile in tile.get_exits():
                if tile not in self.path:
                    break
            self.path.append(tile)

    def find_cheats(self, cheat_length):
        self.cheats = []
        for start_i, start_tile in enumerate(self.path):
            for end_i, end_tile in enumerate(self.path[start_i + 1:], start_i + 1):
                open_list = [Node(start_tile, end_tile)]
                heapq.heapify(open_list)
                closed_list = set(self.path[:start_i] + self.path[end_i + 1:])

                while open_list:
                    current_node = heapq.heappop(open_list)
                    closed_list.add(current_node.tile)

                    if current_node.tile.type is not TileType.WALL:
                        if current_node.tile not in (start_tile, end_tile):
                            continue

                    if current_node.tile is end_tile:
                        shortcut = []
                        while current_node:
                            shortcut.append(current_node.tile)
                            current_node = current_node.parent
                        shortcut.reverse()
                        
                        Cheat(start_tile, end_tile, shortcut, self)
                        break

                    for exit in current_node.tile.get_exits(True):
                        node = Node(exit, end_tile, current_node)

                        if exit in closed_list:
                            continue

                        if node.g > cheat_length:
                            continue

                        if node in open_list:
                            index = open_list.index(node)
                            if open_list[index].g < node.g - 1 or open_list[index].g > node.g:
                                del open_list[index]
                                heapq.heapify(open_list)
                            else:
                                continue

                        heapq.heappush(open_list, node)

    def count_cheats(self, min_time = 100, verbose = True):
        total = 0
        for time, cheats in groupby(self.cheats, key = lambda cheat: cheat.time):
            if time < min_time:
                continue
            count = len(list(cheats))
            total += count
            if verbose:
                print(f"There are {count} cheats that save {time} picoseconds")
        print(f"{total} cheats save at least {min_time} picoseconds")

    def get_tile(self, x, y):
        return self.track[y][x] if 0 <= y < len(self.track) and 0 <= x < len(self.track[y]) else None
    
    def to_string(self, cheat = None):
        string = ""
        for row in self.track:
            for tile in row:
                char = ""
                if cheat and tile in cheat.path and tile.type not in (TileType.START, TileType.END):
                    if tile in cheat.shortcut[1:]:
                        char = "0123456789abcdefghijk"[cheat.shortcut.index(tile)]
                    else:
                        char = "O"
                else:
                    char = str(tile)
                if cheat and tile in [cheat.start, cheat.end]:
                    char = red(char)
                string += char
            string += "\n"
        return string
    
    def __str__(self):
        return self.to_string()
    
def red(text):
    return f"\033[91m{text}\033[0m"

track = Track("20/input")
track.find_cheats(2)
track.count_cheats()
track.find_cheats(20)
track.count_cheats()