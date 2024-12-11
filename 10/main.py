class Position:
    HEAD_HEIGHT = 0
    END_HEIGHT = 9

    def __init__(self, x, y, height):
        self.x = x
        self.y = y
        self.height = height
        self.heads = set()

        if self.is_head():
            self.score = 0
            self.rating = 0
            self.heads.add(self)

    def is_head(self):
        return self.height == Position.HEAD_HEIGHT
    
    def is_end(self):
        return self.height == Position.END_HEIGHT
    
    def __str__(self):
        return str(self.height)
    
class Map:
    def __init__(self, file):
        self.map = []
        with open(file) as f:
            for y, line in enumerate(f):
                self.map.append([])
                for x, height in enumerate(line.strip()):
                    height = int(height)
                    self.map[y].append(Position(x, y, height))
        
        self.width = len(self.map[0])
        self.height = len(self.map)

    def get_position(self, x, y):
        return self.map[y][x]
    
    def is_adjacent(self, pos1, pos2):
        return abs(pos1.x - pos2.x) + abs(pos1.y - pos2.y) == 1
    
    def can_move_to(self, cur, to):
        return self.is_adjacent(cur, to) and to.height - cur.height == 1
    
    def is_on_map(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height
    
    def get_exits(self, pos):
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        exits = []

        for dx, dy in directions:
            x, y = pos.x + dx, pos.y + dy
            if self.is_on_map(x, y):
                exit = self.get_position(x, y)
                if self.can_move_to(pos, exit):
                    exits.append(exit)

        return exits
    
    def paths_string(self, head):
        string = ""
        for row in self.map:
            row_string = ""
            for pos in row:
                if head in pos.heads:
                    row_string += str(pos)
                else:
                    row_string += "."
            if row_string.count(".") == len(row_string):
                continue
            string += row_string + "\n"
        return string
    
    def get_heads(self):
        heads = []
        for row in self.map:
            for pos in row:
                if pos.is_head():
                    heads.append(pos)
        return heads
    
    def find_ends(self, start, head = None):
        if head is None:
            head = start

        ends = []
        for exit in self.get_exits(start):
            if exit.is_end():
                ends.append(exit)
                exit.heads.add(head)
            else:
                more_ends = self.find_ends(exit, head)
                if len(more_ends):
                    exit.heads.add(head)
                ends.extend(more_ends)
            
        return ends

    def run(self):
        total_score = 0
        total_rating = 0
        for head in self.get_heads():
            ends = self.find_ends(head)
            head.rating = len(ends)
            head.score = len(set(ends))
            total_score += head.score
            total_rating += head.rating
            print(self.paths_string(head))
        
        return total_score, total_rating
    
    def __str__(self):
        return "\n".join("".join(str(pos) for pos in row) for row in self.map)
    
m = Map("10/input")
print(m)
print(m.run())
