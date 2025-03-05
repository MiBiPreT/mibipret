#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Routines for performing ordination statistics on sample data.

@author: Alraune Zech, Jorrit Bakker
"""

import numpy as np
import skbio.stats.ordination as sciord
from sklearn import decomposition
from mibipret.data.check_data import check_data_frame


def pca(data_frame,
        independent_variables = False,
        dependent_variables = False,
        n_comp = 2,
        verbose = False,
        ):
    """Function that performs Principal Component Analysis.

    Makes use of routine sklearn.decomposition.PCA on the input data and gives
    the site scores and loadings.

    Principal component analysis (PCA) is a linear dimensionality reduction
    technique with applications in exploratory data analysis, visualization
    and data preprocessing. The data is linearly transformed onto a new
    coordinate system such that the directions (principal components) capturing
    the largest variation in the data can be easily identified.

    Input
    -----
        data_frame : pd.dataframe
            Tabular data containing variables to be evaluated with standard
            column names and rows of sample data.
        independent_variables : Boolean or list of strings; default False
            list with column names to select from data_frame
            being characterized as independent variables (= environment)
        dependent_variables : Boolean or list of strings; default is False
            list with column names to select from data_frame
            being characterized as dependent variables (= species)
        n_comp : int, default is 2
            Number of components to report
        verbose : Boolean, The default is False.
           Set to True to get messages in the Console about the status of the run code.

    Output
    ------
        results : Dictionary
            containing the scores and loadings of the PCA,
            the percentage of the variation explained by the first principal components,
            the correlation coefficient between the first two PCs,
            names of columns (same length as loadings)
            names of indices (same length as scores)
    """
    if verbose:
        print('==============================================================')
        print(" Running function 'pca()' on data")
        print('==============================================================')

    data,cols= check_data_frame(data_frame)

    if independent_variables is False and dependent_variables is False:
        data_pca = data
        names_independent = cols
        names_dependent = []

    elif independent_variables is not False and dependent_variables is False:
        names_independent = extract_variables(cols,
                              independent_variables,
                              name_variables = 'independent variables'
                              )
        names_dependent = []
        data_pca = data[names_independent]
    elif independent_variables is False and dependent_variables is not False:
        names_dependent = extract_variables(cols,
                              dependent_variables,
                              name_variables = 'dependent variables'
                              )
        names_independent = []
        data_pca = data[names_dependent]

    else:
        names_independent = extract_variables(cols,
                              independent_variables,
                              name_variables = 'independent variables'
                              )
        names_dependent = extract_variables(cols,
                              dependent_variables,
                              name_variables = 'dependent variables'
                              )
        data_pca = data[names_independent + names_dependent]

    # Checking if the dimensions of the dataframe allow for PCA
    if data_pca.shape[0] < data_pca.shape[1]:
        raise ValueError("PCA not possible with more variables than samples.")

    try:
        # Using scikit.decomposoition.PCA with an amount of components equal
        # to the amount of variables, then getting the loadings, scores and explained variance ratio.
        pca = decomposition.PCA(n_components=len(data_pca.columns))
        pca.fit(data_pca)
        loadings = pca.components_.T
        PCAscores = pca.transform(data_pca)
        variances = pca.explained_variance_ratio_
    except(ValueError,TypeError):
        raise TypeError("Not all column values are numeric values (or NaN). Consider standardizing data first.")

    # Taking the first two PC for plotting
    if dependent_variables is False:
        loadings_independent = loadings[:, 0:n_comp]
        loadings_dependent = np.array([[],[]]).T
    else:
        loadings_independent = loadings[:-len(names_dependent), 0:n_comp]
        loadings_dependent = loadings[-len(names_dependent):, 0:n_comp]
    scores = PCAscores[:, 0:n_comp]
    percent_explained = np.around(100*variances/np.sum(variances), decimals=2)
    coef = np.corrcoef(scores[:,0], scores[:,1])[0,1]

    if verbose:
        print("Information about the success of the PCA:")
        print('----------------------------------------------------------------')
        for i in range(len(percent_explained)):
            print('Principle component {} explains {}% of the total variance.'.format(i,percent_explained[i]))
        print('\nThe correlation coefficient between PC1 and PC2 is {:.2e}.'.format(coef))
        print('----------------------------------------------------------------')

    results = {"method": 'pca',
               "loadings_dependent": loadings_dependent,
               "loadings_independent": loadings_independent,
               "names_independent" : names_independent,
               "names_dependent" : names_dependent,
               "scores": scores,
               "sample_index" : list(data_pca.index),
               "percent_explained": percent_explained,
               "corr_PC1_PC2": coef,
               }

    return results

def cca(data_frame,
        independent_variables,
        dependent_variables,
        n_comp = 2,
        verbose = False,
        ):
    """Function that performs Canonical Correspondence Analysis.

    Function makes use of skbio.stats.ordination.CCA on the input data and gives
    the site scores and loadings.

    Input
    -----
        data_frame : pd.dataframe
            Tabular data containing variables to be evaluated with standard
            column names and rows of sample data.
        independent_variables : list of strings
            list with column names data to be the independent variables (=environment)
        dependent_variables : list of strings
            list with column names data to be the dependen variables (=species)
        n_comp : int, default is 2
            number of dimensions to return
        verbose : Boolean, The default is False.
            Set to True to get messages in the Console about the status of the run code.

    Output
    ------
        results : Dictionary
            * method: name of ordination method (str)
            * loadings_independent: loadings of independent variables (np.ndarray)
            * loadings_dependent: loadings of dependent variables (np.ndarray)
            * names_independent: names of independent varialbes (list of str)
            * names_dependent: names of dependent varialbes (list of str)
            * scores: scores (np.ndarray)
            * sample_index: names of samples (list of str)
    """
    if verbose:
        print('==============================================================')
        print(" Running function 'cca()' on data")
        print('==============================================================')

    results = constrained_ordination(data_frame,
                           independent_variables,
                           dependent_variables,
                           method = 'cca',
                           n_comp = n_comp,
                           )
    return results

def rda(data_frame,
        independent_variables,
        dependent_variables,
        n_comp = 2,
        verbose = False,
        ):
    """Function that performs Redundancy Analysis.

    Function makes use of skbio.stats.ordination.RDA on the input data and gives
    the site scores and loadings.

    Input
    -----
        data_frame : pd.dataframe
            Tabular data containing variables to be evaluated with standard
            column names and rows of sample data.
        independent_variables : list of strings
            list with column names data to be the independent variables (=envirnoment)
        dependent_variables : list of strings
            list with column names data to be the dependent variables (=species)
        n_comp : int, default is 2
            number of dimensions to return
        verbose : Boolean, The default is False.
            Set to True to get messages in the Console about the status of the run code.

    Output
    ------
        results : Dictionary
            * method: name of ordination method (str)
            * loadings_independent: loadings of independent variables (np.ndarray)
            * loadings_dependent: loadings of dependent variables (np.ndarray)
            * names_independent: names of independent varialbes (list of str)
            * names_dependent: names of dependent varialbes (list of str)
            * scores: scores (np.ndarray)
            * sample_index: names of samples (list of str)
    """
    if verbose:
        print('==============================================================')
        print(" Running function 'rda()' on data")
        print('==============================================================')

    results = constrained_ordination(data_frame,
                           independent_variables,
                           dependent_variables,
                           method = 'rda',
                           n_comp = n_comp,
                           )
    return results


def constrained_ordination(data_frame,
                           independent_variables,
                           dependent_variables,
                           method = 'cca',
                           n_comp = 2,
        ):
    """Function that performs constrained ordination.

    Function makes use of skbio.stats.ordination on the input data and gives
    the scores and loadings.

    Input
    -----
        data_frame : pd.DataFrame
            Tabular data containing variables to be evaluated with standard
            column names and rows of sample data.
        independent_variables : list of strings
           list with column names data to be the independent variables (=environment)
        dependent_variables : list of strings
           list with column names data to be the dependen variables (=species)
        method : string, default is cca
            specification of ordination method of choice. Options 'cca' & 'rda'
        n_comp : int, default is 2
            number of dimensions to return

    Output
    ------
        results : Dictionary
            * method: name of ordination method (str)
            * loadings_independent: loadings of independent variables (np.ndarray)
            * loadings_dependent: loadings of dependent variables (np.ndarray)
            * names_independent: names of independent varialbes (list of str)
            * names_dependent: names of dependent varialbes (list of str)
            * scores: scores (np.ndarray)
            * sample_index: names of samples (list of str)
    """
    data,cols= check_data_frame(data_frame)

    intersection = extract_variables(cols,
                          independent_variables,
                          name_variables = 'independent variables'
                          )
    data_independent_variables = data[intersection]

    intersection = extract_variables(cols,
                          dependent_variables,
                          name_variables = 'dependent variables'
                          )
    data_dependent_variables = data[intersection]

    # Checking if the dimensions of the dataframe allow for CCA
    if (data_dependent_variables.shape[0] < data_dependent_variables.shape[1]) or \
        (data_independent_variables.shape[0] < data_independent_variables.shape[1]):
        raise ValueError("Ordination method {} not possible with more variables than samples.".format(method))

    # Performing constrained ordination using function from scikit-bio.
    if method == 'cca':
        try:
            sci_ordination = sciord.cca(data_dependent_variables, data_independent_variables, scaling = n_comp)
        except(TypeError,ValueError):
            raise TypeError("Not all column values are numeric values. Consider standardizing data first.")
    elif method == 'rda':
        try:
            sci_ordination = sciord.rda(data_dependent_variables, data_independent_variables, scaling = n_comp)
        except(TypeError,ValueError):
            raise TypeError("Not all column values are numeric values. Consider standardizing data first.")
    else:
        raise ValueError("Ordination method {} not a valid option.".format(method))

    loadings_independent = sci_ordination.biplot_scores.to_numpy()[:,0:n_comp]
    loadings_dependent = sci_ordination.features.to_numpy()[:,0:n_comp]
    scores = sci_ordination.samples.to_numpy()[:,0:n_comp]

    if loadings_independent.shape[1]<n_comp:
        raise ValueError("Number of dependent variables too small.")

    results = {"method": method,
               "loadings_dependent": loadings_dependent,
               "loadings_independent": loadings_independent,
               "names_independent" : data_independent_variables.columns.to_list(),
               "names_dependent" : data_dependent_variables.columns.to_list(),
               "scores": scores,
               "sample_index" : list(data.index),
               }

    return results

def extract_variables(columns,
                      variables,
                      name_variables = 'variables'
                      ):
    """Checking overlap of two given list.

    Function is used for checking if a list of variables is present in
    the column names of a given dataframe (of quantities for data analysis)

    Input
    -----
        columns: list of strings
            given extensive list (usually column names of a pd.DataFrame)
        variables: list of strings
            list of names to extract/check overlap with strings in list 'column'
        name_variables: str, default is 'variables'
            name of type of variables given in list 'variables'

    Output
    ------
        intersection: list
            list of strings present in both lists 'columns' and 'variables'

    """
    if isinstance(variables,list):
        intersection = list(set(columns) & set(variables))
        remainder = list(set(variables) - set(columns))
        if len(intersection) == 0:
            raise ValueError("No column names for '{}' identified in columns of dataframe.".format(name_variables))
        elif len(intersection) < len(variables):
            print("WARNING: not all column names for '{}' are found in dataframe.".format(name_variables))
            print('----------------------------------------------------------------')
            print("Columns used in analysis:", intersection)
            print("Column names not identified in data:", remainder)
            print('________________________________________________________________')
    else:
        raise ValueError("List of column names for '{}' empty or in wrong format.".format(name_variables))

    return intersection

