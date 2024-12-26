class Schematic:
    HEIGHT = 7
    FILLED = "#"
    EMPTY = "."

    def __init__(self, schematic):
        self.schematic = schematic
    
    def __eq__(self, other):
        return self.schematic == other._schematic
    
    def __hash__(self):
        return hash(str(self.schematic))

class Floor:
    def __init__(self, file):
        self.schematics = []
        with open(file) as f:
            schematics = f.read().split("\n\n")
            for schematic in schematics:
                schematic = [row.strip() for row in schematic]
                self.schematics.append(Schematic(schematic))

    def try_keys(self):
        pairs = set()
        for schematic in self.schematics:
            for other in self.schematics:
                if not any(cell1 == cell2 == Schematic.FILLED for cell1, cell2 in zip(schematic.schematic, other.schematic)):
                    pairs.add(frozenset((schematic, other)))

        return len(pairs)
    
floor = Floor("25/input.txt")
print(floor.try_keys())