import itertools

class Node:
    def __init__(self, vertice):
        self.vertice = vertice
        self.edges = set()

    def add_edge(self, node):
        self.edges.add(node)

def find_clusters(vertices, edges, nodes):
    clusters = set()
    # We go over all the vertices
    for v in vertices:
        node = nodes[v]
        connected_nodes = []
        # and for each we collect what vertices they are connected to
        for other_node in node.edges:
            connected_nodes.append(other_node.vertice)

        # now if any of them are also connected, they form a cluster
        for v1, v2 in itertools.combinations(connected_nodes, 2):
            # one of them has to start with 't'
            if (v1, v2) in edges and (v.startswith('t') or v1.startswith('t') or v2.startswith('t')) :
                # sort the tuple to make sure we do not count these clusters twice
                # then add to our overall set of clusters
                clusters.add(tuple(sorted((v, v1, v2))))
    return len(clusters)


def read_file(f):
    with open(f) as opened_file:
        return opened_file.read()

def parse_input(text):
    edges = {(line.split("-")[0], line.split("-")[1]) for line in text.splitlines()}
    edges = edges.union({(line.split("-")[1], line.split("-")[0]) for line in text.splitlines()})
    vertices = {line.split("-")[0] for line in text.splitlines()}
    vertices = vertices.union({line.split("-")[1] for line in text.splitlines()})

    nodes = {}
    for v in vertices:
        nodes[v] = Node(v)
    
    for v1, v2 in edges:
        nodes[v1].add_edge(nodes[v2])

    return vertices, edges, nodes

text = read_file('day23.txt')
vertices, edges, nodes = parse_input(text)

num_clusters = find_clusters(vertices, edges, nodes)
print(num_clusters)
