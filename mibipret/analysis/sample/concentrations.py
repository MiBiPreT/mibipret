#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Routines for calculating total concentrations and counts for samples.

@author: Alraune Zech
"""


from mibipret.data.check_data import check_data_frame
from mibipret.data.set_data import determine_quantities


def total_concentration(
        data_frame,
        name_list = "all",
        verbose = False,
        include = False,
        **kwargs,
        ):
    """Calculate total concentration of given list of quantities.

    Input
    -----
        data: pd.DataFrame
            Contaminant concentrations in [ug/l], i.e. microgram per liter
        name_ist: str or list, dafault is 'all'
            either short name for group of quantities to use, such as:
                    - 'all' (all qunatities given in data frame except settings)
                    - 'BTEX' (for benzene, toluene, ethylbenzene, xylene)
                    - 'BTEXIIN' (for benzene, toluene, ethylbenzene, xylene,
                                  indene, indane and naphthaline)
            or list of strings with names of quantities to use
        verbose: Boolean
            verbose flag (default False)
        include: bool, default False
            whether to include calculated values to DataFrame


    Output
    ------
        tot_conc: pd.Series
            Total concentration of contaminants in [ug/l]

    """
    if verbose:
        print('==============================================================')
        print(" Running function 'total_concentration()' on data")
        print('==============================================================')

    ### check on correct data input format and extracting column names as list
    data,cols= check_data_frame(data_frame,inplace = include)

    ### sorting out which columns in data to use for summation of concentrations
    quantities = determine_quantities(cols,name_list = name_list, verbose = verbose)

    ### actually performing summation
    tot_conc = data[quantities].sum(axis = 1)

    if isinstance(name_list, str):
        name_column = 'total concentration {}'.format(name_list)
    elif isinstance(name_list, list):
        name_column = 'total concentration selection'

    tot_conc.rename(name_column,inplace = True)
    if verbose:
        print('________________________________________________________________')
        print("{} in [ug/l] is:\n{}".format(name_column,tot_conc))
        print('--------------------------------------------------')

    ### additing series to data frame
    if include:
        data[name_column] = tot_conc

    return tot_conc

def total_count(
        data_frame,
        name_list = "all",
        threshold = 0.,
        verbose = False,
        include = False,
        **kwargs,
        ):
    """Calculate total number of quantities with concentration exceeding threshold value.

    Input
    -----
        data: pd.DataFrame
            Contaminant concentrations in [ug/l], i.e. microgram per liter
        name_ist: str or list, dafault is 'all'
            either short name for group of quantities to use, such as:
                    - 'all' (all qunatities given in data frame except settings)
                    - 'BTEX' (for benzene, toluene, ethylbenzene, xylene)
                    - 'BTEXIIN' (for benzene, toluene, ethylbenzene, xylene,
                                  indene, indane and naphthaline)
            or list of strings with names of quantities to use
        threshold: float, default 0
            threshold concentration value in [ug/l] to test on exceedence
        verbose: Boolean
            verbose flag (default False)
        include: bool, default False
            whether to include calculated values to DataFrame

    Output
    ------
        tot_count: pd.Series
            Total number of quantities with concentration exceeding threshold value

    """
    if verbose:
        print('==============================================================')
        print(" Running function 'total_count()' on data")
        print('==============================================================')

    threshold = float(threshold)
    if threshold<0:
        raise ValueError("Threshold value '{}' not valid.".format(threshold))

    ### check on correct data input format and extracting column names as list
    data,cols= check_data_frame(data_frame,inplace = include)

    ### sorting out which column in data to use for summation of concentrations
    quantities = determine_quantities(cols,name_list = name_list, verbose = verbose)

    ### actually performing count of values above threshold:
    total_count = (data[quantities]>threshold).sum(axis = 1)

    if isinstance(name_list, str):
        name_column = 'total count {}'.format(name_list)
    elif isinstance(name_list, list):
        name_column = 'total count selection'
    total_count.rename(name_column,inplace = True)

    if verbose:
        print('________________________________________________________________')
        print("Number of quantities out of {} exceeding \
              concentration of {:.2f} ug/l :\n{}".format(len(quantities),threshold,total_count))
        print('--------------------------------------------------')

    if include:
        data[name_column] = total_count

    return total_count
