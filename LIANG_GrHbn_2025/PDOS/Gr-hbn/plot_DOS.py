#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: LiangTing
2024/7/1 22:43:25
"""
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from gpyumd.load import load_dos
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
hbn_dos = load_dos(num_dos_points=num_corr_steps, filename="hbn_dos.out")['run0']

gr_dos_in_plane = {}
gr_dos_cross_plane = {}
hbn_dos_in_plane = {}
hbn_dos_cross_plane = {}

gr_dos_in_plane['nu'] = gr_dos['nu']
gr_dos_in_plane['DOSxyz'] = gr_dos['DOSx'] + gr_dos['DOSy']
gr_dos_in_plane['DOSxyz'] /= np.max(gr_dos_in_plane['DOSxyz'])

gr_dos_cross_plane['nu'] = gr_dos['nu']
gr_dos_cross_plane['DOSxyz'] = gr_dos['DOSz']
gr_dos_cross_plane['DOSxyz'] /= np.max(gr_dos_cross_plane['DOSxyz'])

hbn_dos_in_plane['nu'] = hbn_dos['nu']
hbn_dos_in_plane['DOSxyz'] = hbn_dos['DOSx'] + hbn_dos['DOSy']
hbn_dos_in_plane['DOSxyz'] /= np.max(hbn_dos_in_plane['DOSxyz'])

hbn_dos_cross_plane['nu'] = hbn_dos['nu']
hbn_dos_cross_plane['DOSxyz'] = hbn_dos['DOSz']
hbn_dos_cross_plane['DOSxyz'] /= np.max(hbn_dos_cross_plane['DOSxyz'])

######################################## plot #######################################

def plot_overlap(ax, dos1, dos2, label1, label2, color1, color2, x_limits=None, y_limits=None, title_name=None):
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

fig, axes = plt.subplots(1, 2, figsize=(9, 5))

plot_overlap(axes[0], gr_dos_cross_plane, hbn_dos_cross_plane, 'Gr', '$h$-BN',
             'C4', 'C2', x_limits=[0, 30], y_limits=[0, 1.1], title_name="Out-of-plane")

plot_overlap(axes[1], gr_dos_in_plane, hbn_dos_in_plane, 'Gr', '$h$-BN',
             'C4', 'C2', x_limits=[0, 50], y_limits=[0, 1.1], title_name="In-plane")

fig.tight_layout()
fig.savefig("Gr-Hbn-PDOS.svg", bbox_inches='tight', dpi=800)

plt.show()
