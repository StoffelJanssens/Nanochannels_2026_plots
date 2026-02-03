import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import pocal
import os


def interpol_data_range(x, y, x_range):
    # Interpolate y-values at the integer x-values
    y_interp = np.interp(x_range, x, y)
    return y_interp


def write_txt_file_air(file, film_thickness, channel_height):
    data = [['Air', 0],
            ['PCD', film_thickness],
            ['Air', channel_height],
            ['Glass', 0]]
    df = pd.DataFrame(data)
    df.to_csv(file, index=False, sep='\t', header=False)


def write_txt_file_water(file, film_thickness, channel_height):
    data = [['Air', 0],
            ['PCD', film_thickness],
            ['Water', channel_height],  # Data taken from Daimon2007 paper
            ['Glass', 0]]
    df = pd.DataFrame(data)
    df.to_csv(file, index=False, sep='\t', header=False)


# Import data_fig and settings
NCD_film_thickness = 286
wl_fitting_range = [350, 875]  # the optics absorb all light below 300 nm, so best fitting from 350 nm
# height_list = [0, 40, 63, 80, 91, 92]  # obtained from the AFM data_fig in the center of the channel
height = 65  # obtained from the AFM data_fig in the center of the channel

# making array of wavelengths
wl_fit_range = np.arange(wl_fitting_range[0], wl_fitting_range[1] + 1)

os.chdir('resources')

write_txt_file_air('layer_setup.txt', NCD_film_thickness, height)
pocal_result = pocal.pocal('layer_setup.txt', 0, wl_fitting_range[0], wl_fitting_range[1], 1, 500, False, None)
result = pocal_result.s_polarization('reflectance', False, False)
r_theo_air = np.array(result[1]).flatten(order='F') / 100

write_txt_file_water('layer_setup.txt', NCD_film_thickness, height)
pocal_result = pocal.pocal('layer_setup.txt', 0, wl_fitting_range[0], wl_fitting_range[1], 1, 500, False, None)
result = pocal_result.s_polarization('reflectance', False, False)
r_theo_water = np.array(result[1]).flatten(order='F') / 100
plt.close('all')

os.chdir('..')

print('Overall Reflectance difference = ', np.mean(r_theo_air) - np.mean(r_theo_water))

plt.plot(wl_fit_range, r_theo_air, label='air-filled')
plt.plot(wl_fit_range, r_theo_water, label='water-filled')

# Showing plots
plt.ylim(0, 0.55)
plt.xlim(370, 875)
plt.legend()

plt.savefig('d_reflectance_device_simulations.svg')
plt.show()
