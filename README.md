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
    sbatch cc.slurm
  **Make sure to edit the slurm file before continuing**
 
## Steps to edit Slurm File
  1. Add command line arguments with format: 
  *mpirun -n [# of nodes] python main.py [graph file]*
  2. wow, it's that easy!

## Export Data
 * *output.txt*
   * Graph [Graph Name]  
     top 5 nodes by cc: [List of values]  
     cc average value: [Int value]
  * *time.csv*
    *  [Graph Name], [Number of Nodes], [Elapsed Time to run CC]

## Other Notes
 * Uploaded sample_graph.txt for basic testing

 