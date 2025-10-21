from pylab import *
import seaborn as sns
from scipy import interpolate
from ase.io import read
from calorine.calculators import CPUNEP
from dpdata import LabeledSystem,MultiSystems
from glob import glob
from mpl_toolkits.axes_grid1 import make_axes_locatable
    

def vasp2dp(infile):
    fs = glob(infile)
    ms_train=MultiSystems()
    fns = lambda s: [(s,int(n))for s,n in re.findall('(\D+)(\d+)','a%s0'%s)]
    fs = sorted(fs, key=fns)
    
    for f in fs:
        try:
            ls=LabeledSystem(f, fmt = 'vasp/outcar')
        except:
            print(f)
        if len(ls)>0:
            ms_train.append(ls[-1])
         
    return ms_train

def sliding(path): 
	       
    calc = CPUNEP("nep.txt")
    ms_train = vasp2dp(path + "/SCF/OUTCAR-POSCAR_slip*")
    print("Totally got {0} frames for {1}".format(len(ms_train[0]), path))   
    dft_energy = ms_train[0].data['energies']/sum(ms_train[0].data['atom_numbs'])
    dft_energy = (dft_energy - min(dft_energy)) * 1000   # unit in meV/atom

    nep_energy = []
    for i in range(len(ms_train[0])):
        atom = ms_train[0][i].to_ase_structure()[0]
        atom.calc = calc
        nep_energy.append(atom.get_potential_energy() / len(atom.positions))
    nep_energy = (np.array(nep_energy) - min(nep_energy)) * 1000 #unit in meV/atom
    np.save(f"{path}_dft.npy", dft_energy)
    np.save(f"{path}_nep.npy", nep_energy)
    return dft_energy, nep_energy

# Get data if need
#grbn_dft, grbn_nep = sliding("Gr_Gr")
#bnbn_dft, bnbn_nep = sliding("hBN_hBN")
#grbn_dft, grbn_nep = sliding("Gr_hBN")

# Load data

grbn_dft = np.load("gr_hBN_dft.npy")
grbn_nep = np.load("gr_hBN_nep.npy")

#*************************** Set Seaborn style *************************
sns.set(style="ticks")

# Customize axis line, tick, and label properties
sns.set_context("paper", rc={"axes.linewidth": 0.8, "xtick.major.width": 0.8, "ytick.major.width": 0.8, 
    	                         "axes.labelsize": 20, "xtick.labelsize": 18.0, "ytick.labelsize": 18.0})
	              	
#*************************** Set Seaborn style ************************* 

ddx = 1
ddy = np.sqrt(3)
xstep = 21
ystep = 21
extent = 0, ddx*xstep, 0, ddy*ystep
x = np.linspace(0, ddx*(xstep-1), xstep)
y = np.linspace(0, ddy*(ystep-1), ystep)
X, Y = np.meshgrid(x, y)

############################# Gr/HBN ############################

# DFT
figure(figsize=(10, 5))
subplot(1, 3, 1)

grbn_dft_map = grbn_dft.reshape((21, 21), order="F")

#print(np.max(grbn_dft_map)) 

im1 = imshow(grbn_dft_map, 
             extent=extent, 
             cmap='RdBu_r', 
             alpha=.8, 
             interpolation='spline36',              
             origin='lower',
             vmin=0,
             vmax=4.5)
              
C = contour(grbn_dft_map, extent=extent, colors="grey", linestyles="--", linewidths=0.4)
             
## Set_ticks
gca().set_xticks([0, xstep*ddx])
gca().set_xticklabels([0, r"$a$"])
gca().set_yticks([0, ystep*ddy])
gca().set_yticklabels([0, r"$\sqrt{3} a$"])

xlabel(r'$x$ Shift ($\mathrm{\AA}$)')
ylabel(r'$y$ Shift ($\mathrm{\AA}$)')

title("PBE+MBD", fontsize=20)

# colarbar

divider = make_axes_locatable(plt.gca())
cax = divider.append_axes("right", size="8%", pad=0.05)
cbar1 = colorbar(im1, cax=cax)
cbar1.set_ticks(linspace(0, 4.0, 5))  # set the ticks for the colorbar
cbar1.ax.tick_params(width=0.65, length=4.5)  # adjust tick thickness and length

#NEP
subplot(1, 3, 2)
grbn_nep_map = grbn_nep.reshape((21, 21), order="F")
              
#print(np.max(grbn_nep_map)) 

im1 = imshow(grbn_nep_map, 
             extent=extent, 
             cmap='RdBu_r', 
             alpha=.8, 
             interpolation='spline36',           
             origin='lower',
             vmin=0,
             vmax=4.2)

C = contour(grbn_nep_map, extent=extent, colors="grey", linestyles="--", linewidths=0.4)

## Set_ticks
gca().set_xticks([0, xstep*ddx])
gca().set_xticklabels([0, r"$a$"])
gca().set_yticks([0, ystep*ddy])
gca().set_yticklabels([0, r"$\sqrt{3} a$"])

xlabel(r'$x$ Shift ($\mathrm{\AA}$)')
#ylabel(r'$y$ Shift ($\mathrm{\AA}$)')

title("NEP", fontsize=20)

# colarbar

divider = make_axes_locatable(plt.gca())
cax = divider.append_axes("right", size="8%", pad=0.05)
cbar1 = colorbar(im1, cax=cax)
cbar1.set_ticks(linspace(0, 4.0, 5))  # set the ticks for the colorbar
cbar1.ax.tick_params(width=0.65, length=4.5)  # adjust tick thickness and length


###
subplot(1, 3, 3)

#print(np.min(grbn_dft_map- grbn_nep_map)) 

im1 = imshow(grbn_dft_map - grbn_nep_map, 
             extent=extent, 
             cmap='RdBu_r', 
             alpha=.8, 
             interpolation='spline36',           
             origin='lower',
             vmin=0,
             vmax=0.3)

C = contour(grbn_dft_map - grbn_nep_map, extent=extent, colors="grey", linestyles="--", linewidths=0.4)             

xlabel(r'$x$ Shift ($\mathrm{\AA}$)')

title("Differences", fontsize=20) 

## Set_ticks
gca().set_xticks([0, xstep*ddx])
gca().set_xticklabels([0, r"$a$"])
gca().set_yticks([0, ystep*ddy])
gca().set_yticklabels([0, r"$\sqrt{3} a$"])

# colarbar

divider = make_axes_locatable(plt.gca())
cax = divider.append_axes("right", size="8%", pad=0.05)
cbar1 = colorbar(im1, cax=cax)
cbar1.set_ticks(linspace(0, 0.3, 4))  # set the ticks for the colorbar
cbar1.ax.tick_params(width=0.65, length=4.5)  # adjust tick thickness and length

cbar1.set_label('Energy (meV/atom)', fontsize=18)

subplots_adjust(left=0.1, right=0.98, bottom=0.1, top=0.95, wspace=0.42, hspace=0.25)


savefig("Gr-Hbn.svg", bbox_inches='tight')

show()

print("***** ALL Done !!! *****")