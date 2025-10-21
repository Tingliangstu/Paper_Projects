# Calculating the phonon dispersion using nep 
# ASE structure
from ase.io import read, write
from ase.build import mx2
# ASE minimize
from ase.optimize import BFGS, LBFGS, FIRE, MDMin
from ase.optimize.sciopt import SciPyFminBFGS, SciPyFminCG  # SciPy optimizers
from ase.units import GPa
from ase.constraints import ExpCellFilter
# ASE phonon
from ase.phonons import Phonons

# pynep or calorine
from pynep.calculate import NEP
from calorine.calculators import CPUNEP
from calorine.tools import relax_structure

from pylab import *

def relax(structure, pressure=0.0, maxstep=0.1, eps=None, max_step=None):
    
    pressure = -np.sum(structure.get_stress()[:3]) / 3 / GPa
    print(f'pressure before: {pressure: 2f} GPa')
    
    #relax_xyz = True
    #mask = [relax_xyz, relax_xyz, relax_xyz, relax_xyz, relax_xyz, relax_xyz]     # False = fixed, ignore this component

    #ucf = ExpCellFilter(structure, scalar_pressure=pressure*GPa, mask=mask, constant_volume=False)
    #gopt = BFGS(ucf, maxstep=maxstep)
    #gopt.run(fmax=eps, steps=max_step)

    relax_structure(structure)                                # use calorine interface with ASE
    
    print("******** Relax ALL Done !!!!! *********")
    
    pressure = -np.sum(structure.get_stress()[:3]) / 3 / GPa
    print(f'pressure after relax: {pressure: 2f} GPa')
    
    #write('WSe2_optimize.vasp', structure)
    
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
                 supercell=(repeat_cell, repeat_cell, 1), name='phonon', delta=0.05)

    ph.run()
    # Read forces and assemble the dynamical matrix
    ph.read(acoustic=True)
    ph.clean()

    path = relaxed_atoms.cell.bandpath('GMKG', npoints=2000)
    bs = ph.get_band_structure(path, convert_to_Thz=True)

    save_ph_data(bs, file_name='WSe2_phonon_data', convert_to_THz=True)

    # Plot
    fig = figure(1, figsize=(7, 4))
    ax = fig.add_axes([.12, .07, .67, .85])
    emax = 10
    bs.plot(ax=ax, emin=-0.1, emax=emax, colors='b', ylabel='Frequency [THz]')
    savefig('phonon.svg')
    show()

def get_calculator(structure, NEP_file, repeat_cell = 6):

    # Get model from .cif
    calculator = NEP(NEP_file)
    print("\n********* Using NEP potential **********\n")
    structure.set_calculator(calculator)
 
    f_max = 0.0001
    relaxed_structure = relax(structure=structure, eps=f_max, max_step=100000)
    
    phonon_calculator(relaxed_structure, calculator, repeat_cell)


if __name__ == "__main__":
	
    # Construct model
    structure = mx2(formula='WSe2', a=3.32, thickness=3.325, size=(1, 1, 1), vacuum=30)
    write("WSe2_pristine.vasp", structure)

    # Nep file
    nep_potential_file = 'nep.txt'
    get_calculator(structure, nep_potential_file)
    
    print('***************** ALL Done !!! *****************')
    


