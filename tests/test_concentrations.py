#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Testing analysis module on NA screening of mibipret.

@author: Alraune Zech
"""

import numpy as np
import pandas as pd
import pytest
from mibipret.analysis.sample.concentrations import total_concentration
from mibipret.analysis.sample.concentrations import total_count


class TestTotalConcentration:
    """Class for testing analysis module on NA screening of mibipret."""

    columns1 = ['sample_nr', 'sulfate', 'benzene']
    s01 = ['2000-001', 748, 263]
    s02 = ['2000-002', 548, 103]

    data1 = pd.DataFrame([s01,s02],
                         columns = columns1)


    def test_total_concentration_01(self):
        """Testing routine total_concentration().

        Correct calculation of total amount of contaminants (total concentration).
        """
        out = total_concentration(self.data1).values
        test = self.data1.iloc[:,1:].sum(axis = 1).values
        assert np.all(out == test)

    def test_total_concentration_02(self):
        """Testing routine total_concentration().

        Testing inplace option adding calculated values as column to data.
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


    def test_total_concentration_04(self,capsys):
        """Testing routine total_concentration().

        Testing verbose flag.
        """
        total_concentration(self.data1,verbose=True)
        out,err=capsys.readouterr()

        assert len(out)>0


class TestTotalCount:
    """Class for testing analysis module on NA screening of mibipret."""

    columns1 = ['sample_nr', 'sulfate', 'benzene']
    s01 = ['2000-001', 748, 263]
    s02 = ['2000-002', 548, ]

    data1 = pd.DataFrame([s01,s02],
                         columns = columns1)

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


    def test_total_count_06(self,capsys):
        """Testing routine total_count().

        Testing verbose flag.
        """
        total_count(self.data1,verbose=True)
        out,err=capsys.readouterr()

        assert len(out)>0



