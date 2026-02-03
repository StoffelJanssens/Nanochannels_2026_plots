import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def interpol_data_range(x, y, x_range):
    # Interpolate y-values at the integer x-values
    y_interp = np.interp(x_range, x, y)
    return y_interp


# Import  and settings
data_ref = pd.read_csv('resources/TFAN_mirror.csv', header=None).to_numpy()
wl_fitting_range = [350, 875]
height_list = [0, 40, 63, 80, 91]

# making array of wavelengths
wl_fit_range = np.arange(wl_fitting_range[0], wl_fitting_range[1] + 1)

# reference data_fig to obtain reflectance
wl_ref = data_ref[:, 0]
r_ref = data_ref[:, 1] / 100
r_ref_interp_fr = interpol_data_range(wl_ref, r_ref, wl_fit_range)

for height in height_list:
    # extracting x and y data_fig
    data_1 = pd.read_csv('data_fig/' + str(height) + '_' + str(0) + '.csv', skiprows=9, header=None).to_numpy()
    data_2 = pd.read_csv('data_fig/' + str(height) + '_' + str(1) + '.csv', skiprows=9, header=None).to_numpy()
    data_3 = pd.read_csv('data_fig/' + str(height) + '_' + str(2) + '.csv', skiprows=9, header=None).to_numpy()
    data_meas = (data_1 + data_2 + data_3) / 3
    wl_meas = data_meas[:, 0]
    r_meas = data_meas[:, 1] / 100

    # interpolating x and y data_fig in the x-range
    r_meas_interp_fr = interpol_data_range(wl_meas, r_meas, wl_fit_range)

    # calculating reflectance
    r_meas_interp_corr_fr = r_meas_interp_fr * r_ref_interp_fr

    # Plotting reflectance corrected with reference reflectance
    plt.plot(wl_fit_range, r_meas_interp_corr_fr, label=height)

# Plotting, saving, showing
plt.ylim(0, 0.55)
plt.xlim(350, 875)
plt.legend()

plt.savefig('a_reflectance_experiments.svg')
plt.show()
