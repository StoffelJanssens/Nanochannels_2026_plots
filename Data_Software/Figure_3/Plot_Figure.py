import matplotlib.pyplot as plt

height = [46, 66, 87, 93, 106]  # nm
max_width = [4, 6, 7, 7, 8]  # um

fig, ax = plt.subplots()
ax.errorbar(height, max_width, xerr=6, yerr=1, marker='o', linestyle='')
plt.show()