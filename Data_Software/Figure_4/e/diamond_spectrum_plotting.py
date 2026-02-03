import numpy as np
from matplotlib import pyplot as plt

data_1 = np.loadtxt('diamond_spectrum.csv', delimiter=',')
plt.plot(data_1[:, 0], data_1[:, 1]/1000)
#
plt.xlim(270, 320)
plt.ylim(-0.15, 11)

plt.savefig('diamond_spectrum_plot.svg')
plt.show()
