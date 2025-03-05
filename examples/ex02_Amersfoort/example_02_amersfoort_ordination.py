"""Unconstrained Ordination (PCA) with plot for Amersfoort data.

Example of diagnostic plotting using ordination with contaminant data from Amersfoort site.

@author: Alraune Zech
"""

from mibipret.analysis.reduction.ordination import pca
from mibipret.analysis.reduction.transformation import filter_values
from mibipret.analysis.reduction.transformation import transform_values
from mibipret.data.check_data import standard_names
from mibipret.data.check_data import standardize
from mibipret.data.load_data import load_excel
from mibipret.data.set_data import extract_data
from mibipret.data.set_data import merge_data
from mibipret.visualize.ordination_plot import ordination_plot

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
                                  verbose = verbose)


data = merge_data([environment,contaminants],clean = True)
#display(data)


###------------------------------------------------------------------------###
variables_1 = standard_names(['Sum GC'])
variables_2 = standard_names(['nitrate','pH','nitrite','sulfate','Redox','EC','DOC',"Mn","Fe"])


data_ordination = extract_data(data,
                  name_list = variables_1 + variables_2,
                  keep_setting_data = True,
                  )

filter_values(data_ordination,
              replace_NaN = 'remove',
              inplace = True,
              verbose = True)

transform_values(data_ordination,
                 name_list = variables_1,
                 how = 'log_scale',
                 inplace = True,
                 )

transform_values(data_ordination,
                 name_list = variables_1,
                  how = 'standardize',
                  inplace = True,
                  )

transform_values(data_ordination,
                 name_list = variables_2,
                 how = 'standardize',
                 inplace = True,
                 )

###------------------------------------------------------------------------###
ordination_output = pca(data_ordination,
                        independent_variables = variables_1+variables_2,
                        verbose = True)

fig, ax = ordination_plot(ordination_output=ordination_output,
                plot_scores = True,
                plot_loadings = True,
                rescale_loadings_scores = True,
                title = "Unconstrained Ordination PCA",
                # plot_scores = False,
                # axis_ranges = [-0.6,0.8,-0.8,1.0],
                # save_fig = 'save3.png',
                )
