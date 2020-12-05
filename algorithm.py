from mpi4py import MPI
import networkx as nx
from scipy.sparse import csr_matrix
import numpy as np
from heapq import heappush, heappop
from itertools import count

# Input: NetworkX Graph (G)
# Output: Dictionary of Closeness Centralities for all nodes in Graph G
def sequentialClosenessCentrality(G):
    # Initialize dictionary to hold all node, closeness centrality pairs
    closeness_centrality = {}

    if G.is_directed():
        G = G.reverse()  # create a reversed graph view

    for n in G.nodes:
        # Dijkstra’s is used as APSP algorithm
        sp = dijkstra(G, [n])
        # Mask infinity so we don't sum them later on and sum
        # sp = np.ma.masked_invalid(shortest_paths)
        totsp = sum(sp.values())
        len_G = G.number_of_nodes()
        len_sp = len(sp)

        _closeness_centrality = 0.0
        if totsp > 0.0 and len_G > 1:
            _closeness_centrality = (len_sp - 1.0) / totsp
            # normalize to number of nodes-1 in connected part
            s = (len_sp - 1.0) / (len_G - 1)
            _closeness_centrality *= s
        closeness_centrality[n] = _closeness_centrality

    return closeness_centrality

# Input: NetworkX Graph (G), comm
# Output: Dictionary of Closeness Centralities for all nodes in Graph G
def parallelClosenessCentrality(G, comm):

    rank = comm.Get_rank()
    P = comm.Get_size()

    if(rank == 0):
        # Initialize dictionary to hold all node, closeness centrality pairs
        closeness_centrality = {}

        if G.is_directed():
            G = G.reverse()  # create a reversed graph view

        # print("rank 0: {}".format(nx.number_of_edges(G)))

    # may throw error    
    G = comm.bcast(G, root=0)

    # Initialize closeness centrality partition
    cc_part = {}

    # Get number of nodes
    N = G.number_of_nodes()

    count = N // P
    remainder = N % P
    start = 0
    end = 0

    if rank < remainder:
        # The first 'remainder' ranks get 'count + 1' tasks each
        start = rank * (count + 1)
        stop = start + count
    else:
        # The remaining 'size - remainder' ranks get 'count' task each
        start = rank * count + remainder
        stop = start + (count - 1)
    
    rankNodes = list(G.nodes)[start: stop + 1]

    for n in rankNodes:
        # Dijkstra’s is used as APSP algorithm
        sp = dijkstra(G, [str(n)])
        # Mask infinity so we don't sum them later on and sum
        # sp = np.ma.masked_invalid(shortest_paths)
        totsp = sum(sp.values())
        len_G = G.number_of_nodes()
        len_sp = len(sp)

        _closeness_centrality = 0.0
        if totsp > 0.0 and len_G > 1:
            _closeness_centrality = (len_sp - 1.0) / totsp
            # normalize to number of nodes-1 in connected part
            s = (len_sp - 1.0) / (len_G - 1)
            _closeness_centrality *= s
        cc_part[n] = _closeness_centrality



    closeness_centrality_dict = comm.gather(cc_part, root=0)
    closeness_centrality = {}
    # wait for everyone
    if(rank == 0):
        for dictionary in closeness_centrality_dict:
            closeness_centrality.update(dictionary)
        return closeness_centrality
    else:
        return

def dijkstra(G, sources): 
    G_succ = G._succ if G.is_directed() else G._adj
    # print("{}".format(G_succ))
    push = heappush
    pop = heappop
    dist = {}  # dictionary of final distances
    seen = {}
    # frontier is heapq with 3-tuples (distance,c,node)
    # use the count c to avoid comparing nodes (may not be able to)
    c = count()
    frontier = []
    for source in sources:
        seen[source] = 0
        push(frontier, (0, next(c), source))
    while frontier:
        (d, _, v) = pop(frontier)
        if v in dist:
            continue  # already searched this node.
        dist[v] = d

        for u, e in G_succ[v].items():
            path_cost = dist[v] + 1
            if u not in seen or path_cost < seen[u]:
                seen[u] = path_cost
                push(frontier, (path_cost, next(c), u))
              
    # The optional predecessor and path dictionaries can be accessed
    # by the caller via the pred and paths objects passed as arguments.
    return dist