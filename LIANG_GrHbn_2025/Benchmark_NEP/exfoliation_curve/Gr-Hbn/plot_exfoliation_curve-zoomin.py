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

## nep data for AB, AA, ABp 
nep_AB_stacking = loadtxt('AB-stacking/nep_bilayer_Gr-Hbn_AB.data')
nep_AA_stacking = loadtxt('AA-stacking/nep_bilayer_Gr-Hbn_AA.data')
nep_ABp_stacking = loadtxt('ABp_stacking/nep_bilayer_Gr-Hbn_ABp.data')

## DFT data for AB, AA, ABp 
DFT_AB_stacking = loadtxt('AB-stacking/Gr_HBn_AB_stacking_exfoliation_curve.data')
DFT_AA_stacking = loadtxt('AA-stacking/Gr_HBn_AA_stacking_exfoliation_curve.data')
DFT_ABp_stacking = loadtxt('ABp_stacking/Gr_HBn_ABp_stacking_exfoliation_curve.data')

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
AB_relative_DFT_energies = DFT_AB_stacking[:, 2] - DFT_AB_stacking[45, 2]
AB_relative_nep_energies = nep_AB_stacking[:, 1] -  nep_AB_stacking[44, 1]

plot(DFT_AB_stacking[:, 1], AB_relative_DFT_energies*1000, '^', c="C4", label="PBE+MBD (AB stacking)", markersize=7.0, alpha=0.5)
plot(nep_AB_stacking[:, 0], AB_relative_nep_energies*1000, ls="-", lw=lw, c="C4", label="NEP", alpha=0.8)
	
## AA
AA_relative_DFT_energies = DFT_AA_stacking[:, 2] - DFT_AA_stacking[45, 2]
AA_relative_nep_energies = nep_AA_stacking[:, 1] -  nep_AA_stacking[44, 1]

plot(DFT_AA_stacking[:, 1], AA_relative_DFT_energies*1000, 'D', c="C2", label="PBE+MBD (AA stacking)", markersize=7.0, alpha=0.5)
plot(nep_AA_stacking[:, 0], AA_relative_nep_energies*1000, ls="-", lw=lw, c="C2", label="NEP", alpha=0.8)

## ABp
ABp_relative_DFT_energies = DFT_ABp_stacking[:, 2] - DFT_ABp_stacking[45, 2]
ABp_relative_nep_energies = nep_ABp_stacking[:, 1] -  nep_ABp_stacking[44, 1]

plot(DFT_ABp_stacking[:, 1], ABp_relative_DFT_energies*1000, 'o', c="#BF4045", label="PBE+MBD (ABp stacking)", markersize=7.0, alpha=0.5)
plot(nep_ABp_stacking[:, 0], ABp_relative_nep_energies*1000, ls="-", lw=lw, c="#BF4045", label="NEP", alpha=0.8)


xlim([2.5, 5])
ylim([-30, -10])
xlabel('Interlayer distance ($\mathrm{\AA}$)')
ylabel('Energy (meV/atom)')

#title('Gr/$h$-BN heterostructure', fontsize=15)
#legend(loc="best", frameon=False, fontsize=13)

savefig("Gr-Hbn-Exfoliation_curve-zoomin.svg", bbox_inches='tight')
show()
