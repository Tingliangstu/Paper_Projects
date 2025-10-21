from ase import Atoms
from ase.io import read, write
from ase.build import make_supercell
import os, re, shutil
import numpy as np
from ase.constraints import FixedLine

l = 1.445
hBN_hBN = Atoms("BNNB",
           positions=[[0, 0, 10],
                      [l/2*np.sqrt(3), l/2, 10],
                      [0, 0, 13.4],
                      [l/2*np.sqrt(3), l/2, 13.4]],
           cell=[[l*np.sqrt(3), 0, 0],
                 [l/2*np.sqrt(3), l/2*3, 0],
                 [0, 0, 50]])
hBN_hBN.center()
write("hBN_hBN.vasp", hBN_hBN)

atoms = hBN_hBN.copy()
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
    for j in np.arange(y_mode):
        structure = hBN_hBN.copy()
        structure.positions[2, 0] += delta_x * i
        structure.positions[2, 1] += delta_y * j
        structure.positions[3, 0] += delta_x * i
        structure.positions[3, 1] += delta_y * j 
        structure.wrap()
        c = FixedLine(
            a=[atom.index for atom in structure],
            direction=[0, 0, 1])
        structure.set_constraint(c)
        traj_slip.append(structure)    
        slip_frames += 1
        write(f"SCF/POSCAR_slip_x_{i}_y_{j}", structure)

write("traj_slip.xyz", [traj_slip[i] for i in range(len(traj_slip))])

print('****** Totally got {0} frames slip ****'.format(slip_frames))
print('****** ALL Done !!! ****')