#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: LiangTing
2023/12/18 12:06:31
"""
from pylab import *
import numpy as np
import seaborn as sns

## load data

## nep data
nep_graphite_stacking = loadtxt('hbn.data')

## DFT data
DFT_graphite_stacking = loadtxt('bulk_Hbn_exfoliation_curve.data')


#*************************** Set Seaborn style *************************
sns.set(style="ticks")

# Customize axis line, tick, and label properties
sns.set_context("paper", rc={"axes.linewidth": 0.65, "xtick.major.width": 0.65, "ytick.major.width": 0.65, 
	              "axes.labelsize": 15, "xtick.labelsize": 13.0, "ytick.labelsize": 13.0})
	              	
#*************************** Set Seaborn style ************************* 

figure(figsize=(5, 5))

lw=2.0
alpha=0.6

## AB
DFT_energies = DFT_graphite_stacking[:, 2] - DFT_graphite_stacking[49, 2]
nep_energies = nep_graphite_stacking[:, 1] -  nep_graphite_stacking[48, 1]

plot(DFT_graphite_stacking[:, 1], DFT_energies*1000, 'o', c="C2", label="PBE+MBD", markersize=7.0, alpha=0.5)
plot(nep_graphite_stacking[:, 0], nep_energies*1000, ls="-", lw=lw, c="C2", label="NEP", alpha=0.8)

xlim([4, 16])
ylim([-60, 100])
xlabel('Interlayer distance ($\mathrm{\AA}$)')
ylabel('Energy (meV/atom)')

title('Bulk $h$-BN', fontsize=15)
legend(loc="best", frameon=False, fontsize=13)

savefig("Hbn_curve.svg", bbox_inches='tight')
show()
