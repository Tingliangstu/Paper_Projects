# -*- coding: utf-8 -*-
from pylab import *
import numpy as np
import os
import seaborn as sns
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from matplotlib import colors
from matplotlib.ticker import AutoMinorLocator

def get_rmse(predicted_data, dft_data):
    #squared_error = []
    #for i in range(len(predicted_data)):
    #    squared_error.append(np.square(predicted_data[i]-dft_data[i]))
    #return np.sqrt(sum(squared_error) / len(squared_error))
    mse = mean_squared_error(predicted_data, dft_data)
    rmse = np.sqrt(mse)
    return rmse
    
# Function to calculate MAE
def get_mae(predicted_data, dft_data):
    return mean_absolute_error(dft_data, predicted_data)

# Function to calculate R-squared
def get_r_squared(predicted_data, dft_data):
    return r2_score(dft_data, predicted_data)

def get_true_virial_of_nep(predicted_data, dft_data, flag="nep", diff_tol = 1e8):
    new_nep_virial_nep = []
    new_nep_virial_dft = []
    num = 0
    for i in range(len(predicted_data)):
        if abs(predicted_data[i] - dft_data[i]) < diff_tol:  # since if no virial exist, structure.virial[m] = -1e6 in GPUMD;
            new_nep_virial_nep.append(predicted_data[i])
            new_nep_virial_dft.append(dft_data[i])
        else: 
       	    num += 1
            print(f"{flag}={predicted_data[i]}, DFT={dft_data[i]}")

    if num > 0: 	  
    	print("deleted {0} frames data for {1} virials".format(num, flag))
            
    return new_nep_virial_nep, new_nep_virial_dft

# Load mace train data
mace_energy_comparison = np.loadtxt('energy_train.out')
mace_force_comparison = np.loadtxt('force_train.out')
mace_virial_comparison = np.loadtxt('stress_train.out')

################################################### Calculate MACE's RMSE ##############################################################
# Calculate MAE and R-squared for energy
mace_energy_rmse = get_rmse(mace_energy_comparison[:, 0], mace_energy_comparison[:, 1])   # eV
mace_energy_mae = get_mae(mace_energy_comparison[:, 0], mace_energy_comparison[:, 1])
mace_energy_r2 = get_r_squared(mace_energy_comparison[:, 0], mace_energy_comparison[:, 1])

## Calculate MAE and R-squared for Force
mace_force_rmse = get_rmse(mace_force_comparison[:, 0:3].reshape(-1, 1), mace_force_comparison[:, 3:6].reshape(-1, 1)) # ev/A
mace_force_mae = get_mae(mace_force_comparison[:, 0:3].reshape(-1), mace_force_comparison[:, 3:6].reshape(-1))
mace_force_r2 = get_r_squared(mace_force_comparison[:, 0:3].reshape(-1), mace_force_comparison[:, 3:6].reshape(-1))

# Call get_true_virial_of_nep function (mace) (Gpa)
new_mace_virial_mace, new_mace_virial_dft = get_true_virial_of_nep(mace_virial_comparison[:, 0:6].reshape(-1, 1), mace_virial_comparison[:, 6:12].reshape(-1, 1), 'mace')
mace_virial_rmse = get_rmse(new_mace_virial_mace, new_mace_virial_dft)
mace_virial_mae = get_mae(new_mace_virial_mace, new_mace_virial_dft)
mace_virial_r2 = get_r_squared(new_mace_virial_mace, new_mace_virial_dft)

# Print MAE and R-squared for energy, force, and virial
print("Energy RMSE: {:.2f} meV/atom".format(mace_energy_rmse*1000))
print("Energy MAE: {:.2f} meV/atom".format(mace_energy_mae*1000))
print("Energy R^2: {:.5f}\n".format(mace_energy_r2))
print("Force RMSE: {:.2f} meV/A".format(mace_force_rmse*1000))
print("Force MAE: {:.2f} meV/A".format(mace_force_mae*1000))
print("Force R^2: {:.5f}\n".format(mace_force_r2))
print("Virial RMSE: {:.2f} GPa".format(mace_virial_rmse))
print("Virial MAE: {:.2f} GPa".format(mace_virial_mae))
print("Virial R^2: {:.5f}".format(mace_virial_r2))

# Plot
alpha=0.65

#*************************** Set Seaborn style *************************
sns.set(style="ticks")

# Customize axis line, tick, and label properties
sns.set_context("paper", rc={"axes.linewidth": 0.8, "xtick.major.width": 0.8, "ytick.major.width": 0.8, 
	              "axes.labelsize": 26.2, "xtick.labelsize": 22, "ytick.labelsize": 22})
	              	
#*************************** Set Seaborn style *************************                    	
                             	
figure(figsize=(16.25, 6.5))

model = "NEP-PT-v2"
bar_colar = 'RdBu_r'
start = 'd'

#############  Energy ##############
subplot(1, 3, 1)
i = 0

bins = 100
hist, xedges, yedges = np.histogram2d(mace_energy_comparison[:, 1], mace_energy_comparison[:, 0], bins=bins)

x_indices = np.clip(np.digitize(mace_energy_comparison[:, 1], xedges) - 1, 0, bins - 1)
y_indices = np.clip(np.digitize(mace_energy_comparison[:, 0], yedges) - 1, 0, bins - 1)
	
norm = colors.LogNorm(vmin=1, vmax=hist.max())
cmap = plt.cm.get_cmap(bar_colar)

scatter(mace_energy_comparison[:, 1], mace_energy_comparison[:, 0], c=hist[x_indices, y_indices], label=model,
	       s=60, marker='o', cmap=cmap, norm=norm, edgecolor='None', alpha=alpha)
	              	
#legend(loc="upper left", fontsize=16)

# Add a colorbar
cbar = colorbar(orientation='horizontal', shrink=0.8, aspect=20)
cbar.set_label('Data counts')
cbar.ax.xaxis.set_minor_locator(AutoMinorLocator())

text(0.93, 0.82, "RMSE = {0:4.1f} meV/atom".format(mace_energy_rmse*1000), ha='right', va='bottom', transform=plt.gca().transAxes, fontsize=23)

#x_min, x_max = gca().get_xlim()
#y_min, y_max = gca().get_ylim()

x_min, x_max = -9.5, -7.5
y_min, y_max = -9.5, -7.5

plot([x_min, x_max], [y_min, y_max], c="grey", lw=1)

## Plot setting

xlim([x_min, x_max])
ylim([y_min, y_max])

x_ticks = np.linspace(x_min, x_max, 5)
y_ticks = np.linspace(y_min, y_max, 5)

x_ticks = [tick for tick in x_ticks if x_min <= tick <= x_max]
y_ticks = [tick for tick in y_ticks if y_min <= tick <= y_max]
    
gca().set_xticks(x_ticks)
gca().set_yticks(y_ticks)

xlabel('DFT energy (eV/atom)')
ylabel(f'NEP energy (eV/atom)')

#text(-0.22, 1.04, f"{chr(ord(start) + i)}", transform=plt.gca().transAxes, fontsize=23, fontweight='bold')

#################### Forces ################

subplot(1, 3, 2)
i = 1

x_values = mace_force_comparison[:, 3:6].reshape(-1)
y_values = mace_force_comparison[:, 0:3].reshape(-1)

bins = 100
hist, xedges, yedges = np.histogram2d(x_values, y_values, bins=bins)

x_indices = np.clip(np.digitize(x_values, xedges) - 1, 0, bins - 1)
y_indices = np.clip(np.digitize(y_values, yedges) - 1, 0, bins - 1)

norm = colors.LogNorm(vmin=1, vmax=hist.max())
cmap = plt.cm.get_cmap(bar_colar)

scatter(x_values, y_values, c=hist[x_indices, y_indices],
	       s=60, marker='o', cmap=cmap, norm=norm, edgecolor='None', alpha=alpha)

# Add a colorbar
cbar = colorbar(orientation='horizontal', shrink=0.8, aspect=20)
cbar.set_label('Data counts')
cbar.ax.xaxis.set_minor_locator(AutoMinorLocator())
	             
text(0.97, 0.06, "RMSE = {0:4.1f} meV/\u00C5".format(mace_force_rmse*1000), ha='right', va='bottom', transform=plt.gca().transAxes, fontsize=23)

x_min, x_max = -45, 45
y_min, y_max = -45, 45

#x_min, x_max = gca().get_xlim()
#y_min, y_max = gca().get_ylim()

plot([x_min, x_max], [y_min, y_max], c="grey", lw=1)

xlim([x_min, x_max])
ylim([y_min, y_max])

gca().set_xticks(linspace(-40, 40, 5))
gca().set_yticks(linspace(-40, 40, 5))

xlabel(r'DFT force (eV/$\rm{\AA}$)')
ylabel(r'NEP force (eV/$\rm{\AA}$)')

#text(-0.26, 1.04, f"{chr(ord(start) + i)}", transform=plt.gca().transAxes, fontsize=23, fontweight='bold')

################# virials ####################
subplot(1, 3, 3)
i = 2
# Convert them to NumPy arrays and ensure they are 1D
new_mace_virial_dft = np.array(new_mace_virial_dft).ravel()
new_mace_virial_mace = np.array(new_mace_virial_mace).ravel()

bins = 100
hist, xedges, yedges = np.histogram2d(new_mace_virial_dft, new_mace_virial_mace, bins=bins)

x_indices = np.clip(np.digitize(new_mace_virial_dft, xedges) - 1, 0, bins - 1)
y_indices = np.clip(np.digitize(new_mace_virial_mace, yedges) - 1, 0, bins - 1)

norm = colors.LogNorm(vmin=1, vmax=hist.max())
cmap = plt.cm.get_cmap(bar_colar)

scatter(new_mace_virial_dft, new_mace_virial_mace, c=hist[x_indices, y_indices],
	       s=60, marker='o', cmap=cmap, norm=norm, edgecolor='None', alpha=alpha)
	              	
# Add a colorbar
cbar = colorbar(orientation='horizontal', shrink=0.8, aspect=20)
cbar.set_label('Data counts')
cbar.ax.xaxis.set_minor_locator(AutoMinorLocator())

x_min, x_max = -40, 200
y_min, y_max = -40, 200

#x_min, x_max = gca().get_xlim()
#y_min, y_max = gca().get_ylim()

plot([x_min, x_max], [y_min, y_max], c="grey", lw=1)

text(0.92, 0.06, "RMSE = {0:4.1f} Gpa".format(mace_virial_rmse), ha='right', va='bottom', transform=plt.gca().transAxes, fontsize=22)

xlim([x_min, x_max])
ylim([y_min, y_max])

xlabel('DFT stress (Gpa)')
ylabel(f'NEP stress (Gpa)')

#text(-0.26, 1.04, f"{chr(ord(start) + i)}", transform=plt.gca().transAxes, fontsize=23, fontweight='bold')

########################### Label ##############################

subplots_adjust(left=0.1, right=0.98, bottom=0.1, top=0.95, wspace=0.35, hspace=0.25)

savefig("RMSE.png", bbox_inches='tight', dpi=600)

print("******** All done *******")
