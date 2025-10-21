#!/bin/bash
read_file="bilayer_graphene_AA_Cartesian.POSCAR"

echo "You are processing the $read_file"

for i in 2.9	3.0	3.1	3.2	3.3 3.4 3.5	3.6	3.7	3.8	3.9	4.0	4.1	4.2	4.3	4.4	4.5	4.6	4.7	4.8	4.9	5.0	5.1	5.2	5.3	5.4	5.5	5.6	5.7	5.8	5.9	6.0 7.0 8.0 9.0 10.0 11.0 12.0 13.0 14.0 15.0
do
   # super size in z axis 
   dire_name="bilayer_graphene_AA_distances_${i}"
   mkdir $dire_name
   
   # Got POTCAR and INCAR POSCAR
   cp $read_file $dire_name/POSCAR
   cp INCAR POTCAR run.sh $dire_name 
      
   # Enter directory and modify POSCAR's cz
   cd $dire_name
   
   unit_cz=$(sed -n '9p' POSCAR | awk '{printf "%.2f\n", $3}')
   
   z_number=$(echo "scale=3;$unit_cz + $i" |bc)
   
   sed -i "11s/12.0/${z_number}/g" POSCAR
   sed -i "12s/12.0/${z_number}/g" POSCAR
    
   # Rename job's name
   sed  -i  "2s/MoS2-test/${i}/g"  run.sh

   # Run
   yhbatch  -N  2  -n 48  run.sh
   
   sleep 0.5s    
   cd ..

   echo "$dire_name done, next ..."

done
echo "all done, bye"



