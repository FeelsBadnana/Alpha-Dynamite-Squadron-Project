# Alpha Dynamite Squadron Project
 For CS4990; Implementing Closeness Centrality with Parallel Dijstra's Algorithm
 ![Team Logo](team_logo.jpg)
 
## Libraries Used 
 * Mpi4Py 3.4.3
 * NetworkX 2.5
 * NumPy 1.19.4
 * SciPy 1.5.4
 * Pi4py 3.0.3 (I don't know why it's in my environment; probably not necessary)

## Command to Run
    mpirun -n [Number of Nodes] python main.py [Name of Text File containing Graph Data]
 
## Export Data
 * *output.txt*
   * Graph [Graph Name]
     top 5 nodes by cc: [List of values]
     cc average value: [Int value]
  * *time.csv*
    *  [Graph Name], [Number of Nodes], [Elapsed Time to run CC]

 