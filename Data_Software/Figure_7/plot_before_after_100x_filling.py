import numpy as np
from matplotlib import pyplot as plt


def interpol_data_range(x, y, x_range):
    # Interpolate y-values at the integer x-values
    y_interp = np.interp(x_range, x, y)
    return y_interp


data_1 = np.loadtxt('before_100x.txt')
x_1 = data_1[:, 0]
y_1 = data_1[:, 1]

data_2 = np.loadtxt('after_100x.txt')
x_2 = data_2[:, 0]
y_2 = data_2[:, 1]

y_1_inter = interpol_data_range(x_1, y_1, x_2)
y_mean = (y_1_inter + y_2) / 2
plt.plot(x_2, y_mean + 10, color='gray')
plt.plot(x_2, y_mean - 10, color='gray')
plt.fill_between(x_2, y_mean + 10, y_mean - 10, color='gray')

plt.plot(x_2, y_1_inter)
plt.plot(x_2, y_2)

plt.xlim(-8, 13)
# x is in micrometers and y is in nanometers

plt.savefig('figure_7.svg')
plt.show()
