from pylab import *
from scipy import interpolate
from ase.io import read
from calorine.calculators import CPUNEP
from dpdata import LabeledSystem,MultiSystems
from glob import glob
      
"""
process multi systems using dpdata
"""
def plot_sliding(nep_path, plot_path):
    # calc = CPUNEP("../../../Train/train_21_cutoff_10_4_lj/nep.txt")
    # print(calc)
    calc = CPUNEP(nep_path)
    fns = lambda s: [(s,int(n))for s,n in re.findall('(\D+)(\d+)','a%s0'%s)]


    def vasp2dp(infile):
        fs = glob(infile)
        ms_train=MultiSystems()
        fs = sorted(fs, key=fns)
        for f in fs:
            try:
                ls=LabeledSystem(f, fmt = 'vasp/outcar')
            except:
                print(f)
            if len(ls)>0:
                ms_train.append(ls[-1])
        return ms_train
        
    ms_train = vasp2dp("./SCF/OUTCAR-POSCAR_slip*")
    dft_energy = ms_train[0].data['energies']/ms_train[0].data['atom_numbs']
    dft_energy = (dft_energy - min(dft_energy)) * 1000 #unit in meV/atom

    nep_energy = []
    for i in range(len(ms_train[0])):
        atom = ms_train[0][i].to_ase_structure()[0]
        atom.calc = calc
        nep_energy.append(atom.get_potential_energy() / len(atom.positions))
    nep_energy = (np.array(nep_energy) - min(nep_energy)) * 1000 #unit in meV/atom

    ilp_energy = loadtxt("./ILP_results/Sliding_energy_ilp.txt")
    # np.savetxt("Sliding_energy_dft.txt", dft_energy, 
    #            delimiter = "\t",
    #            fmt="%10.5f", 
    #            header ="Energy (meV/atom)")
    # np.savetxt("Sliding_energy_nep.txt", nep_energy, 
    #            delimiter = "\t",
    #            fmt="%10.5f", 
    #            header ="Energy (meV/atom)")
    # ilp_energy = loadtxt("Sliding_energy_ilp.txt")
        
    # Set figure properties
    aw = 1.5
    fs = 16
    lw = 2
    font = {'size': fs}
    matplotlib.rc('font', **font)
    matplotlib.rc('axes', lw=aw)


    def set_fig_properties(ax_list):
        tl = 6
        tw = 1.5
        tlm = 3

        for ax in ax_list:
            ax.tick_params(which='major', length=tl, width=tw)
            ax.tick_params(which='minor', length=tlm, width=tw)
            ax.tick_params(which='both', axis='both', direction='out', right=False, top=False)


    ddx = 0.2463
    ddy = 0.4265
    xstep = 21
    ystep = 21
    extent = 0, ddx*xstep, 0, ddy*ystep
    x = np.linspace(0, ddx*(xstep-1), xstep)
    y = np.linspace(0, ddy*(ystep-1), ystep)
    X, Y = np.meshgrid(x, y)


    figure(figsize=(12, 10))
    subplot(2, 3, 1)
    set_fig_properties([gca()])
    DFT_map = dft_energy.reshape((21, 21), order="F")
    im1 = imshow(DFT_map, 
                  extent=extent, 
                  cmap=plt.cm.bwr, 
                  alpha=.9, 
                  interpolation='bilinear',              
                  origin='lower')
    cbar1 = colorbar(im1)
    # cbar1.set_label('Energy (meV/atom)')
    C = contour(X, Y, DFT_map, 10,  colors="grey", linestyles="--")
    clabel(C, inline=True, fontsize=10)
    xlabel(r'$x$ Shift ($\mathrm{\AA}$)')  
    ylabel(r'$y$ Shift ($\mathrm{\AA}$)')
    title("(a) PBE-MBD", fontsize=16)

    subplot(2, 3, 2)
    set_fig_properties([gca()])
    NEP_map = nep_energy.reshape((21, 21), order="F")
    im2 = imshow(NEP_map, 
                  extent=extent, 
                  cmap=plt.cm.bwr, 
                  alpha=.9, 
                  interpolation='bilinear',              
                  origin='lower')
    cbar2 = colorbar(im2)
    # cbar2.set_label('Energy (meV/atom)')
    C = contour(X, Y, NEP_map, 10,  colors="grey", linestyles="--")
    clabel(C, inline=True, fontsize=10)
    xlabel(r'$x$ Shift ($\mathrm{\AA}$)')  
    # ylabel(r'$y$ Shift ($\mathrm{\AA}$)')
    title("(b) NEP", fontsize=16)

    subplot(2, 3, 3)
    set_fig_properties([gca()])
    ILP_map = ilp_energy.reshape((21, 21), order="F")
    im3 = imshow(ILP_map, 
                  extent=extent, 
                  cmap=plt.cm.bwr, 
                  alpha=.9, 
                  interpolation='bilinear', 
                  origin='lower')
    cbar3 = colorbar(im3)
    C = contour(X, Y, ILP_map, 10,  colors="grey", linestyles="--")
    clabel(C, inline=True, fontsize=10)
    cbar3.set_label('Energy (meV/atom)')
    xlabel(r'X Shift ($\mathrm{\AA}$)')  
    # ylabel(r'Y Shift ($\mathrm{\AA}$)')
    title("(c) ILP", fontsize=16)

    subplot(2, 3, 4)
    set_fig_properties([gca()])
    im4 = imshow(NEP_map-DFT_map, 
                  extent=extent, 
                  cmap=plt.cm.bwr, 
                  alpha=.9, 
                  interpolation='bilinear',              
                  origin='lower')
    cbar4 = colorbar(im4)
    # cbar4.set_label('Energy (meV/atom)')
    C = contour(X, Y, NEP_map-DFT_map, 5,  colors="grey", linestyles="--")
    clabel(C, inline=True, fontsize=10)
    xlabel(r'$x$ Shift ($\mathrm{\AA}$)')  
    # ylabel(r'$y$ Shift ($\mathrm{\AA}$)')
    title("(e) NEP versus PBE-MBD", fontsize=16)

    subplot(2, 3, 5)
    set_fig_properties([gca()])
    im5 = imshow(NEP_map-ILP_map, 
                  extent=extent, 
                  cmap=plt.cm.bwr, 
                  alpha=.9, 
                  interpolation='bilinear',              
                  origin='lower')
    cbar5 = colorbar(im5)
    # cbar5.set_label('Energy (meV/atom)')
    C = contour(X, Y, NEP_map-ILP_map, 5,  colors="grey", linestyles="--")
    clabel(C, inline=True, fontsize=10)
    xlabel(r'$x$ Shift ($\mathrm{\AA}$)')  
    # ylabel(r'$y$ Shift ($\mathrm{\AA}$)')
    title("(f) NEP versus ILP", fontsize=16)

    subplot(2, 3, 6)
    set_fig_properties([gca()])
    im6 = imshow(ILP_map-DFT_map, 
                  extent=extent, 
                  cmap=plt.cm.bwr, 
                  alpha=.9, 
                  interpolation='bilinear',              
                  origin='lower')
    cbar6 = colorbar(im6)
    cbar6.set_label('Energy (meV/atom)')
    C = contour(X, Y, ILP_map-DFT_map, 5,  colors="grey", linestyles="--")
    clabel(C, inline=True, fontsize=10)
    xlabel(r'$x$ Shift ($\mathrm{\AA}$)')  
    # ylabel(r'$y$ Shift ($\mathrm{\AA}$)')
    title("(g) ILP versus PBE-MBD", fontsize=16)

    subplots_adjust(wspace=0.1, hspace=0.3)
    savefig(plot_path, dpi=300, bbox_inches='tight')

# plot_sliding("../../../Train/train_20_cutoff_10_4/nep.txt", "./Sliding_energy_train20.png")
# plot_sliding("../../../Train/train_21_cutoff_10_4_lj/nep.txt", "./Sliding_energy_train21.png")
# plot_sliding("../../../Train/train_27_cutoff_8_4_nmax_12_12_basis_15_15_neuron_80_no_weight_no_virial_for_defect/nep.txt", "./Sliding_energy_train27.png")
# plot_sliding("../../../Train/train_28_cutoff_8_4_ForceDelta_1/nep.txt", "./Sliding_energy_train28.png")
plot_sliding("../../../Train/train_29_weight_5/nep.txt", "./Sliding_energy_train29.png")