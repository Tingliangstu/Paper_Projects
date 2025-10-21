import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set Seaborn style
sns.set(style="ticks")
sns.set_context("paper", rc={
    "axes.linewidth": 0.9,
    "xtick.major.width": 1.1,
    "ytick.major.width": 1.1,
    "axes.labelsize": 24,
    "xtick.labelsize": 20.0,
    "ytick.labelsize": 20.0
})

# Load data from files
def load_data(file_path, convert_units=False):
    data = pd.read_csv(file_path, delim_whitespace=True, header=None, names=["Temperature", "HeatCapacity"])
    if convert_units:
        data["HeatCapacity"] *= 4.184  # Convert cal/mol/K to J/mol/K
    return data

# File paths
files = {
    "WTe2": "WTe2_capacity.txt",
    "MoTe2": "MoTe2_capacity.txt",
    "WSe2": "WSe2_capacity.txt",
    "MoSe2": "MoSe2_capacity.txt",
    "MoS2": "MoS2_capacity.txt",
    "BP_Yo_Machida": "BP_capacity_Yo_Machida.txt",
    "BP_Stephenson": "BP_capacity_stephenson_1968.txt",
    "hBN": "Hbn_capacity.txt",
    "Graphite": "graphite_capacity.txt"
}

# Load and convert data
data_dict = {}
for material, file in files.items():
    convert_units = material == "BP_Stephenson"
    data_dict[material] = load_data(file, convert_units=convert_units)

# Combine BP data
bp_data = pd.concat([data_dict["BP_Yo_Machida"], data_dict["BP_Stephenson"]])

# Marker shapes and colors for each material
markers = {
    "WTe2": "o", "MoTe2": "h", "WSe2": "x", "MoSe2": "p", "MoS2": "^", 
    "BP": "s", "hBN": "v", "Graphite": "D"
}
# Updated colors for a more visually appealing palette
colors = {
    "WTe2": "#1f77b4",  # Blue
    "MoTe2": "#ff7f0e",  # Orange
    "WSe2": "#2ca02c",   # Green
    "MoSe2": "#d62728",  # Red
    "MoS2": "#9467bd",   # Purple
    "BP": "#8c564b",     # Brown
    "hBN": "#e377c2",    # Pink
    "Graphite": "#7f7f7f" # Grey
}

# Plotting
plt.figure(figsize=(8, 7.5))

# Plot each dataset in the specified order with different markers, colors, and no edge color
plot_order = ["WTe2", "MoTe2", "WSe2", "MoSe2", "MoS2", "BP", "hBN", "Graphite"]

for material in plot_order:
    if material == "BP":
        plt.scatter(bp_data["Temperature"], bp_data["HeatCapacity"], label="Black Phosphorus", 
                    color=colors["BP"], marker=markers["BP"], s=120, alpha=0.8, edgecolors='none')
    else:
        data = data_dict[material]
        label = material.replace("_", " ")
        marker = markers.get(material, "o")
        color = colors.get(material, "black")
        plt.scatter(data["Temperature"], data["HeatCapacity"], label=label, 
                    color=color, marker=marker, s=120, alpha=0.8, edgecolors='none')

# Plot single-layer graphene data point
plt.scatter(320.278, 8.63252, color="black", marker="*", s=240, label="Graphene 1L", alpha=0.6, edgecolors='none')

# Customize plot
plt.xlim(0, 360)
plt.ylim(0, 80)
plt.xlabel("Temperature (K)")
plt.ylabel("Heat Capacity (J mol$^{-1}$ K$^{-1}$)")
#plt.legend()
plt.tight_layout()
plt.savefig('heat_capacity.svg', bbox_inches='tight', dpi=600)
plt.show()
