#!/bin/bash
#{pre_tell existence of a regular file

set -e 
set -u

file_name="bilayer_Gr_AA_stacking_exfoliation_curve.data"

if [ -f $file_name ]
then
   rm $file_name
   echo -e "\nthe old file:[$file_name] removed. \n"
fi

for i in  2.0 2.1 2.2 2.3 2.4 2.5 2.6 2.7 2.8 2.9 3.0	3.1	3.2	3.3 3.4 3.5	3.6	3.7	3.8	3.9	4.0	4.1	4.2	4.3	4.4	4.5	4.6	4.7	4.8	4.9	5.0	5.1	5.2	5.3	5.4	5.5	5.6	5.7	5.8	5.9	6.0 7.0 8.0 9.0 10.0 11.0 12.0 13.0 14.0 15.0
do
	#super size in z-axis

	read_dire="bilayer_graphene_AA_distances_${i}"
	
	N1=$(sed -n '7p' $read_dire/POSCAR | awk '{print $1}')
	#N2=$(sed -n '7p' $read_dire/POSCAR | awk '{print $2}')
	
	#N_total=$(echo "scale=3;$N1 + $N2" |bc)
	
	echo "It have $N1 atoms in this POSCAR"
	
	ener_per_atom=$(grep "free  energy   TOTEN" $read_dire/OUTCAR | tail -1 | awk '{print $5 / '$N1'}')
	
	layer_distance=$(echo "scale=3; $i * 1.0" |bc)
	
	echo "$i	$layer_distance		$ener_per_atom" >> $file_name
	echo "$read_dire done, next ..."
	
	grep "free  energy   TOTEN"  $read_dire/OUTCAR
	
done
echo "all done, bye"
