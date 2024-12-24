import networkx as nx

computers = nx.read_edgelist("23/input.txt", delimiter="-", comments = "\r")

parties = list(nx.enumerate_all_cliques(computers))
chiefs_parties = 0
for party in parties:
    if len(party) == 3 and any(computer.startswith("t") for computer in party):
        chiefs_parties += 1

print(chiefs_parties)
print(",".join(sorted(max(parties, key=len))))