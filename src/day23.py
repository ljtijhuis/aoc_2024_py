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

def find_largest_cluster_brute_force(vertices, edges, nodes):
    clusters = set([frozenset([v]) for v in vertices])
    
    while True:
        print("Doing a pass across clusters to see if they are interconnected. Count: " + str(len(clusters)))
        next_clusters = set()
        for c in clusters:
            for v in vertices:
                if are_interconnected(c, set([v])):
                    next_clusters.add(frozenset(c.union(set([v]))))
        
        if len(next_clusters) == 0:
            return max(clusters, key=len)
        clusters = next_clusters
       
def are_interconnected(c1, c2):
    for v1 in c1:
        for v2 in c2:
            if not (v1, v2) in edges:
                return False
    return True

def find_largest_cluster(vertices, edges, nodes):
    in_clique = set()
    to_consider = set(vertices)
    ignore = set()
    cliques_found = set()
    bron_kerbosch(in_clique, to_consider, ignore, nodes, cliques_found)
    return max(cliques_found, key=len)

def bron_kerbosch(in_clique, to_consider, ignore, nodes, cliques_found):
    if len(to_consider) == 0 and len(ignore) == 0:
        cliques_found.add(frozenset(in_clique))
    else:
        while len(to_consider) > 0:
            v = to_consider.pop()
            neighbors = set([v2.vertice for v2 in nodes[v].edges])
            bron_kerbosch(
                in_clique.union({v}), # we add v to the clique found
                to_consider.intersection(neighbors), # the intersection of vertices left and that v is connected to
                ignore.intersection(neighbors), # ignore the ignore list intersected with neighbors
                nodes,
                cliques_found
            )
            ignore.add(v) # ignore v in the next iterations
    
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

largest_cluster = find_largest_cluster(vertices, edges, nodes)
print(",".join(sorted(largest_cluster)))

largest_cluster = find_largest_cluster_brute_force(vertices, edges, nodes)
print(",".join(sorted(largest_cluster)))