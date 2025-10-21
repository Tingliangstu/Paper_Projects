import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# Data
labels = ['NEMD (classical)', 'AEMD', 'Expt. (Raman)', 'Expt. (TDTR)']
values = [62.539155, 6.91712, 52.2, 34.5]
errors = [[10.76446596, 0.364866919, 2.1, 7.4],   # Upper errors
          [10.76446596, 0.364866919, 2.1, 11.6]]   # Lower errors for TDTR

# Set Seaborn style
sns.set(style="ticks")

# Customize axis line, tick, and label properties
sns.set_context("paper", rc={"axes.linewidth": 0.9, "xtick.major.width": 0.9, "ytick.major.width": 0.9, 
                             "axes.labelsize": 22, "xtick.labelsize": 20.0, "ytick.labelsize": 20.0})

# Create bar chart with custom size
fig, ax = plt.subplots(figsize=(8, 5))  # Set the figure size here
bar_width = 0.2  # Set the bar width
index = np.arange(len(labels))  # Set the bar positions

# Create bars with error bars
bars = ax.bar(index, values, bar_width, yerr=errors, capsize=5, 
              color=['#BF4045', 'C2', 'C4', 'grey'], alpha=0.6)
              
# Add labels and customize the plot
ax.set_ylabel('$G$ (MWm$^{-2}$K$^{-1}$)')
ax.set_xticks(index)
ax.set_xticklabels(labels)
ax.set_ylim(0, 80)
ax.set_xlim(-0.3, len(labels)-0.8)  # Adjust x-axis limits for spacing

# Remove x-axis ticks but keep labels
ax.tick_params(axis='x', length=0)  # Set the length of x-axis ticks to 0 to remove the tick marks

# Move the x-axis labels down
ax.set_xticklabels(labels, ha='center', rotation=0)  # Keep labels centered, no rotation
for tick in ax.get_xticklabels():
    tick.set_y(-0.05)  # Move labels down by 0.05

# Add legend if needed (commented out here)
# ax.legend(['NEMD (classical)', 'AEMD', 'Expt. (Raman)', 'Expt. (TDTR)'], loc="best", frameon=False, fontsize=18)

sns.despine(top=True, right=True)

# Show the plot
plt.tight_layout()
fig.savefig("AEMD_ITC_Comparison.svg", bbox_inches='tight', dpi=800)
plt.show()
