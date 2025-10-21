# -*- coding: utf-8 -*-
"""
Created on 2022/10/10 15:43:40
@author: Liang Ting
"""
import numpy as np
import seaborn as sns
from pylab import *
from mpl_toolkits.axes_grid1 import make_axes_locatable

def plot_sed(out_files_name, plot_cutoff_freq = None, plot_interval = 5, vmin = None, vmax = None, if_show_figures=True):
    
    # load data for draw
    sed_avg = np.loadtxt(out_files_name + '.SED')
    qpoints = np.loadtxt(out_files_name + '.Qpts')
    thz = np.loadtxt(out_files_name + '.THz')
    
    # load NEP
    nep_data = loadtxt('band_structure_ABp.txt')
    kpoint = loadtxt('qx_axis_data.txt')

    # ******************** Control plotting params ********************
    log = True
    color = 'RdBu_r'    # 'inferno', 'jet', 'Spectral', 'RdYlGn' (https://matplotlib.org/stable/tutorials/colors/colormaps.html)

    interp = 'hanning'    # 'hanning' or 'spline36'
    df = plot_interval    # Scale interval for drawing

    # For plot scale
    max_thz = max(thz)
    max_sed_y = np.size(sed_avg, 0)
    scale_factor = max_sed_y / max_thz

    # ******************** Whether to apply log scaling data ********************
    if log:
        sed_avg = np.log(sed_avg)

    ### ******************** Creat a figure, set its size ********************
    fig, ax = plt.subplots()
    fig.set_size_inches(4, 4.5, forward=True)       # Control the size of the output image
    fig.tight_layout(pad=6)
    
    if not vmin:
        vmin = np.trunc(sed_avg.min())
    if not vmax:
        vmax = np.trunc(sed_avg.max())

    print('********* The vmin = {} and vmax = {} *********'.format(vmin, vmax))
    
    #*************************** Set Seaborn style *************************
    sns.set(style="ticks")
    # Customize axis line, tick, and label properties
    sns.set_context("paper", rc={"axes.linewidth": 0.8, "xtick.major.width": 0.8, "ytick.major.width": 0.8, 
                     "axes.labelsize": 23, "xtick.labelsize": 20.0, "ytick.labelsize": 20.0})
                     	
    #*************************** Set Seaborn style ************************* 
    
    # Plot colormap
    im = ax.imshow(sed_avg, cmap=color, interpolation=interp, aspect='auto', origin='lower', vmax=vmax, vmin=vmin)
    
    # colarbar
    ticks = np.arange(vmin, vmax+2, 2)
    bar = fig.colorbar(im, ax=ax)
    bar.set_ticks(ticks)
    bar.set_ticklabels([str(int(t)) for t in ticks])
    
    bar.outline.set_visible(False)
    bar.ax.tick_params(labelsize=8, width=0, length=0, pad=0.65)
    
    bar.set_label(r'log($\Phi$($\mathbf{q}$, $\omega$)) (J s)', fontsize=12)
    
    # Secondary y-axis for band structure
    scale_factor_nep_k = len(qpoints) / max(nep_data[:, 0])
    scale_factor_nep_feq = len(thz) / max(thz)

    ax.plot(nep_data[:, 0]*scale_factor_nep_k-0.5, nep_data[:, 1:]*scale_factor_nep_feq, color="grey",
    	                                            linestyle="-", lw=1.0, label="Lattice Dynamic", alpha=0.6)
    	                                            
    
    ## Set xticks
    xticks = [-0.5, len(qpoints)-0.5]
    ax.set_xticks(xticks)
    ax.set_xticklabels([r'$\Gamma$', r'A'], fontsize=12.5)
    
    # yticks
    freqs = np.arange(0, thz.max(), df)
    nf = len(freqs)
    ids = np.zeros(nf)
    for i in range(nf):
        ids[i] = np.argwhere(thz <= freqs[i]).max()
        
    ax.set_yticks(ids)
    ax.tick_params(which='major', length=4)                        
    ax.set_yticklabels(list(map(lambda x: str(int(x)), freqs)))
    	
    ax.set_ylabel('Frequency (THz)', fontsize=13)
    
    title("ABp stacking", fontsize=13) 
    
    if plot_cutoff_freq:
        ax.set_ylim([0, plot_cutoff_freq * scale_factor])
    
    savefig('{}-SED.svg'.format(out_files_name), format='svg', dpi = 1200, bbox_inches='tight')

    if if_show_figures:
        plt.show()

if __name__ == "__main__":

    out_files_name = 'Gr-Hbn-ABp'
    plot_cutoff_freq = 5               # THz
    plot_interval = 1                  # THz
    vmax = -8                          # For SED image (high)
    vmin = -20                         # For SED image (low)

    plot_sed(out_files_name, plot_cutoff_freq, plot_interval, vmin=vmin, vmax=vmax)

    print('************** ALL DONE !!! **************')
