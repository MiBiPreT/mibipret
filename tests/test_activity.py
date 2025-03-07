"""Tests for the activity plot in mibipret.visualize module.

@author: Alraune Zech
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pytest
from mibipret.data.names_data import name_metabolites_variety
from mibipret.data.names_data import name_na_traffic_light
from mibipret.data.names_data import name_total_contaminants
from mibipret.visualize.activity import activity


class TestActivity:
    """Class for testing activity plot of mibipret."""

    meta = [41,33,47,20,36]
    conc = [13132.,11695.,4101.,498.,2822]
    traffic = ['red','y','green','green','red']

    meta_pd = pd.Series(data = meta, name = name_metabolites_variety)
    conc_pd = pd.Series(data = conc, name = name_total_contaminants)
    traffic_pd = pd.Series(data = traffic, name = name_na_traffic_light)

    data_01 = pd.concat([meta_pd,conc_pd,traffic_pd],axis = 1)

    data_02 = [conc_pd,traffic_pd,meta_pd]

    data_03 = [np.array(conc),np.array(meta),np.array(traffic)]

    data_04 = [conc,meta,traffic]

    def test_activity_01(self):
        """Testing routine activity().

        Testing that routine produces a plot when data is provided as DataFrame.
        """
        fig, ax = activity(self.data_01)

        assert isinstance(fig,plt.Figure)
        plt.close(fig)

    def test_activity_02(self):
        """Testing routine activity().

        Testing that routine produces a plot when data is provided as list of pd.Series
        """
        fig, ax = activity(self.data_02)

        assert isinstance(fig,plt.Figure)
        plt.close(fig)

    def test_activity_03(self):
        """Testing routine activity().

        Testing that routine produces a plot when data is provided as list of np.arrays
        """
        fig, ax = activity(self.data_03)

        assert isinstance(fig,plt.Figure)
        plt.close(fig)

    def test_activity_04(self):
        """Testing routine activity().

        Testing that routine produces a plot when data is provided as list of lists
        """
        fig, ax = activity(self.data_04)

        assert isinstance(fig,plt.Figure)
        plt.close(fig)

    def test_activity_05(self):
        """Testing routine activity().

        Testing Error message that not sufficient data for a plot.
        """
        with pytest.raises(ValueError,
           match="List elements in data must be lists, np.arrays or pd.series."):
            activity([1,2,3])


    def test_activity_06(self):
        """Testing routine activity().

        Testing Error message that data is not in required format.
        """
        with pytest.raises(ValueError,
           match="Provided arrays/lists/series of data must have the same length."):
            activity([self.conc,self.meta,self.traffic[:-1]])

    def test_activity_07(self):
        """Testing routine activity().

        Testing Error message that data is not in required format.
        """
        with pytest.raises(ValueError,
           match="Data needs to be DataFrame or list of at least three lists/np.arrays/pd.series."):
            activity(self.conc_pd)

    def test_activity_08(self):
        """Testing routine activity().

        Testing Error message that not sufficient data for a plot.
        """
        with pytest.raises(ValueError,
           match="Too little data for activity plot. At least two values per quantity required."):
            activity([[1],[2],[3]])

    def test_activity_09(self,capsys):
        """Testing routine activity().

        Testing Error message that given file path does not match for writing
        figure to file.
        """
        save_fig = '../dir_does_not_exist/file.png'
        out_text = "WARNING: Figure could not be saved. Check provided file path and name: {}\n".format(save_fig)
        activity(self.data_01,save_fig = save_fig)
        out,err=capsys.readouterr()

        assert out==out_text
