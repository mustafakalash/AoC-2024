from enum import Enum
import math
import sys
import heapq

sys.setrecursionlimit(100000)

class TileType(Enum):
    EMPTY = "."
    WALL = "#"
    START = "S"
    END = "E"
    
class Direction(Enum):
    NORTH = 0, -1
    SOUTH = 0, 1
    EAST = 1, 0
    WEST = -1, 0
    
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def rotations_to(self, other):
        return int(math.acos(self.x * other.x + self.y * other.y) / math.radians(90))
    
    def get_symbol(self):
        if self == Direction.NORTH:
            return "^"
        elif self == Direction.SOUTH:
            return "v"
        elif self == Direction.EAST:
            return ">"
        elif self == Direction.WEST:
            return "<"

class Tile:
    def __init__(self, x, y, type, maze):
        self.x = x
        self.y = y
        self.type = type
        self.maze = maze
    
    def get_exits(self):
        for direction in Direction:
            x = self.x + direction.x
            y = self.y + direction.y
            tile = self.maze.get_tile(x, y)
            if tile is not None and tile.type != TileType.WALL:
                yield tile

    def direction_to(self, other):
        return Direction((other.x - self.x, other.y - self.y))
    
    def __str__(self):
        return self.type.value
    
class Node:
    def __init__(self, tile, g = 0, parent = None, facing = Direction.EAST):
        self.tile = tile
        self.g = g
        self.parent = parent
        self.facing = facing

    def get_h(self):
        return abs(self.tile.x - self.tile.maze.end.x) + abs(self.tile.y - self.tile.maze.end.y)
    
    def get_f(self):
        return self.g + self.get_h()
    
    def __lt__(self, other):
        return self.get_f() < other.get_f()

class Maze:
    MOVE_COST = 1
    ROTATION_COST = 1000

    def __init__(self, filename):
        self.tiles = []
        self.start = None
        self.end = None
        self.paths = []

        with open(filename) as f:
            for y, line in enumerate(f):
                self.tiles.append([])
                for x, char in enumerate(line.strip()):
                    tile = Tile(x, y, TileType(char), self)
                    self.tiles[y].append(tile)
                    
                    if tile.type == TileType.START:
                        self.start = tile
                    elif tile.type == TileType.END:
                        self.end = tile

    def get_tile(self, x, y):
        if 0 <= y < len(self.tiles) and 0 <= x < len(self.tiles[y]):
            return self.tiles[y][x]
        else:
            return None
        
    def get_score(self):
        return self.paths[0][0].g if len(self.paths) else math.inf
        
    def find_path(self, current_node = None, closed_list = set()):
        if current_node is None:
            current_node = Node(self.start)

        closed_list.add(current_node.tile)

        if current_node.tile == self.end:
            print("Found path with score", current_node.g)
            if len(self.paths):
                if current_node.g > self.get_score():
                    return
                elif current_node.g < self.get_score():
                    self.paths = []

            self.paths.append(self.build_path(current_node))
            return

        open_list = []
        for exit in current_node.tile.get_exits():
            if exit in closed_list:
                continue

            direction = current_node.tile.direction_to(exit)
            rotations = current_node.facing.rotations_to(direction) * Maze.ROTATION_COST
            g = current_node.g + rotations + Maze.MOVE_COST

            if g > self.get_score():
                continue

            self.find_path(Node(exit, g, current_node, direction), closed_list.copy())
            heapq.heappush(open_list, Node(exit, g, current_node, direction))
        
        while open_list:
            break
            self.find_path(heapq.heappop(open_list), closed_list.copy())

    def build_path(self, node):
        path = []
        while node:
            path.append(node)
            node = node.parent

        return path
    
    def get_best_paths(self):
        paths = []
        for path in self.paths:
            if path[0].g <= self.get_score():
                paths.append(path)

        return paths
    
    def best_path_nodes(self):
        return len(set(node.tile for path in self.get_best_paths() for node in path))

    def __str__(self):
        paths = {}
        for path in self.get_best_paths():
            for node in path:
                pre = "\033[1m\033[41m"
                post = "\033[0m"
                if node.tile in paths.keys() and paths[node.tile] != pre + node.facing.get_symbol() + post:
                    symbol = "X"
                else:
                    symbol = node.facing.get_symbol()
                
                paths[node.tile] = pre + symbol + post

        result = ""
        for y in self.tiles:
            for tile in y:
                if tile in paths and tile.type == TileType.EMPTY:
                    result += paths[tile]
                else:
                    result += str(tile)
            result += "\n"
        return result

maze = Maze("16/input.txt")
maze.find_path()
print(maze)
print(maze.get_score(), maze.best_path_nodes())