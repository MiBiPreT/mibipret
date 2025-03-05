#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Functions for data extraction and merging in preparation of analysis and plotting.

@author: Alraune Zech
"""
import pandas as pd
import mibipret.data.names_data as names
from mibipret.data.check_data import check_data_frame


def determine_quantities(cols,
         name_list = 'all',
         verbose = False,
         ):
    """Determine quantities to analyse.

    Input
    -----
        cols: list
            Names of quantities from pd.DataFrame)
        name_ist: str or list, dafault is 'all'
            either short name for group of quantities to use, such as:
                    - 'all' (all qunatities given in data frame except settings)
                    - 'BTEX' (for benzene, toluene, ethylbenzene, xylene)
                    - 'BTEXIIN' (for benzene, toluene, ethylbenzene, xylene,
                                  indene, indane and naphthaline)
                    - 'all_cont' (for all contaminant in name list)
            or list of strings with names of quantities to use
        verbose: Boolean
            verbose flag (default False)

    Output
    ------
        quantities: list
            list of strings with names of quantities to use and present in data

    """
    if name_list == 'all':
        ### choosing all column names except those of settings
        quantities = list(set(cols) - set(names.setting_data))
        if verbose:
            print("All data columns except for those with settings will be considered.")
        remainder_list2 = []

    elif isinstance(name_list, list): # choosing specific list of column names except those of settings
        quantities,remainder_list1,remainder_list2 = compare_lists(cols,name_list)

    elif isinstance(name_list, str) and (name_list in names.contaminants.keys()):
        if verbose:
            print("Choosing specific group of contaminants:", name_list)

        contaminants = names.contaminants[name_list].copy()

        # handling of xylene isomeres
        if (names.name_o_xylene in cols) and (names.name_pm_xylene in cols):
            contaminants.remove(names.name_xylene)

        quantities,remainder_list1,remainder_list2 = compare_lists(cols,contaminants)

    elif isinstance(name_list, str) and (name_list in names.electron_acceptors.keys()):
        if verbose:
            print("Choosing specific group of electron acceptors:", name_list)

        electron_acceptors = names.electron_acceptors[name_list].copy()

        quantities,remainder_list1,remainder_list2 = compare_lists(cols,electron_acceptors)

    elif isinstance(name_list, str):
        quantities,remainder_list1,remainder_list2 = compare_lists(cols,[name_list])

        if verbose:
            print("Choosing single quantity:", name_list)

    else:
        raise ValueError("Keyword 'name_list' in correct format")

    if not quantities:
        raise ValueError("No quantities from name list provided in data.\
                         Presumably data not in standardized format. \
                         Run 'standardize()' first.")

    if remainder_list2:
        print("WARNING: quantities from name list not in data:", *remainder_list2,sep='\n')
        print("Maybe data not in standardized format. Run 'standardize()' first.")
        print("_________________________________________________________________")

    if verbose:
        print("Selected set of quantities: ", *quantities,sep='\n')

    return quantities

def extract_data(data_frame,
                 name_list,
                 keep_setting_data = True,
                 verbose = False,
                 ):
    """Extracting data of specified variables from dataframe.

    Args:
    -------
        data_frame: pandas.DataFrames
            dataframe with the measurements
        name_list: list of strings
            list of column names to extract from dataframe
        keep_setting_data: bool, default True
            Whether to keep setting data in the DataFrame.
        verbose: Boolean
            verbose flag (default False)

    Returns:
    -------
        data: pd.DataFrame
            dataframe with the measurements

    Raises:
    -------
    None (yet).

    Example:
    -------
    To be added.

    """
    ### check on correct data input format and extracting column names as list
    data,cols= check_data_frame(data_frame,inplace = False)

    quantities = determine_quantities(cols,
                                      name_list = name_list,
                                      verbose = verbose)

    if keep_setting_data:
        settings,r1,r2 = compare_lists(cols,names.setting_data)
        i1,quantities_without_settings,r2 = compare_lists(quantities,names.setting_data)
        columns_names = quantities + quantities_without_settings
    else:
        columns_names = quantities

    return data[columns_names]


    # data = data_frame.copy()

    # inter_names,r_columns,r_name_list = compare_lists(data.columns.to_list(),name_list)

    # if len(inter_names)<len(name_list):
    #     print("Warning: Not all variables in name_list are identified in the data frame columns: ",r_name_list)

    # if keep_setting_data:
    #     inter_settings,r1,r2 = compare_lists(data.columns.to_list(),names.setting_data)
    #     i1,rim_names,r2 = compare_lists(inter_names,names.setting_data)
    #     inter1 = inter_settings + rim_names
    # else:
    #     inter1 = inter_names
    # return data[inter1]

def merge_data(data_frames_list,
               how='outer',
               on=[names.name_sample],
               clean = True,
               **kwargs,
               ):
    """Merging dataframes along columns on similar sample name.

    Args:
    -------
        data_frames_list: list of pd.DataFrame
            list of dataframes with the measurements
        how: str, default 'outer'
            Type of merge to be performed.
            corresponds to keyword in pd.merge()
            {‘left’, ‘right’, ‘outer’, ‘inner’, ‘cross’}, default ‘outer’
        on: list, default "sample_nr"
            Column name(s) to join on.
            corresponds to keyword in pd.merge()
        clean: Boolean, default True
            Whether to drop columns which are in all provided data_frames
            (on which not to merge, potentially other settings than sample_name)
        **kwargs: dict
            optional keyword arguments to be passed to pd.merge()

    Returns:
    -------
        data: pd.DataFrame
            dataframe with the measurements

    Raises:
    -------
    None (yet).

    Example:
    -------
    To be added.

    """
    if len(data_frames_list)<2:
        raise ValueError('Provide List of DataFrames.')


    data_merge = data_frames_list[0]
    for data_add in data_frames_list[1:]:
        if clean:
            intersection,remainder_list1,remainder_list2 = compare_lists(
                data_merge.columns.to_list(),data_add.columns.to_list())
            intersection,remainder_list1,remainder_list2 = compare_lists(intersection,on)
            data_add = data_add.drop(labels = remainder_list1+remainder_list2,axis = 1)
        data_merge = pd.merge(data_merge,data_add, how=how, on=on,**kwargs)
        # complete data set, where values of porosity are added (otherwise nan)

    return data_merge

### ===========================================================================
### Auxilary Functions
### ===========================================================================

def compare_lists(list1,
                  list2,
                  verbose = False,
                  ):
    """Checking overlap of two given list.

    Input
    -----
        list1: list of strings
            given extensive list (usually column names of a pd.DataFrame)
        list2: list of strings
            list of names to extract/check overlap with strings in list 'column'
        verbose: Boolean, default True
            verbosity flag

    Output
    ------
        (intersection, remainder_list1, reminder_list2): tuple of lists
            * intersection: list of strings present in both lists 'list1' and 'list2'
            * remainder_list1: list of strings only present in 'list1'
            * remainder_list2: list of strings only present in 'list2'

    Example:
    -------
    list1 = ['test1','test2']
    list2 =  ['test1','test3']

    (['test1'],['test2']['test3']) = compare_lists(list1,list2)

    """
    intersection = list(set(list1) & set(list2))
    remainder_list1 = list(set(list1) - set(list2))
    remainder_list2 = list(set(list2) - set(list1))

    if verbose:
        print('================================================================')
        print(" Running function 'extract_variables()'")
        print('================================================================')
        print("strings present in both lists:", intersection)
        print("strings only present in either of the lists:", remainder_list1 +  remainder_list2)

    return (intersection,remainder_list1,remainder_list2)
