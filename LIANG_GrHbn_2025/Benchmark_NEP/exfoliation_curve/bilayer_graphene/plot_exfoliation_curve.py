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

## nep data for AB, AA
nep_AA_stacking = loadtxt('bilayer_graphene_AA/nep_bilayer_graphene_AA.data')
nep_AB_stacking = loadtxt('bilayer_graphene_AB/nep_bilayer_graphene_AB.data')

## DFT data for AB, AA 
DFT_AA_stacking = loadtxt('bilayer_graphene_AA/bilayer_Gr_AA_stacking_exfoliation_curve.data')
DFT_AB_stacking = loadtxt('bilayer_graphene_AB/bilayer_Gr_AB_stacking_exfoliation_curve.data')

#*************************** Set Seaborn style *************************
sns.set(style="ticks")

# Customize axis line, tick, and label properties
sns.set_context("paper", rc={"axes.linewidth": 0.65, "xtick.major.width": 0.65, "ytick.major.width": 0.65, 
	              "axes.labelsize": 15, "xtick.labelsize": 13.0, "ytick.labelsize": 13.0})
	              	
#*************************** Set Seaborn style ************************* 

figure(figsize=(5, 10))

lw=2.0
alpha=0.6

## AA
AA_relative_DFT_energies = DFT_AA_stacking[:, 2] - DFT_AA_stacking[45, 2]
AA_relative_nep_energies = nep_AA_stacking[:, 1] -  nep_AA_stacking[44, 1]

plot(DFT_AA_stacking[:, 1], AA_relative_DFT_energies*1000, '^', c="C4", label="PBE+MBD (AA stacking)", markersize=7.0, alpha=0.5)
plot(nep_AA_stacking[:, 0], AA_relative_nep_energies*1000, ls="-", lw=lw, c="C4", label="NEP", alpha=0.8)

## AB
AB_relative_DFT_energies = DFT_AB_stacking[:, 2] - DFT_AB_stacking[45, 2]
AB_relative_nep_energies = nep_AB_stacking[:, 1] -  nep_AB_stacking[44, 1]

plot(DFT_AB_stacking[:, 1], AB_relative_DFT_energies*1000, 'D', c="C2", label="PBE+MBD (AB stacking)", markersize=7.0, alpha=0.5)
plot(nep_AB_stacking[:, 0], AB_relative_nep_energies*1000, ls="-", lw=lw, c="C2", label="NEP", alpha=0.8)


xlim([2, 9])
ylim([-30, 80])
xlabel('Interlayer distance ($\mathrm{\AA}$)')
ylabel('Energy (meV/atom)')

title('Bilayer graphene', fontsize=15)
legend(loc="best", frameon=False, fontsize=13)

savefig("Bilayer-graphene.svg", bbox_inches='tight')
show()
