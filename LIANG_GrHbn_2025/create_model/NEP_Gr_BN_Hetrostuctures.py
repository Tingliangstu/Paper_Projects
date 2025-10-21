#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
For creating the mono-multi layer Gr-Hbn hetrostructure GPUMD data
@author: LiangTing
Email: lianting.zj@gmail.com
2023/09/07 11:53
"""
import numpy as np

def generate_super_structure(gr_supercell, hbn_supercell):

    ## Lattice parameters
    primitive_atoms = np.array([[0.25, 1/6, 0],
                                [0.75, 1/3, 0],
                                [0.75, 2/3, 0],
                                [0.25, 5/6, 0]])

    num_primitive_atoms = np.size(primitive_atoms, 0)

    ## Onelayer atoms number
    gr_atom = gr_supercell[0] * gr_supercell[1] * gr_supercell[2] * num_primitive_atoms
    bn_atom = hbn_supercell[0] * hbn_supercell[1] * hbn_supercell[2] * num_primitive_atoms

    cc_bond = 1.42
    bn_bond = cc_bond*gr_supercell[0]/hbn_supercell[0]
    
    layer_distance = 3.4

    gr_box = np.array([cc_bond * np.sqrt(3), cc_bond * 3, layer_distance])
    hbn_box = np.array([bn_bond * np.sqrt(3), bn_bond * 3, layer_distance])

    # store the data
    position = np.zeros([bn_atom + gr_atom, 3])
    atom_type = []
    group_id = np.zeros(bn_atom + gr_atom)
    atom_id = 0

    # For hbn multilayer
    for nx in range(hbn_supercell[0]):
        for ny in range(hbn_supercell[1]):
            for nz in range(hbn_supercell[2]):              # For 2D material, z = 1
                for k in range(num_primitive_atoms):

                    if nz == 1:
                        group_id[atom_id] = 1
                        
                    elif nz == 0:
                        group_id[atom_id] = 0

                    else:
                        group_id[atom_id] = nz - 1

                    if nz % 2 == 0:
                        if atom_id % 2 == 0:                # B1 atom --- even layer
                            atom_type.append('B')
                        else:
                            atom_type.append('N')     # N1 atom --- even layer

                    else:
                        if atom_id % 2 == 0:                # B2 atom --- odd layer
                            atom_type.append('B')
                        else:
                            atom_type.append('N')          # N2 atom --- odd layer

                    # For atom position
                    position[atom_id, 0] = primitive_atoms[k][0] * hbn_box[0] + nx * hbn_box[0]
                    position[atom_id, 1] = primitive_atoms[k][1] * hbn_box[1] + ny * hbn_box[1]
                    position[atom_id, 2] = primitive_atoms[k][2] + nz * hbn_box[2]

                    atom_id += 1             # Increase index

    # For Gr multilayer
    for nx in range(gr_supercell[0]):
        for ny in range(gr_supercell[1]):
            for nz in range(gr_supercell[2]):              # For 2D material, z = 1
                for k in range(num_primitive_atoms):
                    
                    if (nz + hbn_supercell[2]) == (gr_supercell[2] + hbn_supercell[2] - 1):
                        group_id[atom_id] = 22
                    	  
                    else:
                        group_id[atom_id] = nz + hbn_supercell[2] - 1

                    # For C layer
                    if (nz + hbn_supercell[2]) % 2 == 0:
                        atom_type.append('C')                 # C atom --- even layer
                    else:
                        atom_type.append('C')                 # C atom --- old layer

                    # For atom position
                    position[atom_id, 0] = primitive_atoms[k][0] * gr_box[0] + nx * gr_box[0]
                    position[atom_id, 1] = primitive_atoms[k][1] * gr_box[1] + ny * gr_box[1]
                    position[atom_id, 2] = primitive_atoms[k][2] + (nz + hbn_supercell[2]) * gr_box[2]

                    atom_id += 1             # Increase index

    # write to file
    output_file_name = 'model.xyz'

    with open(output_file_name, 'w') as fid:

        fid.write('{0}\n'.format(bn_atom + gr_atom))

        fid.write('Lattice=\"{0:8.8f} {1:8.8f} {2:8.8f} {3:8.8f} {4:8.8f} {5:8.8f} {6:8.8f} {7:8.8f} {8:8.8f}\"'.\
            format(gr_box[0]*gr_supercell[0], 0, 0, 0, gr_box[1]*gr_supercell[1], 0, 0, 0, max(position[:, 2]+3.5)))
        fid.write('  Properties=species:S:1:pos:R:3:group:I:1  pbc="T T F"\n')
        for i, row in enumerate(position):
            fid.write('{0} {1:15.8f} {2:15.8f} {3:15.8f} {4:10.0f}\n'.format(atom_type[i],           # ids and molecular's ids
                                                                         row[0], row[1], row[2],     # position
                                                                         group_id[i]))               # group_id
    fid.close()

    print('\n************* ' + output_file_name + ' is written successfully' + ' ************\n')

if __name__ == "__main__":

    num_layer_gr = 12
    num_layer_hbn = 13

    gr_supercell = [56, 56, num_layer_gr]  # x, y, z
    hbn_supercell = [55, 55, num_layer_hbn]  # x, y, z

    generate_super_structure(gr_supercell, hbn_supercell)

    print('Graphene/h-BN heterostructure data generate all done\n')