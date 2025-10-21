#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: LiangTing
2024/7/1 22:43:25
"""
from pylab import *
import numpy as np
import seaborn as sns

# Load ITC data
ITC_Gr_Hbn_300K = loadtxt('count_data_Gr-Hbn_tersoff.data')

#*************************** Set Seaborn style *************************
sns.set(style="ticks")

# Customize axis line, tick, and label properties
sns.set_context("paper", rc={"axes.linewidth": 0.8, "xtick.major.width": 0.8, "ytick.major.width": 0.8, 
                             "axes.labelsize": 20, "xtick.labelsize": 18.0, "ytick.labelsize": 18.0})

#*************************** Set Seaborn style ************************* 

figure(figsize=(5, 5))
sns.histplot(ITC_Gr_Hbn_300K[:, 3], binwidth=4, bins=10, kde=False, color='C2', alpha=0.6, label = '300 K')

xlim([60, 130])
ylim([0, 8])

xlabel('$G$ (MWm$^{-2}$K$^{-1}$)')
ylabel('Counts')

title("Tersoff+ILP", fontsize=20)
legend(loc="best", frameon=False, fontsize=15)
sns.despine()

savefig("Counts_Tersoff_ILP.svg", bbox_inches='tight', dpi=800)

###########################################################################################

figure(figsize=(5, 5))
sns.histplot(ITC_Gr_Hbn_300K[:, 1], binwidth=4, bins=10, kde=False, color='C4', alpha=0.6, label = '300 K')

xlim([210, 290])
ylim([0, 6])

xlabel('$G$ (MWm$^{-2}$K$^{-1}$)')
ylabel('Counts')

title("Tersoff+LJ", fontsize=20)
legend(loc="best", frameon=False, fontsize=15)
sns.despine()

savefig("Counts_Tersoff_LJ.svg", bbox_inches='tight', dpi=800)

show()
