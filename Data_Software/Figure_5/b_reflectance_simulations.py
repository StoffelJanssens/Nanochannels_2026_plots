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


# Import data_fig and settings
NCD_film_thickness = 286
wl_fitting_range = [350, 875]  # the optics absorb all light below 300 nm, so best fitting from 350 nm
# height_list = [0, 40, 63, 80, 91, 92]  # obtained from the AFM data_fig in the center of the channel
height_list = [0, 40, 63, 80, 91]  # obtained from the AFM data_fig in the center of the channel

# making array of wavelengths
wl_fit_range = np.arange(wl_fitting_range[0], wl_fitting_range[1] + 1)

os.chdir('resources')
reflectance_list = []
for height in height_list:
    write_txt_file('layer_setup.txt', NCD_film_thickness, height)
    pocal_result = pocal.pocal('layer_setup.txt', 0, wl_fitting_range[0], wl_fitting_range[1], 1, 500, False, None)
    result = pocal_result.s_polarization('reflectance', False, False)
    r_theo = np.array(result[1]).flatten(order='F') / 100
    reflectance_list.append(r_theo)
    plt.close('all')

os.chdir('..')

for reflectance, height in zip(reflectance_list, height_list):
    plt.plot(wl_fit_range, reflectance, label=height)

# Showing plots
plt.ylim(0, 0.55)
plt.xlim(350, 875)
plt.legend()

plt.savefig('b_reflectance_simulations.svg')
plt.show()
