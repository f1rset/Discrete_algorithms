"""Module for graphs"""
import time
import random
from itertools import combinations, groupby
import matplotlib.pyplot as plt
import networkx as nx
from tqdm import tqdm

#_________________________________________________________

def bellman_ford(graph, source):
    """realization of bellman-ford algorithm

    Args:
        graph (DiGrapf): oriented graph
        source (_type_): node from which starts algorithm

    Raises:
        ValueError: If negative cycle in graph

    Returns:
        dict: distances from source node
    """
    distances = {node: float('inf') for node in graph.nodes()}
    distances[source] = 0

    for _ in range(len(graph.nodes()) - 1):
        for u, v, weight in graph.edges(data='weight'):
            if distances[u] + weight < distances[v]:
                distances[v] = distances[u] + weight

    # Check for negative cycles
    for u, v, weight in graph.edges(data='weight'):
        if distances[u] + weight < distances[v]:
            raise ValueError("Graph contains a negative cycle")

    return distances




def floyd_warshall(graph):
    """realization of floyd-warshall algorithm

    Args:
        graph (DiGraph): oriented graph

    Returns:
        list: matrix of distances
    """
    num_nodes = len(graph.nodes())
    distances = [[float('inf')] * num_nodes for _ in range(num_nodes)]

    for u, v, weight in graph.edges(data='weight'):
        distances[u][v] = weight

    for i in range(num_nodes):
        distances[i][i] = 0

    for k in range(num_nodes):
        for i in range(num_nodes):
            for j in range(num_nodes):
                distances[i][j] = min(distances[i][j], distances[i][k] + distances[k][j])

    return distances


#_____________________________________________________
# You can use this function to generate a random graph with 'num_of_nodes' nodes
# and 'completeness' probability of an edge between any two nodes
# If 'directed' is True, the graph will be directed
# If 'draw' is True, the graph will be drawn
def gnp_random_connected_graph(num_of_nodes: int,
                               completeness: float,
                               directed: bool = False,
                               draw: bool = False):
    """
    Generates a random graph, similarly to an Erdős-Rényi 
    graph, but enforcing that the resulting graph is conneted (in case of undirected graphs)
    """


    if directed:
        G = nx.DiGraph()
    else:
        G = nx.Graph()
    edges = combinations(range(num_of_nodes), 2)
    G.add_nodes_from(range(num_of_nodes))

    for _, node_edges in groupby(edges, key = lambda x: x[0]):
        node_edges = list(node_edges)
        random_edge = random.choice(node_edges)
        if random.random() < 0.5:
            random_edge = random_edge[::-1]
        G.add_edge(*random_edge)
        for e in node_edges:
            if random.random() < completeness:
                G.add_edge(*e)

    for (u,v,w) in G.edges(data=True):
        w['weight'] = random.randint(-5, 20)

    if draw:
        plt.figure(figsize=(10,6))
        if directed:
            # draw with edge weights
            pos = nx.arf_layout(G)
            nx.draw(G,pos, node_color='lightblue',
                    with_labels=True,
                    node_size=500,
                    arrowsize=20,
                    arrows=True)
            labels = nx.get_edge_attributes(G,'weight')
            nx.draw_networkx_edge_labels(G, pos,edge_labels=labels)

        else:
            nx.draw(G, node_color='lightblue',
                with_labels=True,
                node_size=500)

    return G

G = gnp_random_connected_graph(10, 0.5, True, True)
if __name__=='__main__':
    NUM_OF_ITERATIONS = 50
    time_taken: float = 0
    for i in tqdm(range(NUM_OF_ITERATIONS)):

        # note that we should not measure time of graph creation
        G = gnp_random_connected_graph(500, 0.4, False)

        start = time.time()
        floyd_warshall(G)
        end = time.time()

        time_taken += end - start

    print(time_taken / NUM_OF_ITERATIONS)
