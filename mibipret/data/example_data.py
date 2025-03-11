#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Example dat.

Measurements on quantities and parameters in groundwater samples
used for biodegredation and bioremediation analysis.

@author: Alraune Zech
"""

import numpy as np
import pandas as pd
import mibipret.data.names_data as names
from mibipret.data.unit_settings import standard_units


def example_data(data_type = 'all',
                 with_units = False,
                 ):
    """Function provinging test data for mibipret data analysis.

    Args:
    -------
        data_type: string
            Type of data to return:
                -- "all": all types of data available
                -- "set_env_cont": well setting, environmental and contaminants data
                -- "setting": well setting data only
                -- "environment": data on environmental
                -- "contaminants": data on contaminants
                -- "metabolites": data on metabolites
                -- "isotopes": data on isotopes
                -- "hydro": data on hydrogeolocial conditions
        with_units: Boolean, default False
            flag to provide first row with units
            if False (no units), values in columns will be numerical
            if True (with units), values in columns will be objects

    Returns:
    -------
        pandas.DataFrame: Tabular data with standard column names

    Raises:
    -------
        None

    Example:
    -------
        To be added!
    """
    mgl = standard_units['mgperl'][0]
    microgl = standard_units['microgperl'][0]

    setting = [names.name_sample,names.name_observation_well,names.name_sample_depth]
    setting_units = [' ',' ',standard_units['meter'][0]]
    setting_s01 = ['2000-001', 'B-MLS1-3-12', -12.]
    setting_s02 = ['2000-002', 'B-MLS1-5-15', -15.5]
    setting_s03 = ['2000-003', 'B-MLS1-6-17', -17.]
    setting_s04 = ['2000-004', 'B-MLS1-7-19', -19.]

    environment = [names.name_pH,
                   names.name_EC,
                   names.name_redox,
                   names.name_oxygen,
                   names.name_nitrate,
                   names.name_nitrite,
                   names.name_sulfate,
                   names.name_ammonium,
                   names.name_sulfide,
                   names.name_methane,
                   names.name_ironII,
                   names.name_manganese,
                   names.name_phosphate]

    environment_units = [' ',standard_units['microsimpercm'][0],standard_units['millivolt'][0],
                         mgl,mgl,mgl,mgl,mgl,mgl,mgl,mgl,mgl,mgl]
    environment_s01 = [7.23, 322., -208.,0.3,122.,0.58, 23., 5., 0., 748., 3., 1.,1.6]
    environment_s02 = [7.67, 405., -231.,0.9,5.,0.0, 0., 6., 0., 2022., 1., 0.,0]
    environment_s03 = [7.75, 223., -252.,0.1,3.,0.03, 1., 13., 0., 200., 1., 0.,0.8]
    environment_s04 = [7.53, 58., -317.,0., 180.,1., 9., 15., 6., 122., 0., 0.,0.1]

    contaminants = [names.name_benzene,
                    names.name_toluene,
                    names.name_ethylbenzene,
                    names.name_pm_xylene,
                    names.name_o_xylene,
                    names.name_indane,
                    names.name_indene,
                    names.name_naphthalene]

    contaminants_units = [microgl,microgl,microgl,microgl,
                          microgl,microgl,microgl,microgl]
    contaminants_s01 = [263., 2., 269., 14., 51., 1254., 41., 2207.]
    contaminants_s02 = [179., 7., 1690., 751., 253., 1352., 15., 5410.]
    contaminants_s03 = [853., 17., 1286., 528., 214., 1031., 31., 3879.]
    contaminants_s04 = [1254., 10., 1202., 79., 61., 814., 59., 1970.]

    metabolites = [names.name_phenol,
                   names.name_cinnamic_acid,
                   names.name_benzoic_acid]

    metabolites_units = [microgl,microgl,microgl]
    metabolites_s01 = [0.2, 0.4, 1.4]
    metabolites_s02 = [np.nan, 0.1, 0.]
    metabolites_s03 = [0., 11.4, 5.4]
    metabolites_s04 = [0.3, 0.5, 0.7]

    # isotopes = ['delta_13C-benzene','delta_2H-benzene']
    isotopes = [names.name_13C+'-'+names.name_benzene,
                names.name_2H+'-'+names.name_benzene,
                ]

    isotopes_units = [standard_units['permil'][0],standard_units['permil'][0]]
    isotopes_s01 = [-26.1,-106.]
    isotopes_s02 = [-25.8,-110.]
    isotopes_s03 = [-24.1,-118.]
    isotopes_s04 = [-24.1,-117.]

    if  data_type == 'setting':
        data = pd.DataFrame([setting_units,setting_s01,setting_s02,setting_s03,
                             setting_s04],columns = setting)

    elif  data_type == 'environment':
        units = setting_units+environment_units
        columns = setting+environment
        sample_01 = setting_s01+environment_s01
        sample_02 = setting_s02+environment_s02
        sample_03 = setting_s03+environment_s03
        sample_04 = setting_s04+environment_s04

        data = pd.DataFrame([units,sample_01,sample_02,sample_03,sample_04],
                            columns = columns)

    elif  data_type == 'contaminants':
        units = setting_units+contaminants_units
        columns = setting+contaminants
        sample_01 = setting_s01+contaminants_s01
        sample_02 = setting_s02+contaminants_s02
        sample_03 = setting_s03+contaminants_s03
        sample_04 = setting_s04+contaminants_s04

        data = pd.DataFrame([units,sample_01,sample_02,sample_03,sample_04],
                            columns = columns)

    elif  data_type == 'metabolites':

        units = setting_units+metabolites_units
        columns = setting+metabolites
        sample_01 = setting_s01+metabolites_s01
        sample_02 = setting_s02+metabolites_s02
        sample_03 = setting_s03+metabolites_s03
        sample_04 = setting_s04+metabolites_s04

        data = pd.DataFrame([units,sample_01,sample_02,sample_03,sample_04],
                            columns = columns)

    elif  data_type == 'isotopes':

        units = setting_units+isotopes_units
        columns = setting+isotopes
        sample_01 = setting_s01+isotopes_s01
        sample_02 = setting_s02+isotopes_s02
        sample_03 = setting_s03+isotopes_s03
        sample_04 = setting_s04+isotopes_s04

        data = pd.DataFrame([units,sample_01,sample_02,sample_03,sample_04],
                            columns = columns)

    elif data_type == "set_env_cont":

        units = setting_units+environment_units+contaminants_units
        columns = setting+environment+contaminants
        sample_01 = setting_s01+environment_s01+contaminants_s01
        sample_02 = setting_s02+environment_s02+contaminants_s02
        sample_03 = setting_s03+environment_s03+contaminants_s03
        sample_04 = setting_s04+environment_s04+contaminants_s04

        data = pd.DataFrame([units,sample_01,sample_02,sample_03,sample_04],
                            columns = columns)

    elif data_type == 'all':
        units = setting_units+environment_units+contaminants_units+metabolites_units + isotopes_units
        columns = setting+environment+contaminants+metabolites + isotopes
        sample_01 = setting_s01+environment_s01+contaminants_s01+metabolites_s01+isotopes_s01
        sample_02 = setting_s02+environment_s02+contaminants_s02+metabolites_s02+isotopes_s02
        sample_03 = setting_s03+environment_s03+contaminants_s03+metabolites_s03+isotopes_s03
        sample_04 = setting_s04+environment_s04+contaminants_s04+metabolites_s04+isotopes_s04

        data = pd.DataFrame([units,sample_01,sample_02,sample_03,sample_04],
                            columns = columns)

    else:
        raise ValueError("Specified data type '{}' not available".format(data_type))

    if not with_units:
        data.drop(0,inplace = True)
        for quantity in data.columns[2:]:
            data[quantity] = pd.to_numeric(data[quantity])

    return data
