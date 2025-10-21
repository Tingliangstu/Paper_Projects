#!/bin/bash
#SBATCH -J DW
#SBATCH -p amd_512
#SBATCH -N 1
#SBATCH -n 48
#SBATCH -o out.%J
#SBATCH -e err.%J

module load mpi/intel/2022.1
PROGRAM=/public3/home/scg9538/software/VASP/vasp.6.3.0/bin/vasp_std_3D

mpirun  $PROGRAM
        
