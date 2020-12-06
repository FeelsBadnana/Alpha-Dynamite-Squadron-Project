#!/bin/bash

#SBATCH -p compute          # Submit to 'compute' Partition or queue
#SBATCH -J twitter          # Name the job as 'cc-batch-job'
#SBATCH -o t1-%j.out   # Write the standard output to file named 'cc-batch-job-<job_number>.out'
#SBATCH -e t1-%j.err   # Write the standard error to file named 'cc-batch-job-<job_number>.err'
#SBATCH -t 1-12:00:00        # Run for a maximum time of 0 days, 24 hours, 00 mins, 00 secs
#SBATCH --ntasks-per-node=1 # Request n cores or task per node
#SBATCH --mem-per-cpu=32000   # Request 4000MB (4GB) RAM per core

mpirun -n 1 python main.py twitter_combined.txt
mpirun -n 4 python main.py twitter_combined.txt
mpirun -n 8 python main.py twitter_combined.txt
mpirun -n 16 python main.py twitter_combined.txt
mpirun -n 32 python main.py twitter_combined.txt
