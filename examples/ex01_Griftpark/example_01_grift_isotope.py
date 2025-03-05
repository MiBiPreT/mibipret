#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Lambda plot of isotopes.

Script reproducing Figure 3.10 in the PhD thesis of Suzanne Faber, 2023
'Field investigations and reactive transport modelling of biodegrading
 coal tar compounds at a complex former manufactured gas plant''

data provided on personal basis

@author: Alraune Zech
"""

import matplotlib.pyplot as plt
import numpy as np
from mibipret.analysis.reduction.stable_isotope_regression import Lambda_regression
from mibipret.analysis.reduction.stable_isotope_regression import extract_isotope_data
from mibipret.data.check_data import standardize
from mibipret.data.load_data import load_csv

plt.close('all')

# import sys
# path = '/home/alraune/GitHub/MiBiPreT/mibipret/mibipret/'
# sys.path.append(path)
# from data.data import load_csv
# from data.data import standardize
# from analysis.reduction.stable_isotope_regression import Lambda_regression
# from analysis.reduction.stable_isotope_regression import extract_isotope_data

###------------------------------------------------------------------------###
### Script settings
verbose = True
# molecules = ['benzene','toluene','ethylbenzene','pm_xylene','naphthalene','indane'] #make sure to use standard names
molecules = ['Benzene','Toluene','Ethylbenzene','m,p-Xylene','Indane','Naphthalene']

###------------------------------------------------------------------------###
### File path settings
file_csv = "./grift_BTEXIIN_isotopes.csv"
save_fig = "./example_01_grift_isotopes.pdf"

###------------------------------------------------------------------------###
### Load and standardize data of isotopes

isotopes_raw,units = load_csv(file_csv,
                                  verbose = verbose)

isotopes,units = standardize(isotopes_raw,
                                reduce = True,
                                verbose=verbose)

###------------------------------------------------------------------------###
### Figure settings

wells = ['C','B2','B']
mto = ['s','o','^','<','>','d','*']

fig, axes = plt.subplots(figsize=[7.5,9],ncols = 2, nrows = 3)
ax = axes.flat

for j,molecule in enumerate(molecules):

    for i,well in enumerate(wells):
        data = isotopes[isotopes["obs_well"] == well]

        x,y = extract_isotope_data(data,molecule)
        results = Lambda_regression(x,y,validate_indices = True)

        # Plot the scatter plot
        ax[j].scatter(x, y, marker=mto[i],zorder = 3)
        if len(x)>2:
            # Create a trendline
            polynomial = np.poly1d(results['coefficients'])
            trendline_x = np.linspace(np.min(results['delta_C']), np.max(results['delta_C']), 50)
            trendline_y = polynomial(trendline_x)
            ax[j].plot(trendline_x, trendline_y,
                       label=r'{}, $\Lambda = {:.0f}$'.format(well,results['coefficients'][0]))

        ax[j].set_title(molecule)
        ax[j].grid(True,zorder = 0)
        ax[j].legend(title = r'Well & Lambda:')
        if j%2 == 0:
            ax[j].set_ylabel(r'$\delta^2$H')
        if j >= len(ax)-2:
            ax[j].set_xlabel(r'$\delta^{{13}}$C')

fig.tight_layout()
# plt.savefig(save_fig)
