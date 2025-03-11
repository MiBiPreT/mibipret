"""Example of data analysis of contaminant data from Griftpark, Utrecht.

@author: Alraune Zech
"""

import matplotlib.pyplot as plt
import numpy as np
from mibipret.analysis.sample.concentrations import total_concentration
from mibipret.analysis.sample.concentrations import total_count
from mibipret.data.check_data import check_columns
from mibipret.data.check_data import check_units
from mibipret.data.check_data import check_values
from mibipret.data.check_data import standardize
from mibipret.data.load_data import load_excel

#import mibipret.analysis.sample.screening_NA as na
#from mibipret.visualize.activity import activity

###------------------------------------------------------------------------###
### Script settings
verbose = True
plt.close('all')

###------------------------------------------------------------------------###
### File path settings
file_path = './amersfoort.xlsx'

###------------------------------------------------------------------------###
### Load and standardize data of environmental quantities/chemicals
environment_raw,units = load_excel(file_path,
                                   sheet_name = 'environment',
                                   verbose = verbose)

###------------------------------------------------------------------------###
### Details of standardization process
column_names_known,column_names_unknown,column_names_standard = check_columns(
    environment_raw,
    verbose = verbose)
check_list = check_units(environment_raw,
                         verbose = verbose)
environment_pure = check_values(environment_raw,
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
                                    reduce = True,
                                    verbose=verbose)

###------------------------------------------------------------------------###
### Load and standardize data of metabolites
metabolites_raw,units = load_excel(file_path,
                                    sheet_name = 'metabolites',
                                    verbose = verbose)

metabolites,units = standardize(metabolites_raw,
                                reduce = False,
                                verbose=verbose)

metabolites_columns = check_columns(metabolites_raw,
                                    verbose = verbose)
metabolites_units_check = check_units(metabolites_raw,
                                      verbose = verbose)

metabolites_pure = check_values(metabolites_raw,
                                verbose = verbose)

###------------------------------------------------------------------------###
### Basic analysis of contaminant concentrations per sample

contaminants_total = total_concentration(contaminants,
                                         name_list = 'all',
                                         verbose = True)

contaminants_BTEXIIN = total_concentration(contaminants,
                                          name_list = 'BTEXIIN',
                                          verbose = True,
                                          )

contaminants_BTEX = total_concentration(contaminants,
                                        name_list = 'BTEX',
                                        verbose = True,
                                        )

contaminants_BT = total_concentration(contaminants,
                                              name_list = ['benzene','toluene'],
                                              verbose = True,
                                              )


plt.bar(np.arange(len(contaminants_total.values)),np.sort(contaminants_total.values),label='all')
plt.bar(np.arange(len(contaminants_BTEXIIN.values)),np.sort(contaminants_BTEXIIN.values),label='BTEXIIN')
plt.bar(np.arange(len(contaminants_BTEX.values)),np.sort(contaminants_BTEX.values),label='BTEX')
plt.bar(np.arange(len(contaminants_BT.values)),np.sort(contaminants_BT.values),label='BT')
plt.bar(np.arange(len(contaminants['toluene'].values)),np.sort(contaminants['toluene'].values),label='T')
plt.xlabel('Samples')
plt.ylabel('Total concentration [ug/l]')
plt.yscale('log')
plt.legend()
plt.title('Total concentration of contaminants per sample')

###------------------------------------------------------------------------###
### Basic analysis of number of contaminants per sample

contaminants_count = total_count(contaminants,
                                  name_list = 'all',
                                  verbose = True)

contaminants_count_BTEXIIN = total_count(contaminants,
                                  name_list = 'BTEXIIN',
                                  verbose = True)

contaminants_count_BTEX = total_count(contaminants,
                                  name_list = 'BTEX',
                                  verbose = True)

plt.figure(num=2)
plt.bar(np.arange(len(contaminants_count.values)),np.sort(contaminants_count.values),label='all')
plt.bar(np.arange(len(contaminants_count_BTEXIIN.values)),np.sort(contaminants_count_BTEXIIN.values),label='BTEXIIN')
plt.bar(np.arange(len(contaminants_count_BTEX.values)),np.sort(contaminants_count_BTEX.values),label='BTEX')
plt.xlabel('Samples')
plt.ylabel('Total number')
plt.title('Total number of contaminants per sample')
plt.legend()

###------------------------------------------------------------------------###
### Calculating total concentration of metabolites

metabolites_total = total_concentration(metabolites,
                                        name_list = 'all',
                                        verbose = True)


plt.figure(num=3)
plt.bar(np.arange(len(metabolites_total.values)),np.sort(metabolites_total.values),label='all')
plt.xlabel('Samples')
plt.ylabel('Total concentration [ug/l]')
# plt.legend()
plt.title('Total concentration of metabolites per sample')


metabolites_count = total_count(metabolites,
                                name_list = 'all',
                                verbose = True)

plt.figure(num=4)
plt.bar(np.arange(len(metabolites_count.values)),np.sort(metabolites_count.values),label='all')
plt.xlabel('Samples')
plt.ylabel('Total number')
plt.title('Total number of metabolites per sample')
# plt.legend()

###------------------------------------------------------------------------###
### Evaluation of intervention threshold exceedance

# na_intervention_all = thresholds_for_intervention(contaminants,
#                                               contaminant_group='all',
#                                               verbose = verbose,
#                                               )

# na_intervention = thresholds_for_intervention(contaminants,
#                                               contaminant_group='BTEXIIN',
#                                               verbose = verbose,
#                                               )


# data_activity = [contaminants_total.values,
#                  metabolites_count.values,
#                  na_intervention['intervention_traffic'].values]

###------------------------------------------------------------------------###
###------------------------------------------------------------------------###
###------------------------------------------------------------------------###

###
# ### perform NA screening step by step

# tot_reduct = na.reductors(data,verbose = verbose,ea_group = 'ONSFe')

# tot_oxi = na.oxidators(data,verbose = verbose, contaminant_group='BTEXIIN')
# #tot_oxi_nut = na.oxidators(data,verbose = verbose,nutrient = True)

# e_bal = na.electron_balance(data,verbose = verbose)

# na_traffic = na.NA_traffic(data,verbose = verbose)

# ###------------------------------------------------------------------------###
# ### Evaluation of intervention threshold exceedance

# tot_cont = na.total_contaminant_concentration(data,verbose = verbose,contaminant_group='BTEXIIN')

# na_intervention = na.thresholds_for_intervention(data,verbose = verbose,contaminant_group='BTEXIIN')

# ###------------------------------------------------------------------------###
# ### NA screening and evaluation of intervention threshold exceedance in one go

# ### run full NA screening with results in separate DataFrame
# data_na = na.screening_NA(data,verbose = verbose)

# ### run full NA screening with results added to data
# na.screening_NA(data,inplace = True,verbose = verbose)

# ###------------------------------------------------------------------------###
# ### Create activity plot linking contaminant concentration to metabolite occurence
# ### and NA screening

# fig, ax = activity(data)
