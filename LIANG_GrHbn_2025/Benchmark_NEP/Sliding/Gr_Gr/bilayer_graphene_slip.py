"""
For constructing the slip structure and their corresponding perturbed structures
2022/11/24 13:41:16
"""

from ase.io import read, write
from ase.build import make_supercell
import os, re, shutil
import numpy as np
from ase.constraints import FixedLine

atoms = read("AB_3.4.vasp")
a = atoms.get_cell()[0][0]
b = atoms.get_cell()[0][0]
print('**** The lattice a is {0:5.4f} ****'.format(a))

aa

x1 = atoms.positions[2, 0]          # Coord of two atoms on the top
y1 = atoms.positions[2, 1]
x2 = atoms.positions[3, 0]
y2 = atoms.positions[3, 1]
N = 20
delta_x = a / N
delta_y = b / N * np.sqrt(3)
x_mode = N + 1
y_mode = N + 1
traj_slip = []
slip_frames = 0

os.makedirs("SCF", exist_ok=True)
for i in np.arange(x_mode):
    new_x1 = x1 + delta_x * i
    new_x2 = x2 + delta_x * i
    for j in np.arange(y_mode):
        new_y1 = y1 + delta_y * j
        new_y2 = y2 + delta_y * j
        new_atoms = read("AB_3.4.vasp")
        new_atoms.positions[2, 0] = new_x1
        new_atoms.positions[2, 1] = new_y1
        new_atoms.positions[3, 0] = new_x2
        new_atoms.positions[3, 1] = new_y2 
        new_atoms.wrap()  
        c = FixedLine(
            a=[atom.index for atom in new_atoms if atom.symbol == 'C'],
            direction=[0, 0, 1])
        new_atoms.set_constraint(c)
        traj_slip.append(new_atoms)    
        slip_frames += 1
        write("POSCAR_slip_x_{0}_y_{1}".format(i, j), new_atoms)
        # For assign jobs submitted
        shutil.move("POSCAR_slip_x_{0}_y_{1}".format(i, j), "SCF/.".format(i, j))

write("traj_slip.xyz", [traj_slip[i] for i in range(len(traj_slip))])

print('****** Totally got {0} frames slip ****'.format(slip_frames))
print('****** ALL Done !!! ****')