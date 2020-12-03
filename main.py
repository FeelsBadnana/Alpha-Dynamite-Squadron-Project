import algorithm
from mpi4py import MPI
import networkx as nx
import sys
import time

# Arguments: File Name of Graph Data (txt)
def main():
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()

    graph = None

    # Check command-line arguments
    if(len(sys.argv) != 2):
        if(rank == 0):
            print(len(sys.argv), "is an invalid number of arguments.")
            print("Please enter only one file argument. Ending program now ...")
        return

    # Read in command-line argument
    graph_name = sys.argv[1]

    if(rank == 0):
        # Read in graph data
        graph = nx.read_edgelist(graph_name, create_using=nx.DiGraph)

    # Run closeness centrality measure
    cc, elapsed_time = runCC(graph, comm)

    if(rank == 0):
        # Export Data after finishing program for node 0 only
        exportCCData(cc, graph_name)
        exportTime(elapsed_time, graph_name, comm.Get_size())
    
def runCC(graph, comm):

    cc = {}
    elapsed_time = -1

    rank = comm.Get_rank()
    num_of_nodes = comm.Get_size()

    # node 0 should start time
    if(rank == 0):
        start = time.time()

    # Run parallel algorithm if nodes > 1
    if num_of_nodes > 1:
        if(rank == 0):
            cc = algorithm.parallelClosenessCentrality(graph, comm)
        else:
            algorithm.parallelClosenessCentrality(None, comm)

    # Run sequential algorithm if nodes = 1
    elif num_of_nodes == 1:
        cc = algorithm.sequentialClosenessCentrality(graph)

    # Raise error if nodes < 1
    else:
        raise SystemExit('Nodes cannot be less than one. You entered {}'.format(nodes))

    # Calculate elapsed time of CC
    if(rank == 0):
        end = time.time()
        elapsed_time = end - start

    return cc, elapsed_time

def exportCCData(cc, graph_name):
    # Find top five cc values and average
    cc_ordered = sorted(cc.items(), key=lambda x: x[1], reverse=True)
    cc_top_five = cc_ordered[0:5]
    cc_avg = sum(cc.values()) / len(cc)

    # Export following Closeness Centrality data to txt file
    with open("output.txt", "a") as f:
        f.write("Graph {}:\n".format(graph_name))
        f.write("top 5 nodes by cc: {}\n".format(cc_top_five))
        f.write("cc average value: {}\n\n\n".format(cc_avg))

def exportTime(elapsed_time, graph_name, num_of_nodes):
    output = "{}, {}, {}\n".format(graph_name, num_of_nodes, elapsed_time)

    # Export elapsed time to csv file
    with open("time.csv", "a") as f:
        f.write(output)

if __name__ == "__main__":
    main()
