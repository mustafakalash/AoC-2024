class Computer:
    def __init__(self, name):
        self.name = name
        self.connections = set()

    def add_connection(self, other):
        self.connections.add(other)
        other.connections.add(self)

    def __eq__(self, other):
        return self.name == other.name
    
    def __hash__(self):
        return hash(self.name)
    
    def __str__(self):
        return self.name
    
class Network:
    CHIEFS_NAME = "t"

    def __init__(self, file):
        self.computers = set()
        with open(file) as f:
            for line in f:
                c1, c2 = line.strip().split("-")
                computer1 = self.get_computer(c1)
                computer2 = self.get_computer(c2)
                computer1.add_connection(computer2)
                
    def get_computer(self, name):
        for computer in self.computers:
            if computer.name == name:
                return computer
            
        computer = Computer(name)
        self.computers.add(computer)
        return computer
    
    def find_lan_parties(self):
        parties = set()
        
        def bron_kerbosch(party, candidates, visited):
            if not candidates and not visited:
                if len(party) > 2:
                    parties.add(frozenset(party))
            for computer in candidates.copy():
                new_party = party | {computer}
                bron_kerbosch(new_party, candidates & computer.connections, visited & computer.connections)
                candidates.remove(computer)
                visited.add(computer)
                if len(new_party) > 2:
                    parties.add(frozenset(new_party))

        bron_kerbosch(set(), self.computers.copy(), set())

        return parties
    
    def find_chiefs_parties(self):
        chiefs_parties = 0
        parties = self.find_lan_parties()
        for party in parties:
            if len(party) == 3 and any(computer.name.startswith("t") for computer in party):
                chiefs_parties += 1
        
        return chiefs_parties, ",".join(sorted([str(computer) for computer in max(parties, key=len)]))
    
network = Network("23/input.txt")
print(network.find_chiefs_parties())