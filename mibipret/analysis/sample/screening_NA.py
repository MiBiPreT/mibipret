#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Routines for calculating natural attenuation potential.

@author: Alraune Zech
"""

import numpy as np
import pandas as pd
import mibipret.data.names_data as names
from mibipret.data.check_data import check_data_frame
from mibipret.data.set_data import determine_quantities
from mibipret.data.set_data import extract_settings
from .properties import properties


def reductors(
    data_frame,
    ea_group = 'ONS',
    include = False,
    verbose = False,
    **kwargs,
    ):
    """Calculate the amount of electron reductors [mmol e-/l].

    making use of imported molecular mass values for quantities in [mg/mmol]

    Input
    -----
        data: pd.DataFrame
            concentration values of electron acceptors in [mg/l]
        ea_group: str
            Short name for group of electron acceptors to use
            default is 'ONS' (for oxygen, nitrate, and sulfate)
        include: bool, default False
            Whether to modify the DataFrame rather than creating a new one.
        verbose: Boolean
            verbose flag (default False)

    Output
    ------
        tot_reduct: pd.Series
        Total amount of electrons needed for reduction in [mmol e-/l]
    """
    if verbose:
        print('==============================================================')
        print(" Running function 'reductors()' on data")
        print('==============================================================')

    ### check on correct data input format and extracting column names as list
    data,cols= check_data_frame(data_frame,inplace = include)

    ### sorting out which columns in data to use for summation of electrons available
    quantities = determine_quantities(cols,name_list = ea_group, verbose = verbose)

    ### actually performing summation
    try:
        tot_reduct = 0.
        for ea in quantities:
            tot_reduct += properties[ea]['factor_stoichiometry']* data[ea]/properties[ea]['molecular_mass']
    except TypeError:
        raise ValueError("Data not in standardized format. Run 'standardize()' first.")

    tot_reduct.rename(names.name_total_reductors,inplace = True)
    if verbose:
        print("Total amount of electron reductors per well in [mmol e-/l] is:\n{}".format(tot_reduct))
        print('----------------------------------------------------------------')

    ### additing series to data frame
    if include:
        data[names.name_total_reductors] = tot_reduct

    return tot_reduct

def oxidators(
    data_frame,
    contaminant_group = "BTEXIIN",
    nutrient = False,
    include = False,
    verbose = False,
    **kwargs,
    ):
    """Calculate the amount of electron oxidators [mmol e-/l].

    Calculate the amount of electron oxidators in [mmol e-/l]
    based on concentrations of contaminants, stiochiometric ratios of reactions,
    contaminant properties (e.g. molecular masses in [mg/mmol])

    alternatively: based on nitrogen and phosphate availability

    Input
    -----
        data: pd.DataFrame
            Contaminant contentrations in [ug/l], i.e. microgram per liter
            if nutrient is True, data also needs to contain concentrations
            of Nitrate, Nitrite and Phosphate
        contaminant_group: str
            Short name for group of contaminants to use
            default is 'BTEXIIN' (for benzene, toluene, ethylbenzene, xylene,
                                  indene, indane and naphthaline)
        nutrient: Boolean
            flag to include oxidator availability based on nutrient supply
            calls internally routine "available_NP()" with data
        inplace: bool, default False
            Whether to modify the DataFrame rather than creating a new one.
        verbose: Boolean
            verbose flag (default False)

    Output
    ------
        tot_oxi: pd.Series
            Total amount of electrons oxidators in [mmol e-/l]
    """
    if verbose:
        print('==============================================================')
        print(" Running function 'oxidators()' on data")
        print('==============================================================')

    ### check on correct data input format and extracting column names as list
    data,cols= check_data_frame(data_frame,inplace = include)

    ### sorting out which columns in data to use for summation of electrons available
    quantities = determine_quantities(cols,name_list = contaminant_group, verbose = verbose)

    ### actually performing summation
    if nutrient:
        NP_avail = available_NP(data)

    try:
        tot_oxi = 0.
        for cont in quantities:
            # tot_oxi += data[cont]*0.001/properties[cont]['molecular_mass']*
                #properties[cont]['factor_stoichiometry']
            if nutrient:
                nut_avail = 1000.*NP_avail*properties[cont]['molecular_mass']/(properties[cont]['cs']*12.)
                c_min = nut_avail.combine(data[cont], min, 0) # mass concentration in ug/l
            else:
                c_min = data[cont]

            cm_cont = c_min* 0.001/properties[cont]['molecular_mass'] # molar concentration in mmol/l

            tot_oxi += cm_cont *  properties[cont]['factor_stoichiometry']
    except TypeError:
        raise ValueError("Data not in standardized format. Run 'standardize()' first.")

    tot_oxi.rename(names.name_total_oxidators,inplace = True)
    if verbose:
        print("Total amount of oxidators per well in [mmol e-/l] is:\n{}".format(tot_oxi))
        print('-----------------------------------------------------')

    ### additing series to data frame
    if include:
        data[names.name_total_oxidators] = tot_oxi

    return tot_oxi

def available_NP(
        data_frame,
        include = False,
        verbose = False,
        **kwargs,
        ):
    """Function calculating available nutrients.

    Approximating the amount of hydrocarbons that can be degraded based
    on the amount of nutrients (nitrogen and phosphate available)

    Input
    -----
        data_frame: pd.DataFrame
            nitrate, nitrite and phosphate concentrations in [mg/l]
        include: bool, default False
            Whether to modify the DataFrame rather than creating a new one.
        verbose: Boolean
            verbose flag (default False)

        Output
        ------
        NP_avail: pd.Series
            The amount of nutrients for degrading contaminants

    """
    if verbose:
        print('==============================================================')
        print(" Running function 'available_NP()' on data")
        print('==============================================================')

    ### check on correct data input format and extracting column names as list
    data,cols= check_data_frame(data_frame,inplace = include)

    nutrient_list = [names.name_nitrate, names.name_nitrite, names.name_phosphate]
    list_nut_miss = []

    for nut in nutrient_list:
        if nut not in cols:
            list_nut_miss.append(nut)
    if len(list_nut_miss)>0:
        raise ValueError("Concentrations of nutrient(s) missing:", list_nut_miss)

    CNs = (data[names.name_nitrate] + data[names.name_nitrite]) * (39. / 4.5)
    CPs = data[names.name_phosphate] * (39. / 1.)
    NP_avail =CNs.combine(CPs, min, 0)
    NP_avail.name = names.name_NP_avail

    if include:
        data[names.name_NP_avail] = NP_avail

    if verbose:
        print("Total NP available is:\n{}".format(NP_avail))
        print('----------------------')

    return NP_avail

def electron_balance(
        data_frame,
        include = False,
        verbose = False,
        **kwargs,
        ):
    """Decision if natural attenuation is taking place.

    Function to calculate electron balance, based on electron availability
    calculated from concentrations of contaminant and electron acceptors

    Input
    -----
        data_frame: pd.DataFrame
            tabular data containinng "total_reductors" and "total_oxidators"
                -total amount of electrons available for reduction [mmol e-/l]
                -total amount of electrons needed for oxidation [mmol e-/l]
        include: bool, default False
            Whether to modify the DataFrame rather than creating a new one.
        verbose: Boolean
            verbose flag (default False)

    Output
    ------
        e_bal : pd.Series
            Ratio of electron availability: electrons available for reduction
            devided by electrons needed for oxidation

    """
    if verbose:
        print('==============================================================')
        print(" Running function 'electron_balance()' on data")
        print('==============================================================')

    ### check on correct data input format and extracting column names as list
    data,cols= check_data_frame(data_frame,inplace = include)

    if names.name_total_reductors in cols:
        tot_reduct = data[names.name_total_reductors]
    else:
        tot_reduct = reductors(data,**kwargs)

    if names.name_total_oxidators in cols:
        tot_oxi = data[names.name_total_oxidators]
    else:
        tot_oxi = oxidators(data,**kwargs)

    e_bal = tot_reduct.div(tot_oxi, axis=0)
    e_bal.name = names.name_e_balance

    if include:
        data[names.name_e_balance] = e_bal

    if verbose:
        print("Electron balance e_red/e_cont is:\n{}".format(e_bal))
        print('---------------------------------')

    return e_bal

def NA_traffic(
        data_frame,
        include = False,
        verbose = False,
        **kwargs,
        ):
    """Function evaluating if natural attenuation (NA) is ongoing.

    Function to calculate electron balance, based on electron availability
    calculated from concentrations of contaminant and electron acceptors.

    Input
    -----
        data_frame: pd.DataFrame
            Ratio of electron availability
        include: bool, default False
            Whether to modify the DataFrame rather than creating a new one.
        verbose: Boolean
            verbose flag (default False)

    Output
    ------
        traffic : pd.Series
            Traffic light (decision) based on ratio of electron availability

    """
    if verbose:
        print('==============================================================')
        print(" Running function 'NA_traffic()' on data")
        print('==============================================================')

    ### check on correct data input format and extracting column names as list
    data,cols= check_data_frame(data_frame,inplace = include)

    if names.name_e_balance in cols:
        e_balance = data[names.name_e_balance]
    else:
        e_balance = electron_balance(data,**kwargs)

    e_bal = e_balance.values
    traffic = np.where(e_bal<1,"red","green")
    traffic[np.isnan(e_bal)] = "y"

    NA_traffic = pd.Series(name =names.name_na_traffic_light,
                           data = traffic,
                           index = e_balance.index
                           )

    if include:
        data[names.name_na_traffic_light] = NA_traffic

    if verbose:
        print("Evaluation if natural attenuation (NA) is ongoing:")#" for {}".format(contaminant_group))
        print('--------------------------------------------------')
        print("Red light: Reduction is limited at {} out of {} locations".format(
            np.sum(traffic == "red"),len(e_bal)))
        print("Green light: Reduction is limited at {} out of {} locations".format(
            np.sum(traffic == "green"),len(e_bal)))
        print("Yellow light: No decision possible at {} out of {} locations".format(
            np.sum(np.isnan(e_bal)),len(e_bal)))
        print('________________________________________________________________')

    return NA_traffic

def screening_NA(
    data_frame,
    ea_group = 'ONS',
    contaminant_group = "BTEXIIN",
    nutrient = False,
    include = False,
    verbose = False,
    **kwargs,
    ):
    """Calculate the amount of electron reductors [mmol e-/l].

    making use of imported molecular mass values for quantities in [mg/mmol]

    Input
    -----
        data_frame: pd.DataFrame
            Concentration values of
                - electron acceptors in [mg/l]
                - contaminants in [ug/l]
                - nutrients (Nitrate, Nitrite and Phosphate) if nutrient is True
        ea_group: str, default 'ONS'
            Short name for group of electron acceptors to use
            'ONS' stands for oxygen, nitrate, sulfate and ironII
        contaminant_group: str, default 'BTEXIIN'
            Short name for group of contaminants to use
            'BTEXIIN' stands for benzene, toluene, ethylbenzene, xylene,
                                   indene, indane and naphthaline
        nutrient: Boolean, default False
            flag to include oxidator availability based on nutrient supply
            calls internally routine "available_NP()" with data
        include: bool, default False
            Whether to modify the DataFrame rather than creating a new one.
        verbose: Boolean, default False
            verbose flag

    Output
    ------
        na_data: pd.DataFrame
            Tabular data with all quantities of NA screening listed per sample
    """
    if verbose:
        print('==============================================================')
        print(" Running function 'screening_NA()' on data")
        print('==============================================================')

    ### check on correct data input format and extracting column names as list
    data,cols= check_data_frame(data_frame,inplace = include)

    tot_reduct = reductors(data,
                           ea_group = ea_group,
                           include = include,
                           verbose = verbose)
    tot_oxi = oxidators(data,
                        contaminant_group = contaminant_group,
                        nutrient = nutrient,
                        include = include,
                        verbose = verbose)
    e_bal = electron_balance(data,
                             include = include,
                             verbose = verbose)
    na_traffic = NA_traffic(data,
                            contaminant_group = contaminant_group,
                            include = include,
                            verbose = verbose)

    list_new_quantities = [tot_reduct,tot_oxi,e_bal,na_traffic]
    if nutrient:
        NP_avail = available_NP(data,
                                include = include,
                                verbose = verbose)
        list_new_quantities.append(NP_avail)

    if include is False:
       na_data = extract_settings(data)

       for add in list_new_quantities:
           na_data.insert(na_data.shape[1], add.name, add)
    else:
        na_data = data

    return na_data
