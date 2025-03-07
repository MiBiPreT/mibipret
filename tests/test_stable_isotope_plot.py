"""Tests for the stable isotope regression plots in mibipret.visualize module.

@author: Alraune Zech
"""

import matplotlib.pyplot as plt
import numpy as np
from mibipret.visualize.stable_isotope_plots import Keeling_plot
from mibipret.visualize.stable_isotope_plots import Lambda_plot

# import pytest
from mibipret.visualize.stable_isotope_plots import Rayleigh_fractionation_plot


class TestStableIsotopePlot:
    """Class for testing stable isotope regression plots of mibipret."""

    results_Lambda = {
        'delta_C': np.array([-26.5, -26.2, -25.2, -25.7]),
        'delta_H': np.array([-77., -75., -51., -61.]),
        'coefficients': np.array([ 21.2244898 , 483.71428571]),
        }
    results_Rayleigh = {
        'concentration': np.array([2., 1.825, 1.65 , 1.475, 1.3  , 1.125, 0.95 , 0.775, 0.6]),
        'delta': np.array([0.009   , 0.011625, 0.01425 , 0.016875, 0.0195  , 0.022125, 0.02475 , 0.027375, 0.03]),
        'coefficients': np.array([-0.0174713 ,  0.02289195])
        }
    relative_abundance = 0.5*np.array([35., 20., 10.,  7.,  5., 25., 35.])
    results_Keeling = {
        'concentration': np.array([0.05 , 0.075, 0.11 , 0.13 , 0.15 , 0.04 , 0.04 ]),
        'delta': np.array([35., 20., 10.,  7.,  5., 25., 35.]),
        'coefficients': np.array([ 1.44085406, -2.40843306])
        }

    def test_Lambda_plot_01(self):
        """Testing routine Lambda_plot().

        Testing that routine produces a plot when data is provided as dictionary
        of Lambda regression results and standard plot settings.
        """
        fig, ax = Lambda_plot(**self.results_Lambda)

        assert isinstance(fig,plt.Figure)
        plt.close(fig)

    def test_Lambda_plot_02(self,capsys):
        """Testing routine Lambda_plot().

        Testing keyword save_fig. Checks output of Warning that given file path
        does not match for writing figure to file.
        """
        save_fig = '../dir_does_not_exist/file.png'
        out_text = "WARNING: Figure could not be saved. Check provided file path and name: {}\n".format(save_fig)
        Lambda_plot(**self.results_Lambda,
                    save_fig = save_fig)
        out,err=capsys.readouterr()

        assert out==out_text

    def test_Rayleigh_fractionation_plot_01(self):
        """Testing routine Rayleigh_fractionation_plot().

        Testing that routine produces a plot when data is provided as dictionary
        of Lambda regression results and standard plot settings.
        """
        fig, ax = Rayleigh_fractionation_plot(**self.results_Rayleigh)

        assert isinstance(fig,plt.Figure)
        plt.close(fig)

    def test_Rayleigh_fractionation_plot_02(self,capsys):
        """Testing routine Rayleigh_fractionation_plot().

        Testing keyword save_fig. Checks output of Warning that given file path
        does not match for writing figure to file.
        """
        save_fig = '../dir_does_not_exist/file.png'
        out_text = "WARNING: Figure could not be saved. Check provided file path and name: {}\n".format(save_fig)
        Rayleigh_fractionation_plot(**self.results_Rayleigh,
                                    save_fig = save_fig)
        out,err=capsys.readouterr()

        assert out==out_text

    def test_Keeling_plot_01(self):
        """Testing routine Keeling_plot().

        Testing that routine produces a plot when data is provided as dictionary
        of Lambda regression results and standard plot settings.
        """
        fig, ax = Keeling_plot(**self.results_Keeling)

        assert isinstance(fig,plt.Figure)
        plt.close(fig)

    def test_Keeling_plot_02(self):
        """Testing routine Keeling_plot().

        Testing that routine produces a plot when data is provided as dictionary
        of Lambda regression results and standard plot settings.
        """
        fig, ax = Keeling_plot(**self.results_Keeling,
                               relative_abundance = self.relative_abundance)

        assert isinstance(fig,plt.Figure)
        plt.close(fig)

    def test_Keeling_plot_03(self,capsys):
        """Testing routine Keeling_plot().

        Testing keyword save_fig. Checks output of Warning that given file path
        does not match for writing figure to file.
        """
        save_fig = '../dir_does_not_exist/file.png'
        out_text = "WARNING: Figure could not be saved. Check provided file path and name: {}\n".format(save_fig)
        Keeling_plot(**self.results_Keeling,
                     save_fig = save_fig)
        out,err=capsys.readouterr()

        assert out==out_text
