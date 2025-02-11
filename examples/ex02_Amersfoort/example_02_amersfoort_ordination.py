"""Ordination plots for Amersfoort data.

Example of diagnostic plotting using ordination with contaminant data from Amersfoort site.

@author: Alraune Zech
"""

import pandas as pd

# from mibipret.data.data import load_excel, standardize
from mibipret.visualize.ordination_plot import ordination_plot
# from mibipret.analysis.reduction.ordination import pca,cca,rda

import sys
path = '/home/alraune/GitHub/MiBiPreT/mibipret/mibipret/analysis/reduction/'
sys.path.append(path) # append the path to module
from ordination import pca,cca,rda,filter_values,transform_values
path = '/home/alraune/GitHub/MiBiPreT/mibipret/mibipret/data/'
sys.path.append(path) # append the path to module
from data.data import load_excel, standardize, standard_names, merge_data, extract_data

###------------------------------------------------------------------------###
### Script settings
verbose = False #True

###------------------------------------------------------------------------###
### File path settings
file_path = './amersfoort.xlsx'
#file_standard = './grift_BTEXNII_standard.csv'

###------------------------------------------------------------------------###
### Load and standardize data of environmental quantities/chemicals
environment_raw,units = load_excel(file_path,
                                   sheet_name = 'environment',
                                   verbose = verbose)

environment,units = standardize(environment_raw,
                                reduce = True,
                                verbose=verbose)

###------------------------------------------------------------------------###
### Load and standardize data of contaminants
contaminants_raw,units = load_excel(file_path,
                                    sheet_name = 'contaminants',
                                    verbose = verbose)

contaminants,units = standardize(contaminants_raw,
                                 reduce = False,
                                 verbose=verbose)


data = merge_data([environment,contaminants],clean = True)
variables = ['pH','EC','Redox','DOC','nitrate','nitrite','sulfate','Sum GC',"Mn","Fe"]
# variables_standard = ['pH', 'EC', 'redoxpot', 'DOC', 'nitrate', 'nitrite', 'sulfate', 'manganese', 'iron2']
variables_standard = standard_names(variables) # standardize names

# extract_data(data,name_list = variables_standard+['sample_nr','obs_well'], inplace = True)
extract_data(data,
             name_list = variables_standard,
             keep_setting_data = True,
             inplace = True)


filter_values(data, 
              replace_NaN = 'remove', 
              inplace = True,
              verbose = True)

transform_values(data,
                 name_list = ['Sum GC'],
                 how = 'log_scale',
                 inplace = True,
                 )

transform_values(data,
                  # name_list = variables_standard,
                  how = 'standardize',
                  inplace = True,
                )

data2 = pd.read_csv('data.csv',index_col='well')

ordination_output = pca(data,
                        independent_variables = variables_standard,
                         # independent_variables = variables_standard,
                       # n_comp = 2,
                        # replace_NaN = 'remove',
                        # dependent_variables = species,
                        verbose = True)

# ordination_output = cca(df,
#                         independent_variables = environment,
#                         dependent_variables = species,
#                   )

# ordination_output = rda(data,
#                         independent_variables = environment,
#                         dependent_variables = species,
#                   )
# loadings_independent = ordination_output["loadings_independent"]
# names_independent = ordination_output["names_independent"]
# loadings_dependent = ordination_output["loadings_dependent"]
# names_dependent = ordination_output["names_dependent"]
# loadings = np.append(loadings_independent, loadings_dependent, axis=0)

fig, ax = ordination_plot(ordination_output=ordination_output,
                plot_scores = True, 
                plot_loadings = True,
                rescale_loadings_scores = True, 
                # plot_scores = False, 
                # axis_ranges = [-0.6,0.8,-0.8,1.0],
                # save_fig = 'save3.png',
                )