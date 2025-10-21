#!/bin/bash
#SBATCH -J Full_4099 
#SBATCH -p gpu
#SBATCH -N 1
#SBATCH -n 1
#SBATCH -G 1
#SBATCH -o out_%J.log
#SBATCH -e err_%J.log

# CUDA
export CUDA_HOME=/usr/local/cuda/
export PATH=${CUDA_HOME}/bin:$PATH
export LD_LIBRARY_PATH=${CUDA_HOME}/lib64:$LD_LIBRARY_PATH
# GCC
export PATH=/share/home/penghuaying/LT/gcc/gcc-9.1.0/gcc-build-9.1.0/bin:/share/home/penghuaying/LT/gcc/gcc-9.1.0/gcc-build-9.1.0/lib64:$PATH
export LD_LIBRARY_PATH=/share/home/penghuaying/LT/gcc/gcc-9.1.0/gcc-build-9.1.0/lib64/:$LD_LIBRARY_PATH

PROGRAM=/share/home/penghuaying/LT/GPUMD-3.8/src/nep

$PROGRAM

