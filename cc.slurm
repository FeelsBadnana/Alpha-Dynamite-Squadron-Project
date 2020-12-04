#!/bin/bash
​
#SBATCH -p compute          # Submit to 'compute' Partition or queue
#SBATCH -J cc-batch-job          # Name the job as 'cc-batch-job'
#SBATCH -o cc-batch-job-%j.out   # Write the standard output to file named 'cc-batch-job-<job_number>.out'
#SBATCH -e cc-batch-job-%j.err   # Write the standard error to file named 'cc-batch-job-<job_number>.err'
#SBATCH -t 0-12:00:00        # Run for a maximum time of 0 days, 12 hours, 00 mins, 00 secs
#SBATCH --ntasks-per-node=1 # Request n cores or task per node
#SBATCH --mem-per-cpu=4000   # Request 4000MB (4GB) RAM per core
​
mpirun python main.py sample_graph.txt