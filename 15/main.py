from enum import Enum

class Direction(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

    @staticmethod
    def from_symbol(symbol):
        if symbol == "^":
            return Direction.UP
        if symbol == "v":
            return Direction.DOWN
        if symbol == "<":
            return Direction.LEFT
        if symbol == ">":
            return Direction.RIGHT
        
        raise ValueError(f"Unknown direction symbol: {symbol}")
    
    def x(self):
        return self.value[0]
    
    def y(self):
        return self.value[1]

class TileType(Enum):
    WALL = "#"
    BOX = "O"
    ROBOT = "@"
    EMPTY = "."
    LEFT_BOX = "["
    RIGHT_BOX = "]"

    def is_movable(self):
        return self in [TileType.BOX, TileType.ROBOT, TileType.LEFT_BOX, TileType.RIGHT_BOX]
    
    def wider(self):
        if self is TileType.BOX:
            return TileType.LEFT_BOX, TileType.RIGHT_BOX
        elif self is TileType.ROBOT:
            return TileType.ROBOT, TileType.EMPTY
        else:
            return self, self

class Tile:
    def __init__(self, tile_type, x, y, warehouse):
        self.type = tile_type
        self.x = x
        self.y = y
        self.warehouse = warehouse

    def __str__(self):
        return self.type.value
    
    def attempt_move(self, direction, move = True, check_other = True):
        if self.type.is_movable():
            other = None
            if check_other and direction in [Direction.UP, Direction.DOWN]:
                if self.type is TileType.LEFT_BOX:
                    other = self.warehouse.get_tile(self.x + 1, self.y)
                elif self.type is TileType.RIGHT_BOX:
                    other = self.warehouse.get_tile(self.x - 1, self.y)
                    
            x, y = self.x + direction.x(), self.y + direction.y()
            tile = self.warehouse.get_tile(x, y)
            if tile.type is TileType.EMPTY or tile.attempt_move(direction, False):
                if other and not other.attempt_move(direction, False, False):
                    return False

                if move:
                    if self.type is TileType.ROBOT:
                        self.warehouse.robot = tile

                    tile.attempt_move(direction)
                    
                    tile.type = self.type
                    self.type = TileType.EMPTY
                
                    if other:
                        other.attempt_move(direction, True, False)

                return True

        return False
    
    def get_gps(self):
        return (100 * self.y) + self.x

class Warehouse:
    def __init__(self, file, wider = False):
        self.tiles = []
        self.commands = []
        with open(file) as f:
            for y, line in enumerate(f):
                if line == "\n":
                    break

                row = []
                for x, symbol in enumerate(line.strip()):
                    types = [TileType(symbol)]
                    if wider:
                        x *= 2
                        types = types[0].wider()

                    for i, type in enumerate(types):
                        tile = Tile(type, x + i, y, self)
                        if tile.type is TileType.ROBOT:
                            self.robot = tile
                        row.append(tile)
                self.tiles.append(row)

            for line in f:
                self.commands.extend(line.strip())
        
    def get_tile(self, x, y):
        return self.tiles[y][x]
    
    def get_gps(self):
        return sum([box.get_gps() for row in self.tiles for box in row if box.type in [TileType.BOX, TileType.LEFT_BOX]])
    
    def run(self):
        for command in self.commands:
            direction = Direction.from_symbol(command)
            self.robot.attempt_move(direction)

    def __str__(self):
        return "\n".join(["".join([str(tile) for tile in row]) for row in self.tiles])
    
warehouse1 = Warehouse("15/input.txt")
warehouse2 = Warehouse("15/input.txt", True)

warehouse1.run()
print(warehouse2)
warehouse2.run()
print(warehouse2)
print(warehouse1.get_gps())
print(warehouse2.get_gps())