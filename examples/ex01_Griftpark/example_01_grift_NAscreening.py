"""Example of data analysis of contaminant data from Griftpark, Utrecht.

@author: Alraune Zech
"""


# path = '/home/alraune/GitHub/MiBiPreT/mibipret/mibipret/'
# sys.path.append(path) # append the path to module
# import analysis.sample.screening_NA as na
# import data.data as md
# from visualize.activity import activity

import mibipret.analysis.sample.screening_NA as na
from mibipret.data.check_data import standardize
from mibipret.data.load_data import load_csv

#from mibipret.data.check_data import check_columns,check_units,check_values, standardize
from mibipret.visualize.activity import activity

###------------------------------------------------------------------------###
### Script settings
verbose = True
contaminant_group='BTEXIIN'

###------------------------------------------------------------------------###
### File path settings
file_path = './grift_BTEXIIN.csv'
file_standard = './grift_BTEXNII_standard.csv'

###------------------------------------------------------------------------###
### Load and standardize data
data_raw,units = load_csv(file_path,verbose = verbose)

# column_names_known,column_names_unknown,column_names_standard = check_columns(data, verbose = verbose)
# # # print("\nQuantities to be checked on column names: \n",column_names_unknown)

# check_list = check_units(data,verbose = verbose)
# # # print("\nQuantities to be checked on units: \n",check_list)

# data_pure = check_values(data, verbose = verbose)

data,units = standardize(data_raw,reduce = True, store_csv=file_standard,  verbose=verbose)

###------------------------------------------------------------------------###
### perform NA screening step by step

tot_reduct = na.reductors(data,verbose = verbose,ea_group = 'ONS')

tot_oxi = na.oxidators(data,verbose = verbose, contaminant_group=contaminant_group)
#tot_oxi_nut = na.oxidators(data,verbose = verbose,nutrient = True)

e_bal = na.electron_balance(data,verbose = verbose)

na_traffic = na.NA_traffic(data,verbose = verbose)

###------------------------------------------------------------------------###
### Evaluation of intervention threshold exceedance

tot_cont = na.total_contaminant_concentration(data,verbose = verbose,contaminant_group=contaminant_group)

na_intervention = na.thresholds_for_intervention(data,verbose = verbose,contaminant_group=contaminant_group)

###------------------------------------------------------------------------###
### NA screening and evaluation of intervention threshold exceedance in one go

### run full NA screening with results in separate DataFrame
data_na = na.screening_NA(data,verbose = verbose)

### run full NA screening with results added to data
na.screening_NA(data,inplace = True,verbose = verbose)

###------------------------------------------------------------------------###
### Create activity plot linking contaminant concentration to metabolite occurence
### and NA screening

fig, ax = activity(data,save_fig='grift_NA_activity.png',dpi = 300)
