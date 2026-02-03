import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import pocal
import os


def interpol_data_range(x, y, x_range):
    # Interpolate y-values at the integer x-values
    y_interp = np.interp(x_range, x, y)
    return y_interp


def write_txt_file(file, film_thickness, channel_height):
    data = [['Air', '0'],
            ['PCD', film_thickness],
            ['Air', channel_height],
            ['Glass', 0]]
    df = pd.DataFrame(data)
    df.to_csv(file, index=False, sep='\t', header=False)


# General input
NCD_film_thickness = 286  # (in nm)
wl_range = [350, 875]  # (in nm) the optics absorb all light below 300 nm, so best starting from 350 nm
height_list = [0, 40, 63, 80, 91]  # (in nm) obtained from the AFM data_fig in the center of the channel
height_list_theo = np.arange(101)  # till 100 nm

# ---- EXPERIMENT ----
# Import data_fig and settings
data_ref = pd.read_csv('resources/TFAN_mirror.csv', header=None).to_numpy()

# making array of wavelengths
wl_array = np.arange(wl_range[0], wl_range[1] + 1)

# reference data_fig to obtain reflectance
wl_ref = data_ref[:, 0]
r_ref = data_ref[:, 1] / 100
r_ref_interp_fr = interpol_data_range(wl_ref, r_ref, wl_array)

mean_exp_ref_list = []
for height in height_list:
    # extracting x and y data_fig
    data_1 = pd.read_csv('data_fig/' + str(height) + '_' + str(0) + '.csv', skiprows=9, header=None).to_numpy()
    data_2 = pd.read_csv('data_fig/' + str(height) + '_' + str(1) + '.csv', skiprows=9, header=None).to_numpy()
    data_3 = pd.read_csv('data_fig/' + str(height) + '_' + str(2) + '.csv', skiprows=9, header=None).to_numpy()
    data_meas = (data_1 + data_2 + data_3) / 3
    wl_meas = data_meas[:, 0]
    r_meas = data_meas[:, 1] / 100

    # interpolating x and y data_fig in the x-range
    r_meas_interp_fr = interpol_data_range(wl_meas, r_meas, wl_array)

    # calculating reflectance and storing the mean values into an array
    r_meas_interp_corr_fr = r_meas_interp_fr * r_ref_interp_fr
    mean_exp_ref_list.append(np.mean(r_meas_interp_corr_fr))

# ---- THEORY -----

os.chdir('resources')
mean_theo_ref_list_a = []
for height in height_list_theo:
    write_txt_file('layer_setup.txt', NCD_film_thickness, height)
    pocal_result = pocal.pocal('layer_setup.txt', 0, wl_range[0], wl_range[1], 1, 500, False, None)
    result = pocal_result.s_polarization('reflectance', False, False)
    r_theo = np.array(result[1]).flatten(order='F') / 100
    mean_theo_ref_list_a.append(np.mean(r_theo))
    plt.close('all')

mean_theo_ref_list_b = []
for height in height_list_theo:
    write_txt_file('layer_setup.txt', NCD_film_thickness - 10, height)
    pocal_result = pocal.pocal('layer_setup.txt', 0, wl_range[0], wl_range[1], 1, 500, False, None)
    result = pocal_result.s_polarization('reflectance', False, False)
    r_theo = np.array(result[1]).flatten(order='F') / 100
    mean_theo_ref_list_b.append(np.mean(r_theo))
    plt.close('all')

mean_theo_ref_list_c = []
for height in height_list_theo:
    write_txt_file('layer_setup.txt', NCD_film_thickness + 10, height)
    pocal_result = pocal.pocal('layer_setup.txt', 0, wl_range[0], wl_range[1], 1, 500, False, None)
    result = pocal_result.s_polarization('reflectance', False, False)
    r_theo = np.array(result[1]).flatten(order='F') / 100
    mean_theo_ref_list_c.append(np.mean(r_theo))
    plt.close('all')

os.chdir('..')

# Showing plots
fig, ax = plt.subplots()
ax.errorbar(height_list, mean_exp_ref_list, xerr=[0, 10, 10, 10, 10], yerr=0.004, marker='o', linestyle='')
ax.errorbar(height_list_theo, mean_theo_ref_list_a, xerr=0, yerr=0, marker='', linestyle='-')
ax.errorbar(height_list_theo, mean_theo_ref_list_b, xerr=0, yerr=0, marker='', linestyle='-')
ax.errorbar(height_list_theo, mean_theo_ref_list_c, xerr=0, yerr=0, marker='', linestyle='-')

# Save the plot
plt.savefig('c_overall_reflectance.svg')
plt.show()
