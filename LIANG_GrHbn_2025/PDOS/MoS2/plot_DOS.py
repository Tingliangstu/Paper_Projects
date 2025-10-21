#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: LiangTing
2024/7/1 22:43:25
"""
from pylab import *
import numpy as np
import seaborn as sns
from gpyumd.load import load_dos, load_vac

################################ Plot ###################################
#*************************** Set Seaborn style *************************
sns.set(style="ticks")

# Customize axis line, tick, and label properties
sns.set_context("paper", rc={"axes.linewidth": 0.8, "xtick.major.width": 0.8, "ytick.major.width": 0.8,
                             "axes.labelsize": 20, "xtick.labelsize": 18.0, "ytick.labelsize": 18.0})

################################ load data ###############################
num_corr_steps = 500
dos = load_dos(num_dos_points=num_corr_steps)['run0']
vac = load_vac(num_corr_steps)['run0']
dos['DOSxyz'] = dos['DOSx']+dos['DOSy']+dos['DOSz']
vac['VACxyz'] = vac['VACx']+vac['VACy']+vac['VACz']
vac['VACxyz'] /= vac['VACxyz'].max()


figure(figsize=(8,8))

plot(dos['nu'], dos['DOSx'], color='C3',linewidth=3)
plot(dos['nu'], dos['DOSy'], color='C0', linestyle='--',linewidth=3)
plot(dos['nu'], dos['DOSz'], color='C2', linestyle='-.',zorder=100, linewidth=3)
xlim([0, 20])
gca().set_xticks(range(0,20,5))
ylim([0, 10000])
gca().set_yticks(np.arange(0,1501,500))
ylabel('PDOS (1/THz)')
xlabel(r'$\nu$ (THz)')
legend(['x','y', 'z'])
show()