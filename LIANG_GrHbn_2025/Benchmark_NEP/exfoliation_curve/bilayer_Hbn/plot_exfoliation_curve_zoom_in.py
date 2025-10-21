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
nep_AA_stacking = loadtxt('AA_stacking/nep_bilayer_hbn_AA.data')
nep_AAp_stacking = loadtxt('AAp_stacking/nep_bilayer_hbn_AAp.data')
nep_AB_stacking = loadtxt('AB_stacking/nep_bilayer_hbn_AB.data')
nep_ABp_stacking = loadtxt('ABp_stacking/nep_bilayer_hbn_ABp.data')
nep_ApB_stacking = loadtxt('ApB_stacking/nep_bilayer_hbn_ApB.data')

## DFT data for AB, AA, ABp 
DFT_AA_stacking = loadtxt('AA_stacking/bilayer_Hbn_AA_stacking_exfoliation_curve.data')
DFT_AAp_stacking = loadtxt('AAp_stacking/bilayer_Hbn_AAp_stacking_exfoliation_curve.data')
DFT_AB_stacking = loadtxt('AB_stacking/bilayer_Hbn_AB_stacking_exfoliation_curve.data')
DFT_ABp_stacking = loadtxt('ABp_stacking/bilayer_Hbn_ABp_stacking_exfoliation_curve.data')
DFT_ApB_stacking = loadtxt('ApB_stacking/bilayer_Hbn_ApB_stacking_exfoliation_curve.data')

#*************************** Set Seaborn style *************************
sns.set(style="ticks")

# Customize axis line, tick, and label properties
sns.set_context("paper", rc={"axes.linewidth": 0.8, "xtick.major.width": 0.8, "ytick.major.width": 0.8, 
	              "axes.labelsize": 20, "xtick.labelsize": 20.0, "ytick.labelsize": 20.0})
	              	
#*************************** Set Seaborn style ************************* 

figure(figsize=(8, 5))

lw=2.0
alpha=0.6

## AA
AA_relative_DFT_energies = DFT_AA_stacking[:, 2] - DFT_AA_stacking[45, 2]
AA_relative_nep_energies = nep_AA_stacking[:, 1] -  nep_AA_stacking[44, 1]

plot(DFT_AA_stacking[:, 1], AA_relative_DFT_energies*1000, '^', c="C4", label="PBE+MBD (AA stacking)", markersize=7.0, alpha=0.5)
plot(nep_AA_stacking[:, 0], AA_relative_nep_energies*1000, ls="-", lw=lw, c="C4", label="NEP", alpha=0.8)
	
## AAp
AAp_relative_DFT_energies = DFT_AAp_stacking[:, 2] - DFT_AAp_stacking[45, 2]
AAp_relative_nep_energies = nep_AAp_stacking[:, 1] -  nep_AAp_stacking[44, 1]

plot(DFT_AAp_stacking[:, 1], AAp_relative_DFT_energies*1000, 'x', c="k", label="PBE+MBD (AAp stacking)", markersize=8.0, alpha=0.5)
plot(nep_AAp_stacking[:, 0], AAp_relative_nep_energies*1000, ls="-", lw=lw, c="k", label="NEP", alpha=0.5)

## AB
AB_relative_DFT_energies = DFT_AB_stacking[:, 2] - DFT_AB_stacking[45, 2]
AB_relative_nep_energies = nep_AB_stacking[:, 1] -  nep_AB_stacking[44, 1]

plot(DFT_AB_stacking[:, 1], AB_relative_DFT_energies*1000, 'D', c="#BF4045", label="PBE+MBD (AB stacking)", markersize=7.0, alpha=0.5)
plot(nep_AB_stacking[:, 0], AB_relative_nep_energies*1000, ls="-", lw=lw, c="#BF4045", label="NEP", alpha=0.8)
	
## ABp
ABp_relative_DFT_energies = DFT_ABp_stacking[:, 2] - DFT_ABp_stacking[45, 2]
ABp_relative_nep_energies = nep_ABp_stacking[:, 1] -  nep_ABp_stacking[44, 1]

plot(DFT_ABp_stacking[:, 1], ABp_relative_DFT_energies*1000, 'o', c="#345384", label="PBE+MBD (ABp stacking)", markersize=7.0, alpha=0.5)
plot(nep_ABp_stacking[:, 0], ABp_relative_nep_energies*1000, ls="-", lw=lw, c="#345384", label="NEP", alpha=0.8)
	
## ApB
ApB_relative_DFT_energies = DFT_ApB_stacking[:, 2] - DFT_ApB_stacking[45, 2]
ApB_relative_nep_energies = nep_ApB_stacking[:, 1] -  nep_ApB_stacking[44, 1]

plot(DFT_ApB_stacking[:, 1], ApB_relative_DFT_energies*1000, 's', c="C2", label="PBE+MBD (ApB stacking)", markersize=7.0, alpha=0.5)
plot(nep_ApB_stacking[:, 0], ApB_relative_nep_energies*1000, ls="-", lw=lw, c="C2", label="NEP", alpha=0.8)


xlim([2.5, 5.5])
ylim([-30, -5])
xlabel('Interlayer distance ($\mathrm{\AA}$)')
ylabel('Energy (meV/atom)')

#title('Bilayer $h$-BN', fontsize=15)
#legend(loc="best", frameon=False, fontsize=13)

savefig("Bilayer-Hbn-zoom-in.svg", bbox_inches='tight')
show()
