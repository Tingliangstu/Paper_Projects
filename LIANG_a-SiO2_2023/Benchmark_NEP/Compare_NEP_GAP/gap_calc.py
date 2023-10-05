from ase.io import read
# from ase.constraints import ExpCellFilter
# from ase.optimize.precon import PreconLBFGS
from quippy.potential import Potential
import numpy as np

# construct a potential, usage is the same as `quip` command line
pot = Potential('xml_label=GAP_2021_4_19_120_7_32_55_336',
                param_filename='../potential/silica_gap.xml')

test_frames = read('test_261.xyz', ":")
e_dft, e_gap, f_dft, f_gap, v_dft, v_gap = [], [], [], [], [], []

for i, frame in enumerate(test_frames):
    print('************* Processing frame {0} frame *****************'.format(i))
    # Get energies, forces, virials from original dataset (DFT)
    e_dft.append(frame.info['energy'] / len(frame))
    f_dft.append(frame.arrays['force'].reshape(-1))
    v_dft.append(frame.info['virial'].reshape(-1))

    # Get energies, forces, virials from GAP potential
    frame.set_calculator(pot)                                           # associated Atoms with GAP calculator
    vol = frame.get_volume()
    e_gap.append(frame.get_potential_energy() / len(frame))
    f_gap.append(frame.get_forces().reshape(-1))
    v_gap.append(frame.get_stress(voigt=False).reshape(-1) * -1 * vol)  # check the ase definition on stress with virial in gpumd

e_dft = np.array(e_dft)
e_gap = np.array(e_gap)

f_dft = np.concatenate(f_dft)
f_gap = np.concatenate(f_gap)

v_dft = np.concatenate(v_dft)
v_gap = np.concatenate(v_gap)

e_output = np.c_[e_dft, e_gap]
f_output = np.c_[f_dft, f_gap]
v_output = np.c_[v_dft, v_gap]

np.savetxt("energy_comparison.txt", e_output, delimiter="\t", fmt="%20.10f", header="dft_energy (eV/atom) \t gap_energy (eV/atom)")
np.savetxt("force_comparison.txt", f_output, delimiter="\t", fmt="%20.10f", header="dft_force (eV/A) \t gap_force (eV/A)")
np.savetxt("virial_comparison.txt", v_output, delimiter="\t", fmt="%20.10f", header="dft_virial (eV/atom) \t gap_virial (eV/atom)")

print('****************** ALL DONE !!! *******************')