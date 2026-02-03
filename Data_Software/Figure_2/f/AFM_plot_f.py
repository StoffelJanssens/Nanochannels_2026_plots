import numpy as np
from matplotlib import pyplot as plt

plt.figure(figsize=(18, 2.5))

data = np.loadtxt('34_nJ_7_um.txt', delimiter='\t')
plt.plot(data[:, 0] - 16.7, data[:, 1])

plt.xlim(-5.9, 13.9)
plt.ylim(-5, 120)

plt.savefig('f.svg')
plt.show()