import math
from time import sleep

class Node:
    def __init__(self, pos):
        self.pos = pos
        self.antinode = False

    def __str__(self):
        return Map.ANTINODE_SYMBOL if self.antinode else Map.NODE_SMYBOL

class Antenna(Node):
    def __init__(self, pos, freq):
        self.freq = freq
        super().__init__(pos)

    def __str__(self):
        return self.freq

class Map:
    NODE_SMYBOL = "."
    ANTINODE_SYMBOL = "#"
    
    def __init__(self, file):
        self.nodes = []
        with open(file) as f:
            for y, line in enumerate(f):
                self.nodes.append([])
                for x, symbol in enumerate(line.strip()):
                    if symbol == Map.NODE_SMYBOL:
                        self.nodes[y].append(Node((x, y)))
                    else:
                        self.nodes[y].append(Antenna((x, y), symbol))

        self.width = len(self.nodes[0])
        self.height = len(self.nodes)

    def get_node(self, pos):
        x, y = pos
        return self.nodes[y][x]
    
    def get_all_freq(self, freq):
        return [node for node in self.get_all_antennae() if node.freq == freq]
    
    def get_all_antennae(self):
        return [node for row in self.nodes for node in row if isinstance(node, Antenna)]
    
    def is_on_map(self, pos):
        x, y = pos
        return 0 <= x < self.width and 0 <= y < self.height
    
    def set_antinodes(self, node1, node2, resonate = False):
        if resonate:
            node1.antinode = True
            node2.antinode = True
            
        x1, y1 = node1.pos
        x2, y2 = node2.pos

        dx = x2 - x1
        dy = y2 - y1

        def add_antinode(x, y, dx, dy):
            while self.is_on_map((x, y)):
                x = x + dx
                y = y + dy

                if self.is_on_map((x, y)):
                    self.get_node((x, y)).antinode = True

                if not resonate:
                    break

        add_antinode(x1, y1, -dx, -dy)
        add_antinode(x2, y2, dx, dy)

    def count_antinodes(self):
        return sum([1 for row in self.nodes for node in row if node.antinode])
    
    def run(self, resonate = False):
        checked = []

        for node in self.get_all_antennae():
            others = self.get_all_freq(node.freq)
            others.remove(node)

            while others:
                other = others.pop()
                if other in checked:
                    continue
                self.set_antinodes(node, other, resonate)

            checked.append(node)

    def __str__(self):
        return "\n".join(["".join([str(node) for node in row]) for row in self.nodes])
    
map = Map("8/input.txt")
map.run()
print(map)
print(map.count_antinodes())
print("=" * (map.width + 2))
map.run(True)
print(map)
print(map.count_antinodes())