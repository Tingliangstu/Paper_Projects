# Compare phonon dispersion of different potential
from ase.io import read, write
from ase.optimize import BFGS, LBFGS, FIRE, MDMin
from ase.optimize.sciopt import SciPyFminBFGS, SciPyFminCG  # SciPy optimizers

from quippy.potential import Potential

from ase.units import GPa
from ase.constraints import ExpCellFilter
from pynep.calculate import NEP
from calorine.tools import relax_structure

from ase.phonons import Phonons
from pylab import *


def relax(structure, calc, pressure=0.0, maxstep=0.1, eps=None, max_step=None):
    pressure = -np.sum(structure.get_stress()[:3]) / 3 / GPa
    print(f'pressure before: {pressure: 2f} GPa')

    # relax_xyz = True
    # mask = [relax_xyz, relax_xyz, relax_xyz, relax_xyz, relax_xyz, relax_xyz]     # False = fixed, ignore this component

    # ucf = ExpCellFilter(structure, scalar_pressure=pressure*GPa, mask=mask, constant_volume=False)
    # gopt = BFGS(ucf, maxstep=maxstep)
    # gopt.run(fmax=eps, steps=max_step)

    relax_structure(structure)  # use calorine interface with ASE

    print("******** Relax ALL Done !!!!! *********")

    pressure = -np.sum(structure.get_stress()[:3]) / 3 / GPa
    print(f'pressure after relax: {pressure: 2f} GPa')

    write('WSe2_optimize.vasp', structure)

    return structure

def save_ph_data(phonon, file_name = 'phonon_data', convert_to_THz = True):

    # 1 THz = 4.136 meV = 33.356 cm−1;
    # 1 meV = 0.242 THz = 8.066 cm−1;
    # 1 cm−1 = 0.030 THz = 0.124 meV .

    omega = np.squeeze(phonon.energies)
    if convert_to_THz:
       omega = omega * 241.77949   ## From eV to THz

    kpoint, special_k, labels = phonon.get_labels()
    phonon_dic = {'omega': omega, 'kpoint': kpoint, 'special_k':special_k, 'labels':labels}

    np.savez(file_name, **phonon_dic)
    print("************* Save phonon data Done !!! *************")

def phonon_calculator(relaxed_atoms, calculator, repeat_cell):

    print("******** Start to calculate phonon!!!!! *********")
    ph = Phonons(relaxed_atoms, calculator,
                 supercell=(repeat_cell, repeat_cell, repeat_cell), name='phonon', delta=0.05)

    ph.run()
    # Read forces and assemble the dynamical matrix
    ph.read(acoustic=True)
    ph.clean()

    path = relaxed_atoms.cell.bandpath('GMAGZ', npoints=2000)
    bs = ph.get_band_structure(path, convert_to_Thz=False)

    save_ph_data(bs, file_name='alpha_cristobalite_phonon_data/nep_Batch_6_4_2348_calorine.npz', convert_to_THz=True)

    # Plot
    fig = figure(1, figsize=(7, 4))
    ax = fig.add_axes([.12, .07, .67, .85])
    emax = 0.16
    bs.plot(ax=ax, emin=0.0, emax=emax, colors='g')   # ylabel='Frequency [THz]'
    show()

    #savefig('phonon.png')

def get_calculator(file, NEP_file, repeat_cell = 8):

    # Get model from .cif
    model = read(file)

    GAP_pot_calc = Potential('xml_label=GAP_2021_4_19_120_7_32_55_336',
                    param_filename='GAP_potential/silica_gap.xml')

    CHIK_pot_calc = Potential('IP BornMayer',
                               param_filename='BKS_potential/ip.parms.CHIK.xml')

    BKS_pot_calc = Potential('IP BornMayer',
                               param_filename='BKS_potential/ip.parms.BKS.xml')

    Tersoff_pot_calc = Potential('IP Tersoff',
                               param_filename='BKS_potential/ip.parms.Tersoff_2007_SiO.xml')

    # Control potential types
    Tersoff_2007 = False
    Use_BKS = False
    Use_NEP = True
    Use_CHIK = False

    if Use_NEP:
        calculator = NEP(NEP_file)
        print("\n********* Using NEP potential **********\n")

    elif Tersoff_2007:
        calculator = Tersoff_pot_calc
        print("\n********* Using Tersoff-2007 potential **********\n")

    elif Use_BKS:

        calculator = BKS_pot_calc
        print("\n********* Using BKS-1990 potential **********\n")

    elif Use_CHIK:

        calculator = CHIK_pot_calc
        print("\n********* Using CHIK-2008 potential **********\n")

    else:
        calculator = GAP_pot_calc
        print("\n********* Using GAP potential **********\n")

    model.set_calculator(calculator)
    f_max = 0.000001
    relaxed_atoms = relax(structure=model, calc=calculator, eps=f_max, max_step=10000)
    phonon_calculator(relaxed_atoms, calculator, repeat_cell)

if __name__ == "__main__":
    in_file = 'structure/alpha_cristobalite.cif'                     ## The in file for lammps
    nep_potential_file = 'NEP_compare_potential/nep_Full_Batch_6_4_2348_v-0.1_neu-80.txt'

    get_calculator(in_file, nep_potential_file)
