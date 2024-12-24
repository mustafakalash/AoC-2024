from functools import cache

class Towels:
    def __init__(self, file):
        with open(file) as f:
            self.patterns = list(map(lambda line: line.strip(), f.readline().split(", ")))
            f.readline()
            self.designs = list(map(lambda line: line.strip(), f.read().splitlines()))

    @cache
    def build_design(self, design):
        sequences = []
        for pattern in self.patterns:
            if design == pattern:
                sequences.append([pattern])
            elif design.startswith(pattern):
                for sequence in self.build_design(design[len(pattern):]):
                    sequences.append([pattern] + sequence)

        return sequences
    
    def make_designs(self):
        usable_designs = 0
        total_patterns = 0
        for design in self.designs:
            sequences = self.build_design(design)
            print(design, sequences)
            if sequences:
                usable_designs += 1
                total_patterns += len(sequences)

        return usable_designs, total_patterns
    
towels = Towels("19/input.txt")
print(towels.make_designs())