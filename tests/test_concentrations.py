#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Testing analysis module on NA screening of mibipret.

@author: Alraune Zech
"""

import numpy as np
import pandas as pd
import pytest
from mibipret.analysis.sample.concentrations import thresholds_for_intervention
from mibipret.analysis.sample.concentrations import total_concentration
from mibipret.analysis.sample.concentrations import total_contaminant_concentration
from mibipret.analysis.sample.concentrations import total_count
from mibipret.data.example_data import example_data  #, check_values


class TestTotalConcentration:
    """Class for testing analysis module on NA screening of mibipret."""

    columns = ['sample_nr', 'sulfate', 'benzene']
    units = [' ','mg/L', 'ug/L']
    s01 = ['2000-001', 748, 263]
    s02 = ['2000-002', 548, 103]
    s02b = ['2000-002', 548, ]

    data1 = pd.DataFrame([s01,s02],
                         columns = columns)

    data_nonstandard = pd.DataFrame([units,s01,s02b],
                                    columns = columns)


    def test_total_concentration_01(self):
        """Testing routine total_concentration().

        Correct calculation of total amount of contaminants (total concentration).
        """
        out = total_concentration(self.data1).values
        test = self.data1.iloc[:,1:].sum(axis = 1).values
        assert np.all(out == test)

    def test_total_concentration_02(self):
        """Testing routine total_concentration().

        Testing 'include' option adding calculated values as column to data.
        """
        data_test = self.data1.copy()
        total_concentration(data_test,name_list=['sulfate'],include = True).values

        assert data_test.shape[1] == self.data1.shape[1]+1 and \
                np.all(data_test['total concentration selection'] == self.data1['sulfate'])

    def test_total_concentration_03(self):
        """Testing routine total_concentration().

        Correct handling when no overlap of specified list of quantities
        with column names in data frame.
        """
        with pytest.raises(ValueError):
            total_concentration(self.data1,name_list=['test1','test2'])


    def test_total_concentration_04(self):
        """Testing routine total_concentration().

        Correct handling when keywork 'name_colum' is not correctly provided.
        """
        with pytest.raises(ValueError):
            total_concentration(self.data1,
                                name_column = 1,
                                )


    def test_total_concentration_05(self,capsys):
        """Testing routine total_concentration().

        Testing verbose flag.
        """
        total_concentration(self.data1,verbose=True)
        out,err=capsys.readouterr()

        assert len(out)>0

    # def test_total_concentration_06(self):
    #     """Testing Error message that given data type not defined."""
    #     with pytest.raises(ValueError):  #, match = "Data not in standardized format. Run 'standardize()' first."):
    #         total_concentration(data_nonstandard)


class TestTotalContaminantConcentration:
    """Class for testing total concentration of contaminants from module concentation of mibipret."""

    data = example_data(with_units = False)

    def test_total_contaminant_concentration_01(self):
        """Testing routine total_contaminant_concentration().

        Correct calculation of total amount of contaminants (total concentration).
        """
        tot_conc_test = 27046.0
        tot_conc = np.sum(total_contaminant_concentration(self.data))

        assert (tot_conc - tot_conc_test)<1e-5

    def test_total_contaminant_concentration_02(self):
        """Testing routine total_contaminant_concentration().

        Correct calculation of total amount of contaminants (total concentration)
        for BTEX.
        """
        tot_conc_test = 8983.0
        tot_conc = np.sum(total_contaminant_concentration(self.data,contaminant_group='BTEX'))

        assert (tot_conc - tot_conc_test)<1e-5

    def test_total_contaminant_concentration_03(self):
        """Testing routine total_contaminant_concentration().

        Correct handling when unknown group of contaminants are provided.
        """
        with pytest.raises(ValueError):
            total_contaminant_concentration(self.data,contaminant_group = 'test')

class TestTotalCount:
    """Class for testing analysis module on NA screening of mibipret."""

    columns = ['sample_nr', 'sulfate', 'benzene']
    units = [' ','mg/L', 'ug/L']
    s01 = ['2000-001', 748, 263]
    s02 = ['2000-002', 548, ]

    data1 = pd.DataFrame([s01,s02],
                         columns = columns)

    data_nonstandard = pd.DataFrame([units,s01,s02],
                                    columns = columns)


    def test_total_count_01(self):
        """Testing routine total_count().

        Correct calculation of total count of contaminants with concentration > 0.
        """
        out = total_count(self.data1).values

        assert np.all(out == [2,1])

    def test_total_count_02(self):
        """Testing routine total_count().

        Correct calculation of total count of contaminants with concentration > specific threshold.
        """
        out = total_count(self.data1,threshold = 300).values

        assert np.all(out == [1,1])

    def test_total_count_03(self):
        """Testing routine total_count().

        Correct handling when no overlap of specified list of quantities
        with column names in data frame.
        """
        with pytest.raises(ValueError):
            total_count(self.data1,threshold = -1)


    def test_total_count_04(self):
        """Testing routine total_count().

        Testing inplace option adding calculated values as column to data.
        """
        data_test = self.data1.copy()
        total_count(data_test,name_list=['sulfate'],include = True).values

        assert data_test.shape[1] == self.data1.shape[1]+1 and \
                np.all(data_test['total count selection'] == [1,1])

    def test_total_count_05(self):
        """Testing routine total_count().

        Correct handling when no overlap of specified list of quantities
        with column names in data frame.
        """
        with pytest.raises(ValueError):
            total_count(self.data1,name_list=['test1','test2'])

    def test_total_count_06(self):
        """Testing Error message that given data type not defined."""
        with pytest.raises(ValueError):
            total_count(self.data_nonstandard)


    def test_total_count_07(self,capsys):
        """Testing routine total_count().

        Testing verbose flag.
        """
        total_count(self.data1,verbose=True)
        out,err=capsys.readouterr()

        assert len(out)>0

class TestThresholdsForIntervention:
    """Class for testing thresholds_for_intervention() from module concentation of mibipret."""

    data = example_data(with_units = False)

    columns = ['sample_nr', 'sulfate', 'benzene']
    units = [' ','mg/L', 'ug/L']
    s01 = ['2000-001', 748, 263]
    s02b = ['2000-002', 548, ]

    data_nonstandard = pd.DataFrame([units,s01,s02b],
                                    columns = columns)


    def test_thresholds_for_intervention_01(self):
        """Testing routine thresholds_for_intervention().

        Check that routine produced correct dataframe output.
        """
        na_intervention = thresholds_for_intervention(self.data)
        intervention_contaminants_cols = ['sample_nr', 'obs_well', 'depth', 'intervention_traffic',
               'intervention_number', 'intervention_contaminants']

        assert na_intervention.shape == (4,6)
        assert set(na_intervention.columns) == set(intervention_contaminants_cols)

    def test_thresholds_for_intervention_02(self):
        """Testing routine thresholds_for_intervention().

        Correct identification of list of contaminants exceeding
        intervention thresholds.
        """
        na_intervention = thresholds_for_intervention(self.data)
        intervention_contaminants_test = ['benzene', 'ethylbenzene', 'pm_xylene', 'o_xylene', 'indane', 'naphthalene']

        assert set(na_intervention['intervention_contaminants'].iloc[2]) == set(intervention_contaminants_test)

    def test_thresholds_for_intervention_03(self):
        """Testing routine thresholds_for_intervention().

        Correct identification of number of contaminants exceeding
        intervention thresholds.
        """
        na_intervention = thresholds_for_intervention(self.data)
        na_intervention_number_test = 21
        assert (np.sum(na_intervention['intervention_number'].iloc[2]) - na_intervention_number_test)< 1e-5

    def test_thresholds_for_intervention_04(self):
        """Testing routine thresholds_for_intervention().

        Correct evaluation of traffic light on intervention value.
        """
        na_intervention = thresholds_for_intervention(self.data)
        na_intervention_test = ['red','red','red','red']

        assert np.all(na_intervention['intervention_traffic'].values == na_intervention_test)

    def test_thresholds_for_intervention_05(self):
        """Testing routine thresholds_for_intervention().

        Correct handling when unknown group of contaminants are provided.
        """
        with pytest.raises(ValueError):
            thresholds_for_intervention(self.data,contaminant_group = 'test')

    def test_thresholds_for_intervention_06(self):
        """Testing routine thresholds_for_intervention().

        Testing Error message that data is not in standard format.
        """
        with pytest.raises(ValueError):
            thresholds_for_intervention(self.data_nonstandard)

    def test_thresholds_for_intervention_07(self,capsys):
        """Testing routine thresholds_for_intervention().

        Testing Warning that some contaminant concentrations are missing.
        """
        data_test = self.data.drop(labels = 'benzene',axis = 1)
        thresholds_for_intervention(data_test,verbose = False, contaminant_group='BTEX')
        out,err=capsys.readouterr()
        assert len(out)>0

    def test_thresholds_for_intervention_08(self):
        """Testing routine thresholds_for_intervention().

        Testing inplace option adding calculated values as column to data.
        """
        data_test = self.data.copy()
        thresholds_for_intervention(data_test,include = True)
        assert data_test.shape[1] == self.data.shape[1]+3

    def test_thresholds_for_intervention_09(self,capsys):
        """Testing routine thresholds_for_intervention().

        Testing verbose flag.
        """
        thresholds_for_intervention(self.data,verbose=True)
        out,err=capsys.readouterr()

        assert len(out)>0
