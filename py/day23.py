import networkx as nx


def main():
    f = open("../input/real/day23_1.txt")
    # f = open("../input/sample/day23_1.txt")
    graph = set()
    for line in f.readlines():
        nodes = line.split("-")
        nodes.sort()
        graph.add((nodes[0].strip(), nodes[1].strip()))

    edges = {}
    for n1, n2 in graph:
        en1 = edges.get(n1, [])
        en1.append(n2)
        edges[n1] = en1
        en2 = edges.get(n2, [])
        en2.append(n1)
        edges[n2] = en2

    threes = set()
    for e1a, e1b in graph:
        for e2a, e2b in graph:
            if e1a == e2a:
                if e2b in edges[e1b]:
                    # Will need to sort these
                    threes.add(tuple(sorted([e1a, e1b, e2b])))
            if e1b == e2b:
                if e2a in edges[e1a]:
                    # Will need to sort these
                    threes.add(tuple(sorted([e1b, e2a, e1a])))

    sum = 0
    for e1a, e1b, e2b in threes:
        if e1a.startswith("t") or e1b.startswith("t") or e2b.startswith("t"):
            sum += 1

    print(sum)

    G = nx.Graph()

    for a, b in graph:
        G.add_edge(a, b)
    mc = max(nx.find_cliques(G), key=len)
    mc.sort()
    print(",".join(mc))
    print(len(mc))


if __name__ == "__main__":
    main()
