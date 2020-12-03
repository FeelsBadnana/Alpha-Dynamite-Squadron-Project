from mpi4py import MPI
import networkx as nx
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import dijkstra
import numpy as np

# Input: NetworkX Graph (G)
# Output: Dictionary of Closeness Centralities for all nodes in Graph G
def sequentialClosenessCentrality(G):
    # Initialize dictionary to hold all node, closeness centrality pairs
    closeness_centrality = {}

    if G.is_directed():
        G = G.reverse()  # create a reversed graph view

    # Convert NetworkX Graph to Scipy Sparse Matrix for Dijkstra's Algorithm
    sparseMatrix = nx.to_scipy_sparse_matrix(G)

    for n in G.nodes:
        # Dijkstra’s is used as APSP algorithm
        shortest_paths = dijkstra(csgraph=sparseMatrix, directed=True, indices=n)
        # Mask infinity so we don't sum them later on and sum
        sp = np.ma.masked_invalid(shortest_paths)
        totsp = sp.sum()
        len_G = np.size(sp)
        num_of_valid = np.size(sp) - np.ma.count_masked(sp)

        _closeness_centrality = 0.0
        if totsp > 0.0 and len_G > 1:
            _closeness_centrality = (num_of_valid - 1.0) / totsp
            # normalize to number of nodes-1 in connected part
            s = (num_of_valid - 1.0) / (len_G - 1)
            _closeness_centrality *= s
        closeness_centrality[n] = _closeness_centrality

    return closeness_centrality

# Input: NetworkX Graph (G), comm
# Output: Dictionary of Closeness Centralities for all nodes in Graph G
def parallelClosenessCentrality(G, comm):

    rank = comm.Get_rank()
    # print(rank)
    P = comm.Get_size()

    if(rank == 0):
        # print(rank)
        # Initialize dictionary to hold all node, closeness centrality pairs
        closeness_centrality = {}

        if G.is_directed():
            G = G.reverse()  # create a reversed graph view

        # Convert NetworkX Graph to Scipy Sparse Matrix for Dijkstra's Algorithm
        sparseMatrix = nx.to_scipy_sparse_matrix(G)
    else:
        sparseMatrix = None

    # may throw error    
    sparseMatrix = comm.bcast(sparseMatrix, root=0)
    



    # Initialize closeness centrality partition
    cc_part = {}

    # Get number of nodes
    N = sparseMatrix.shape[0]

    count = N // P
    remainder = N % P
    start = 0
    stop = 0

    if rank < remainder:
        # The first 'remainder' ranks get 'count + 1' tasks each
        start = rank * (count + 1)
        stop = start + count
    else:
        # The remaining 'size - remainder' ranks get 'count' task each
        start = rank * count + remainder
        stop = start + (count - 1)


    for n in range(start, stop + 1):
        # Dijkstra’s is used as APSP algorithm
        shortest_paths = dijkstra(csgraph=sparseMatrix, directed=True, indices=n)
        # Mask infinity so we don't sum them later on and sum
        sp = np.ma.masked_invalid(shortest_paths)
        totsp = sp.sum()
        len_G = np.size(sp)
        num_of_valid = np.size(sp) - np.ma.count_masked(sp)

        _closeness_centrality = 0.0
        if totsp > 0.0 and len_G > 1:
            _closeness_centrality = (num_of_valid - 1.0) / totsp
            # normalize to number of nodes-1 in connected part
            s = (num_of_valid - 1.0) / (len_G - 1)
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