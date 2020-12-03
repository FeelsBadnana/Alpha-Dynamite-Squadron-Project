import algorithm
from mpi4py import MPI
import networkx as nx



def main():
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()


    graph = nx.erdos_renyi_graph(10, 0.20, directed = True)
    if(rank == 0):
        print(algorithm.sequentialClosenessCentrality(graph))
    print(algorithm.parallelClosenessCentrality(graph, comm))
    # if(rank == 0):
    #     # print("hello")
    #     # twitter_filename = "twitter_combined.txt.gz"
    #     # twitter = initData(twitter_filename)
    #     # graph = nx.erdos_renyi_graph(1000, 0.20, directed = True)
    #     # algorithm.parallelClosenessCentrality(graph, comm)
        
    #     # output
    #     # print five top
    # else:
    #     algorithm.parallelClosenessCentrality(None, comm)
    

def initData(fileName):
    #open datafile
    with gzip.open(fileName, 'rt') as f:
        edges = f.read()

    nxGraph = nx.DiGraph()

    #adding all edges from graph
    for line in edges.splitlines():
        nodeset = line.split()
        nxGraph.add_edge(*[int(n) for n in nodeset])

    return nxGraph

if __name__ == "__main__":
    main()
