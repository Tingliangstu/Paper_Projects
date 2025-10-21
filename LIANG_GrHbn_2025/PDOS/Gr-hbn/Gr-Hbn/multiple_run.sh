#!/bin/bash

set -e


for i  in {1..3}
do   
   mkdir  ${i}
   
   cd     ${i}
   
   cp -r  ../run_files/run.sh run.sh
   cp -r  ../run_files/nep.txt nep.txt
   
   cp -r  ../run_files/model.xyz model.xyz
   
   cp -r  ../run_files/run.in  run.in
   
   echo "Move file to ${i} done !!!"
   
   bash run.sh 
   
   echo "Submitted done !!!"
   
   wait
   
   echo ""
   echo "************** Finish ${i} GPUMD *********************"
   echo ""

   cd  ..
   
done

