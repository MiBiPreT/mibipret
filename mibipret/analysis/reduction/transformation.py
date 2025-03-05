#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Routines for performing ordination statistics on sample data.

@author: Alraune Zech, Jorrit Bakker
"""

import numpy as np
from scipy.stats import zscore
from mibipret.data.check_data import check_data_frame
from mibipret.data.names_data import setting_data
from mibipret.data.set_data import compare_lists


def filter_values(data_frame,
                  replace_NaN = 'remove',
                  drop_rows = [],
                  inplace = False,
                  verbose = False):
    """Filtering values of dataframes for ordination to assure all are numeric.

    Ordination methods require all cells to be filled. This method checks the
    provided data frame if values are missing/NaN or not numeric and handles
    missing/NaN values accordingly.

    It then removes select rows and mutates the cells containing NULL values based
    on the input parameters.

    Input
    -----
        data_frame : pd.dataframe
            Tabular data containing variables to be evaluated with standard
            column names and rows of sample data.
        replace_NaN : string or float, default "remove"
            Keyword specifying how to handle missing/NaN/non-numeric values, options:
                - remove: remove rows with missing values
                - zero: replace values with 0.0
                - average: replace the missing values with the average of the variable
                            (using all other available samples)
                - median: replace the missing values with the median of the variable
                                        (using all other available samples)
                - float-value: replace all empty cells with that numeric value
        drop_rows : List, default [] (empty list)
            List of rows that should be removed from dataframe.
        inplace: bool, default True
            If False, return a copy. Otherwise, do operation in place.
        verbose : Boolean, The default is False.
           Set to True to get messages in the Console about the status of the run code.

    Output
    ------
        data_filtered : pd.dataframe
            Tabular data containing filtered data.
    """
    data,cols= check_data_frame(data_frame,inplace = inplace)

    if verbose:
        print("==============================================================================")
        print('Perform filtering of values since ordination requires all values to be numeric.')

    if len(drop_rows)>0:
        data.drop(drop_rows, inplace = True)
        if verbose:
            print('The samples of rows {} have been removed'.format(drop_rows))

    # Identifying which rows and columns contain any amount of NULL cells and putting them in a list.
    NaN_rows = data[data.isna().any(axis=1)].index.tolist()
    NaN_cols = data.columns[data.isna().any()].tolist()

    # If there are any rows containing NULL cells, the NULL values will be filtered
    if len(NaN_rows)>0:
        if replace_NaN == 'remove':
            data.drop(NaN_rows, inplace = True)
            text = 'The sample row(s) have been removed since they contain NaN values: {}'.format(NaN_rows)
        elif replace_NaN == 'zero':
            set_NaN = 0.0
            data.fillna(set_NaN, inplace = True)
            text = 'The values of the empty cells have been set to zero (0.0)'
        elif isinstance(replace_NaN, (float, int)):
            set_NaN = float(replace_NaN)
            data.fillna(set_NaN, inplace = True)
            text = 'The values of the empty cells have been set to the value of {}'.format(set_NaN)
        elif replace_NaN == "average":
            for var in NaN_cols:
                data[var] = data[var].fillna(data[var].mean(skipna = True))
            text = 'The values of the empty cells have been replaced by the average of\
                  the corresponding variables (using all other available samples).'
        elif replace_NaN == "median":
            for var in NaN_cols:
                data[var] = data[var].fillna(data[var].median(skipna = True))
            text = 'The values of the empty cells have been replaced by the median of\
                  the corresponding variables (using all other available samples).'
        else:
            raise ValueError("Value of 'replace_NaN' unknown: {}".format(replace_NaN))
    else:
        text = 'No data to be filtered out.'

    if verbose:
        print(text)

    return data

def transform_values(data_frame,
                     name_list = 'all',
                     how = 'log_scale',
                     log_scale_A = 1,
                     log_scale_B = 1,
                     inplace = False,
                     verbose = False,
                     ):
    """Extracting data from dataframe for specified variables.

    Args:
    -------
        data_frame: pandas.DataFrames
            dataframe with the measurements
        name_list: string or list of strings, default 'all'
            list of quantities (column names) to perfrom transformation on
        how: string, default 'standardize'
            Type of transformation:
                * standardize
                * log_scale
                * center
        log_scale_A : Integer or float, default 1
            Log transformation parameter A: log10(Ax+B).
        log_scale_B : Integer or float, default 1
            Log transformation parameter B: log10(Ax+B).
        inplace: bool, default True
            If False, return a copy. Otherwise, do operation in place and return None.
        verbose : Boolean, The default is False.
           Set to True to get messages in the Console about the status of the run code.

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
    data,cols= check_data_frame(data_frame,inplace = inplace)

    if verbose:
        print('==============================================================')
        print(" Running function 'transform_values()' on data")
        print('==============================================================')

    if name_list == 'all':
        intersection = list(set(cols) - set(setting_data))

    else:
        if isinstance(name_list, str):
            name_list = [name_list]
        intersection,remainder_list1,remainder_list2 = compare_lists(cols,name_list)
        if len(intersection) < len(name_list):
            print("WARNING: not all variables in name_list are found in dataframe.")
            print('----------------------------------------------------------------')
            print("Column names identified:", intersection)
            print("Column names not identified in data:", remainder_list2)
            print('________________________________________________________________')

    for quantity in intersection:
        if how == 'log_scale':
            data[quantity] = np.log10(log_scale_A * data[quantity] + log_scale_B)
        elif how == 'center':
            data[quantity] =  data[quantity]-data[quantity].mean()
        elif how == 'standardize':
            data[quantity] = zscore(data[quantity].values)
        else:
            raise ValueError("Value of 'how' unknown: {}".format(how))

    return data
