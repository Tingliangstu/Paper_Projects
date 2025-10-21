from ase.io import read, write
from pynep.calculate import NEP
import numpy as np
from pylab import *

structure = read('bilayer_Hbn_AB_Cartesian.POSCAR')
nep_potential_file = '../../nep.txt'
print("********* Using NEP potential calculator **********")
calculator = NEP(nep_potential_file)
# Get atoms numbers
atom_numbers = len(structure.get_positions())
original_positions = structure.get_positions()

print("********* This structure contains {0} atoms **********\n".format(atom_numbers))

bottom_position = structure.get_positions()[0][2]

nep_energies = []
structure_copy = structure.copy()
structure_copy.calc = calculator
distance = []

scales = [2.0, 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7, 2.8, 2.9, 3.0, 3.1,	3.2, 3.3, 3.4, 3.5,	3.6,	3.7,	3.8,	3.9,	4.0,	4.1,	4.2,	4.3,	4.4,	4.5,	4.6,	4.7,	4.8,	4.9,	5.0,	5.1,	5.2,	5.3,	5.4,	5.5,	5.6,	5.7,	5.8,	5.9,	6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0, 13.0, 14.0, 15.0]

for scale in scales:  #np.arrange(0.6, 6, 0.01):
    position = scale + bottom_position
    distance.append(scale)
    original_positions[1, 2] = position
    original_positions[3, 2] = position
    structure_copy.set_positions(original_positions)
    #print(structure_copy.get_cell())
    nep_energies.append(structure_copy.get_potential_energy() / atom_numbers)
    
# save nep-data

np.savetxt('nep_bilayer_hbn_AB.data', np.column_stack((distance, nep_energies)))

# Set figure properties
aw = 2.0
fs = 17
lw = 3.0
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

# Plot

DFT_data = loadtxt('bilayer_Hbn_AB_stacking_exfoliation_curve.data')

relative_DFT_energies = DFT_data[:, 2] - DFT_data[45, 2]
relative_nep_energies = nep_energies[:] - nep_energies[44]

figure(figsize=(8, 6))
set_fig_properties([gca()])

plot(DFT_data[:, 1], relative_DFT_energies*1000, ls="-", lw=lw, c="C1", label="DFT")
plot(distance, relative_nep_energies*1000, 'o', c="C4", label="NEP")

xlim([2, 10])
ylim([-30, 120])
xlabel('c lattice parameters (A)')
ylabel('Binding energy (meV/atom)')
title('Bilayer Hbn AB-stacking')
legend(loc="best",
        ncol = 2,
        fontsize = 14,
        frameon = False,
        columnspacing = 0.2)

show()
subplots_adjust(wspace=0.35, hspace=0.3)
savefig("Exfoliation_curve.png", bbox_inches='tight')

print("************************ ALL Done !!!! *************************")

