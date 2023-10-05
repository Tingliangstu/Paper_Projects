#!/bin/sh

######################################################################################
startTime=`date +%Y%m%d-%H:%M`
startTime_s=`date +%s`
######################################################################################

DYNASOR=dynasor_cli

Q_MAX=10     		 # Consider qspace from gamma (0) to Q_MAX inverse nanometer
Q_BINS=200      	 # Collect result using Q_BINS "bins" between 0 and $Q_MAX
TIME_WINDOW=4000  	 # Consider time correlations up to TIME_WINDOW trajectory frames
MAX_FRAMES=20000   	 # Read at most MAX_FRAMES frames from trajectory file (then stop)
Num_KPOINT=5000          # Maximum number of points used to sample k-space. Default value is 20000.

dt=$((10*1)) # This needs to be correspond to lammps timestep * dumpFreq * $STEP in fs in order to get the units correct.

TRAJECTORY="../run_trajectory/movie.nc"
trajectory_format="netcdf"
OUTPUT="outputs/dynasor_T300_dynamical"

${DYNASOR} -f "$TRAJECTORY" -v \
	      --q-bins=$Q_BINS \
	      --q-max=$Q_MAX \
	      --max-q-points=$Num_KPOINT \
	      --max-frames=$MAX_FRAMES \
	      --time-window=$TIME_WINDOW \
	      --dt=$dt \
	      --om=$OUTPUT.m

####################################################################
endTime=`date +%Y%m%d-%H:%M`

endTime_s=`date +%s`

sumTime=$[$endTime_s - $startTime_s]

Hour=$[sumTime/3600]

echo "$startTime ---> $endTime" "Total:$Hour  hours"
####################################################################

