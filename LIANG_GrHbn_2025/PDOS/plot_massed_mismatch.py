import matplotlib.pyplot as plt
import seaborn as sns

# Define the masses and atom counts
masses = {
    'Gr': 24.02,
    '$h$-BN': 24.82,
    'MoS2': 160.07,
    'WS2': 247.96,
    'WSe2': 341.76
}

# Define the number of atoms in the unit cell for each material
unit_cell_atoms = {
    'Gr': 2,
    '$h$-BN': 2,
    'MoS2': 3,
    'WS2': 3,
    'WSe2': 3
}

# Calculate the average atomic mass for each material
average_atomic_mass = {material: mass / unit_cell_atoms[material] for material, mass in masses.items()}

# Define the heterojunctions in the specified order
heterojunctions = [
    ('Gr', '$h$-BN'),
    ('$h$-BN', 'MoS2'),
    ('Gr', 'MoS2'),
    ('MoS2', 'WSe2'),
    ('$h$-BN', 'WSe2'),
    ('Gr', 'WSe2'),
    ('$h$-BN', 'WS2'),
    ('WS2', 'WSe2')
]

# Calculate mass differences
mass_diffs = []
for (material1, material2) in heterojunctions:
    avg_mass_diff = abs(average_atomic_mass[material1] - average_atomic_mass[material2])
    mass_diffs.append((f'{material1}/{material2}', avg_mass_diff))

# Sort by mass difference
mass_diffs.sort(key=lambda x: x[1])

# Extract the labels and values for plotting in the specified order
labels, values = zip(*mass_diffs)

# Format labels to display "2" as subscript
formatted_labels = [label.replace("2", "$_2$") for label in labels]

# Set Seaborn style
sns.set(style="ticks")

# Customize axis line, tick, and label properties
sns.set_context("paper", rc={"axes.linewidth": 0.8, "xtick.major.width": 0.8, "ytick.major.width": 0.8,
                             "axes.labelsize": 18, "xtick.labelsize": 16.0, "ytick.labelsize": 16.0})

# Plot the results
bar_width = 0.5  # Width of the bars
plt.figure(figsize=(6, 6))
plt.bar(formatted_labels, values, width=bar_width, color="#BF4045", alpha=0.7)
plt.ylabel('Average Atomic Mass Difference (u)')
plt.xticks(rotation=45)

# Remove top and bottom spines
sns.despine(top=True, right=True)

# Remove x-axis ticks
plt.tick_params(axis='x', which='both', bottom=False, top=False) # Hide x-axis ticks

plt.tight_layout()

# Save the figure
plt.savefig("Massed_differ.svg", bbox_inches='tight', dpi=800)

plt.show()
