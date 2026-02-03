import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def interpol_data_range(x, y, x_range):
    # Interpolate y-values at the integer x-values
    y_interp = np.interp(x_range, x, y)
    return y_interp


# Import data_fig and settings
data_ref = pd.read_csv('resources/TFAN_mirror.csv', header=None).to_numpy()
wavelength_range = [370, 875]  # The optics absorb all light below 300 nm
# data_number_list = [15, 0, 3, 6, 9, 12]
name_list = ['chan_', 'chan_water_']
legend_list = ['air-filled', 'water-filled']

# making array of wavelengths
wl_range = np.arange(wavelength_range[0], wavelength_range[1] + 1)

# reference data_fig to obtain reflectance
wl_ref = data_ref[:, 0]
r_ref = data_ref[:, 1] / 100
r_ref_interp_fr = interpol_data_range(wl_ref, r_ref, wl_range)

overall_r_array = []
for name, label in zip(name_list, legend_list):
    # extracting x and y data_fig

    data_1 = pd.read_csv('data_fig/' + name + str(1) + '.csv', skiprows=9, header=None).to_numpy()
    data_2 = pd.read_csv('data_fig/' + name + str(2) + '.csv', skiprows=9, header=None).to_numpy()
    data_3 = pd.read_csv('data_fig/' + name + str(3) + '.csv', skiprows=9, header=None).to_numpy()
    data_meas = (data_1 + data_2 + data_3) / 3
    wl_meas = data_meas[:, 0]
    r_meas = data_meas[:, 1] / 100

    # interpolating x and y data_fig in the x-range
    r_meas_interp_fr = interpol_data_range(wl_meas, r_meas, wl_range)

    # calculating reflectance
    r_meas_interp_corr_fr = r_meas_interp_fr * r_ref_interp_fr
    overall_r_array.append(r_meas_interp_corr_fr)

    # Plotting reflectance corrected with reference reflectance
    plt.plot(wl_range, r_meas_interp_corr_fr, label=label)

r_theo_air, r_theo_water = overall_r_array
print('Overall Reflectance difference = ', np.mean(r_theo_air) - np.mean(r_theo_water))
# Plotting, saving, showing
plt.ylim(0, 0.55)
plt.xlim(370, 875)
plt.legend()

plt.savefig('c_reflectance_device_experiments.svg')
plt.show()
