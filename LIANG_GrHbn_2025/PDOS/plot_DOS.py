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
from scipy.interpolate import interp1d

################################ Plot ###################################
#*************************** Set Seaborn style *************************
sns.set(style="ticks")

# Customize axis line, tick, and label properties
sns.set_context("paper", rc={"axes.linewidth": 0.8, "xtick.major.width": 0.8, "ytick.major.width": 0.8,
                             "axes.labelsize": 18, "xtick.labelsize": 16.0, "ytick.labelsize": 16.0})

################################ load data ###############################
num_corr_steps = 500
gr_dos = load_dos(num_dos_points=num_corr_steps, filename="gr_dos.out")['run0']
gr_dos['DOSxyz'] = gr_dos['DOSx']+gr_dos['DOSy']+gr_dos['DOSz']
gr_dos['DOSxyz'] /= np.max(gr_dos['DOSxyz']) 

hbn_dos = load_dos(num_dos_points=num_corr_steps, filename="hbn_dos.out")['run0']
hbn_dos['DOSxyz'] = hbn_dos['DOSx']+hbn_dos['DOSy']+hbn_dos['DOSz']
hbn_dos['DOSxyz'] /= np.max(hbn_dos['DOSxyz'])

MoS2_dos = load_dos(num_dos_points=num_corr_steps, filename="MoS2_dos.out")['run0']
MoS2_dos['DOSxyz'] = MoS2_dos['DOSx']+MoS2_dos['DOSy']+MoS2_dos['DOSz']
MoS2_dos['DOSxyz'] /= np.max(MoS2_dos['DOSxyz'])

WS2_dos = load_dos(num_dos_points=num_corr_steps, filename="WS2_dos.out")['run0']
WS2_dos['DOSxyz'] = WS2_dos['DOSx']+WS2_dos['DOSy']+WS2_dos['DOSz']
WS2_dos['DOSxyz'] /= np.max(WS2_dos['DOSxyz']) 

WSe2_dos = load_dos(num_dos_points=num_corr_steps, filename="WSe2_dos.out")['run0']
WSe2_dos['DOSxyz'] = WSe2_dos['DOSx']+WSe2_dos['DOSy']+WSe2_dos['DOSz']
WSe2_dos['DOSxyz'] /= np.max(WSe2_dos['DOSxyz']) 

######################################## plot #######################################

def plot_overlap(ax, dos1, dos2, label1, label2, color1, color2, x_limits=None, y_limits=None):
    # Interpolate dos2 to dos1['nu']
    interp_dos2 = interp1d(dos2['nu'], dos2['DOSxyz'], kind='linear', bounds_error=False, fill_value=0)
    dos2_interp_values = interp_dos2(dos1['nu'])

    ax.plot(dos1['nu'], dos1['DOSxyz'], label=label1, color=color1, alpha=0.7, linewidth=1.8)
    ax.plot(dos1['nu'], dos2_interp_values, label=label2, color=color2, alpha=0.7, linewidth=1.8)

    min_values = np.minimum(dos1['DOSxyz'], dos2_interp_values)
    ax.fill_between(dos1['nu'], min_values, color='yellow', alpha=0.3)

    overlap_area = np.trapz(min_values, dos1['nu'])
    ax.set_title(r"{}/{} overlap area = {:.2f}".format(label1, label2, overlap_area), fontsize=18)

    if x_limits:
        ax.set_xlim(x_limits)
    if y_limits:
        ax.set_ylim(y_limits)
    
    ax.set_ylabel('PDOS (Normalized)')
    ax.set_xlabel('Frequency (THz)')
    ax.legend(loc="best", frameon=False, fontsize=15.5)

fig, axes = plt.subplots(2, 4, figsize=(18, 10))

plot_overlap(axes[0, 0], gr_dos, hbn_dos, 'Gr', '$h$-BN', 'C4', 'C2', x_limits=[0, 50], y_limits=[0, 1.1])
plot_overlap(axes[0, 2], hbn_dos, MoS2_dos, '$h$-BN', r'MoS$_2$', 'C4', 'C2', x_limits=[0, 50], y_limits=[0, 1.1])
plot_overlap(axes[0, 1], gr_dos, MoS2_dos, 'Gr', r'MoS$_2$', 'C4', '#BF4045', x_limits=[0, 50], y_limits=[0, 1.1])
plot_overlap(axes[0, 3], MoS2_dos, WSe2_dos, r'MoS$_2$', r'WSe$_2$', 'C4', 'C6', x_limits=[0, 20], y_limits=[0, 1.1])
plot_overlap(axes[1, 0], hbn_dos, WSe2_dos, '$h$-BN', r'WSe$_2$', 'C2', 'C6', x_limits=[0, 50], y_limits=[0, 1.1])
plot_overlap(axes[1, 2], gr_dos, WSe2_dos, 'Gr', r'WSe$_2$', '#BF4045', 'grey', x_limits=[0, 50], y_limits=[0, 1.1])
plot_overlap(axes[1, 1], hbn_dos, WS2_dos, '$h$-BN', r'WS$_2$', 'C2', 'grey', x_limits=[0, 50], y_limits=[0, 1.1])
plot_overlap(axes[1, 3], WS2_dos, WSe2_dos, r'WS$_2$', r'WSe$_2$', 'grey', 'C6', x_limits=[0, 20], y_limits=[0, 1.1])

fig.tight_layout()

fig.savefig("PDOS.svg", bbox_inches='tight', dpi=800)


plt.show()
