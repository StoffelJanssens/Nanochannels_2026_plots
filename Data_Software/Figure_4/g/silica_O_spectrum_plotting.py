import numpy as np
from matplotlib import pyplot as plt

data_1 = np.loadtxt('silica_O_spectrum.csv', delimiter=',')
plt.plot(data_1[:, 0], data_1[:, 1]/1000)
#
plt.xlim(270, 320)  # electron energy loss [eV]
plt.xlim(525, 555)  # intensity [a. u.]

plt.savefig('silica_O_spectrum_plot.svg')
plt.show()
