from ase.io import read, write
from pynep.calculate import NEP
import numpy as np
from pylab import *

structure = read('bulk_hbn_1x1x1_opti.CONTCAR')
nep_potential_file = '../nep.txt'
print("********* Using NEP potential calculator **********")
calculator = NEP(nep_potential_file)
# Get atoms numbers
atom_numbers = len(structure.get_positions())
original_cell = structure.get_cell()

print("********* This structure contains {0} atoms **********\n".format(atom_numbers))

Lat_c = structure.get_cell()[2, 2]
nep_energies = []
structure_copy = structure.copy()
structure_copy.calc = calculator
distance = []

scales = [0.60, 0.65, 0.70, 0.75, 0.80, 0.85, 0.90, 0.92, 0.94, 0.96, 0.97, 0.98, 0.99, 1.00, 1.01, 1.02, 1.03, 1.04, 1.06, 1.08, 1.10, 1.12, 1.14, 1.16, 1.18, 1.20, 1.22, 1.25, 1.28, 1.31, 1.34, 1.37, 1.41, 1.45, 1.49, 1.53, 1.57, 1.61, 1.65, 1.70, 1.75, 1.80, 1.85, 1.90, 1.95, 2.00, 2.05, 2.10, 2.15, 2.20, 2.30, 2.40, 2.50, 3.00, 3.50, 4.00, 4.50, 5.00, 6.00]

for scale in scales:  #np.arrange(0.6, 6, 0.01):
    Lat_new = scale * Lat_c
    distance.append(Lat_new)
    original_cell[2, 2] = Lat_new
    structure_copy.set_cell(original_cell, scale_atoms=True)
    #print(structure_copy.get_cell())
    nep_energies.append(structure_copy.get_potential_energy() / atom_numbers)

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

DFT_data = loadtxt('bulk_Hbn_exfoliation_curve.data')

# save nep-data

np.savetxt('hbn.data', np.column_stack((DFT_data[:, 1], nep_energies)))

relative_DFT_energies = DFT_data[:, 2] - DFT_data[49, 2]
relative_nep_energies = nep_energies[:] - nep_energies[48]

figure(figsize=(8, 6))
set_fig_properties([gca()])

plot(DFT_data[:, 1], relative_DFT_energies*1000, ls="-", lw=lw, c="C1", label="DFT")
plot(distance, relative_nep_energies*1000, 'o', c="C4", label="NEP")

xlim([4, 16])
ylim([-65, 120])
xlabel('c lattice parameters (A)')
ylabel('Binding energy (meV/atom)')
title('Bulk-Hbn')
legend(loc="best",
        ncol = 2,
        fontsize = 14,
        frameon = False,
        columnspacing = 0.2)

subplots_adjust(wspace=0.35, hspace=0.3)
savefig("Exfoliation_curve.png", bbox_inches='tight')
show()

