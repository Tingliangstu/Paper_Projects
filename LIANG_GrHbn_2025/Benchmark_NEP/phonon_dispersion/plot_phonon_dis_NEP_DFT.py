#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: LiangTing
2021/12/18 12:06:31
"""
from pylab import *
import numpy as np

aw = 1.5
fs = 8
font = {'size': fs}
matplotlib.rc('font', **font)
matplotlib.rc('axes', linewidth=aw)

def set_fig_properties(ax_list):
    tl = 4
    tw = 2
    tlm = 2

    for ax in ax_list:
        ax.tick_params(which='major', length=tl, width=tw)
        ax.tick_params(which='minor', length=tlm, width=tw)
        ax.tick_params(which='both', axis='both', direction='in', right=True, top=True)

def get_exp_data():

    file = 'quartz.txt'
    data = np.loadtxt(file)
    return data

def plot_dispersion(potential):

    # load exp data
    data_exp = get_exp_data()
    nep_data = []
    # load nep data
    for i, name in enumerate(potential):
        name = name + '.npz'
        nep_data.append(np.load(name))

    figure(figsize=(4, 4))
    fontsizes = 12
    set_fig_properties([gca()])

    error_attri = dict(elinewidth=2, ecolor="grey", capsize=3)

    # For nep data
    errorbar(-data_exp[:, 0]+2.0340986411447686, data_exp[:, 1], yerr=data_exp[:, 4], fmt='o', elinewidth=1.5, markersize=4.0,
             color='grey', label="Expt.", capsize=3, capthick=1, zorder=0)

    vlines(nep_data[0]['special_k'], ymin=-0.2, ymax=20, linestyle="--", colors="gray")
    hlines(0, xmin=-0.2, xmax=20, linestyle="--", colors="gray")

    # For nep data
    color_1 = [0.64, 0.08, 0.18]
    for i, name in enumerate(potential):
        plot(nep_data[i]['kpoint'], nep_data[i]['omega'][:, 0], color=color_1, linestyle="-", lw=1.5, label='NEP')
        plot(nep_data[i]['kpoint'], nep_data[i]['omega'][:, 1:], color=color_1, linestyle="-", lw=1.5)

    # labels set
    gca().set_xticks(nep_data[0]['special_k'])
    gca().set_xticklabels([r'$\Gamma$', 'M', 'K', r'$\Gamma$'], fontsize=fontsizes, fontfamily='serif')
    gca().set_yticklabels(linspace(0, 8, 5).astype(int), fontsize=fontsizes, fontfamily='serif')
    xlim([0, max(nep_data[0]['kpoint'])])
    ylim([-0.2, 8])
    gca().set_yticks(linspace(0, 8, 5))
    ylabel('Frequency (THz)', fontsize=fontsizes, fontfamily='serif')
    font = {'family': 'serif', 'size': fontsizes}

    legend(frameon=False, loc="best", prop=font)
    title("Alpha-quartz", fontsize=14, fontfamily='serif')
    savefig("Alpha-quartz.svg", bbox_inches='tight')
    show()


if __name__ == "__main__":

    #compare_pot = ['GAP', 'nep_Full_Batch_6_4_2348_v-0.1_neu-80-12-8', 'nep_6_4_3074_v-0.1_neu-80', 'nep_6_4_2348_v-0.1_neu-80', 'nep_Batch_6_4_2348_v-0.1_neu-80-12-8-without-virials']

    compare_pot = ['nep_Batch_6_4_2348_calorine']
    plot_dispersion(compare_pot)

    print('******************** All Done !!! *************************')
