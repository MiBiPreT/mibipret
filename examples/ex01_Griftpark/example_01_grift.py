"""Example of data analysis of contaminant data from Griftpark, Utrecht.

@author: Alraune Zech
"""

# import sys
# path = '/home/alraune/GitHub/MiBiPreT/mibipret/mibipret/'
# sys.path.append(path) # append the path to module
# import analysis.sample.screening_NA as na
# import data.data as md

import mibipret.analysis.sample.screening_NA as na
import mibipret.data.data as md

###------------------------------------------------------------------------###
### Script settings
verbose = True

###------------------------------------------------------------------------###
### File path settings
file_path = './grift_BTEXIIN.csv'
file_standard = './grift_BTEXNII_standard.csv'

###------------------------------------------------------------------------###
### Load and standardize data
data_raw,units = md.load_csv(file_path,verbose = verbose)

# column_names_known,column_names_unknown,column_names_standard = md.check_columns(data, verbose = verbose)
# # # print("\nQuantities to be checked on column names: \n",column_names_unknown)

# check_list = md.check_units(data,verbose = verbose)
# # # print("\nQuantities to be checked on units: \n",check_list)

# data_pure = md.check_values(data, verbose = verbose)

data,units = md.standardize(data_raw,reduce = True, store_csv=file_standard,  verbose=verbose)

###------------------------------------------------------------------------###
### perform NA screening step by step

tot_reduct = na.reductors(data,verbose = verbose,ea_group = 'ONSFe')

tot_oxi = na.oxidators(data,verbose = verbose, contaminant_group='BTEXIIN')
#tot_oxi_nut = na.oxidators(data,verbose = verbose,nutrient = True)

e_bal = na.electron_balance(data,verbose = verbose)

na_traffic = na.NA_traffic(data,verbose = verbose)

###------------------------------------------------------------------------###
### Evaluation of intervention threshold exceedance

tot_cont = na.total_contaminant_concentration(data,verbose = verbose,contaminant_group='BTEXIIN')

na_intervention = na.thresholds_for_intervention(data,verbose = verbose,contaminant_group='BTEXIIN')

###------------------------------------------------------------------------###
### NA screening and evaluation of intervention threshold exceedance in one go

data_na = na.screening_NA(data,verbose = verbose)
