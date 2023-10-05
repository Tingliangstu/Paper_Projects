from pylab import *
import numpy as np

##set figure properties
aw = 1.5
fs = 16
lw = 2.0
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

def get_rmse(predicted_data, dft_data):
    squared_error = []
    for i in range(len(predicted_data)):
        squared_error.append(np.square(predicted_data[i]-dft_data[i]))

    return np.sqrt(sum(squared_error) / len(squared_error))

def get_true_virial_of_nep(virial_data, diff_tol = 5):
    new_nep_virial_nep = []
    new_nep_virial_dft = []
    for i in range(len(virial_data[:, 0])):
        if abs(virial_data[i, 0] - virial_data[i, 1]) < diff_tol:  # since if no virial exist, structure.virial[m] = -1e6 in GPUMD;
            new_nep_virial_nep.append(virial_data[i, 0])
            new_nep_virial_dft.append(virial_data[i, 1])
    return new_nep_virial_nep, new_nep_virial_dft

# Load NEP test data (NEP_test_Full_Batch_6_4_3074_v-0.1_neu-80)
nep_energy_test = loadtxt('energy_test.out')
nep_force_test = loadtxt('force_test.out')
nep_virial_test = loadtxt('virial_test.out')

# Load GaP test data (https://doi.org/10.1038/s41524-022-00768-w)
gap_energy_comparison = np.loadtxt('energy_comparison.txt')
gap_force_comparison = np.loadtxt('force_comparison.txt')
gap_virial_comparison = np.loadtxt('virial_comparison.txt')

# Calculate RMSE from NEP
nep_energy_test_rmse = get_rmse(nep_energy_test[:, 0], nep_energy_test[:, 1])   # eV
nep_force_test_rmse = get_rmse(nep_force_test[:, 0:3].reshape(-1, 1), nep_force_test[:, 3:6].reshape(-1, 1)) # ev/A

# Call get_true_virial_of_nep function
new_nep_virial_nep, new_nep_virial_dft = get_true_virial_of_nep(nep_virial_test)
nep_virial_test_rmse = get_rmse(new_nep_virial_nep, new_nep_virial_dft)

# Calculate RMSE from GAP
gap_energy_rmse = get_rmse(gap_energy_comparison[:, 0], gap_energy_comparison[:, 1])   # eV
gap_force_rmse = get_rmse(gap_force_comparison[:, 0:3].reshape(-1, 1), gap_force_comparison[:, 3:6].reshape(-1, 1)) # ev/A

#new_gap_virial_gap, new_gap_virial_dft = get_true_virial_of_nep(gap_virial_comparison)
gap_virial_rmse = get_rmse(gap_virial_comparison[:, 0], -gap_virial_comparison[:, 1])

# Plot
figure(figsize=(18, 7))
subplot(1, 3, 1)
set_fig_properties([gca()])

# Energy
plot(gap_energy_comparison[:, 1], gap_energy_comparison[:, 0], 'o', c="C0", ms=5, label="GAP Test")
plot(nep_energy_test[:, 1], nep_energy_test[:, 0], 'o', c="C6", ms=5, label="NEP Test")  # transparent => alpha=0.5
plot([-12, 0], [-12, 0], c = "grey", lw = 1)

text(-8, -10, 'GAP RMSE = {0:4.2f} mev/atom'.format(gap_energy_rmse*1000), fontsize=13)
text(-8, -11, 'NEP RMSE = {0:4.2f} mev/atom'.format(nep_energy_test_rmse*1000), fontsize=13)

xlim([-12, 0])
ylim([-12, 0])
xlabel('DFT energy (eV/atom)')
ylabel('Predicted energy (eV/atom)')
legend(loc="upper left")

# Forces
subplot(1, 3, 2)
set_fig_properties([gca()])

plot(gap_force_comparison[:, 3], gap_force_comparison[:, 0], 'o', c="C2", ms = 5, label="GAP Test")
plot(gap_force_comparison[:, 4:6], gap_force_comparison[:, 1:3], 'o', c="C2", ms = 5)

plot(nep_force_test[:, 3], nep_force_test[:, 0], 'o', c="C7", ms = 5, label="NEP Test")
plot(nep_force_test[:, 4:6], nep_force_test[:, 1:3], 'o', c="C7", ms = 5)
plot([-50, 50], [-50, 50], c = "grey", lw = 1)

text(-20, -37, 'GAP RMSE = {0:4.2f} mev/A'.format(gap_force_rmse*1000), fontsize=13)
text(-20, -42, 'NEP RMSE = {0:4.2f} mev/A'.format(nep_force_test_rmse*1000), fontsize=13)

xlim([-50, 50])
ylim([-50, 50])
xlabel(r'DFT force (eV/$\rm{\AA}$)')
ylabel(r'Predicted force (eV/$\rm{\AA}$)')
legend(loc="upper left")

# virials
subplot(1, 3, 3)
set_fig_properties([gca()])
plot(gap_virial_comparison[:, 1], -gap_virial_comparison[:, 0], 'o', c="C3", ms = 5, label="GAP Test")
plot(nep_virial_test[:, 1], nep_virial_test[:, 0],  'o', c="C8", ms = 5, label="NEP Test")
plot([-10, 10], [-10, 10], c = "grey", lw = 1)

text(-4, -7, 'GAP RMSE = {0:4.2f} mev/atom'.format(gap_virial_rmse*1000), fontsize=13)
text(-4, -8.2, 'NEP RMSE = {0:4.2f} mev/atom'.format(nep_virial_test_rmse*1000), fontsize=13)

xlim([-10, 10])
ylim([-10, 10])
xlabel('DFT virial (eV/atom)')
ylabel('Predicted virial (eV/atom)')
legend(loc="upper left")
subplots_adjust(left=0.1, right=0.98, bottom=0.1, top=0.95, wspace=0.3, hspace=0.3)
#show()

savefig("Compare_NEP_GAP.png", bbox_inches='tight')
