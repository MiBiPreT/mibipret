"""Tests for the ordination plots in mibipret.visualize module.

@author: Alraune Zech
"""

import matplotlib.pyplot as plt
import numpy as np
import pytest
from mibipret.visualize.ordination_plot import ordination_plot


class TestOrdinationPlot:
    """Class for testing ordination plots of mibipret."""

    pca_output_01 = {
        'method': 'pca',
        'loadings_independent': np.array([[ 0.99999675, -0.002548  ],[-0.002548  , -0.99999675]]),
        'loadings_dependent': [],
        'names_independent': ['nitrate', 'oxygen'],
        'names_dependent': [],
        'scores': np.array([[ 4.44999192e+01, -8.83862725e-02],
                            [-7.25012298e+01, -3.90267822e-01],
                            [-7.44991849e+01,  4.14825590e-01],
                            [ 1.02500495e+02,  6.38285042e-02]]),
        'sample_index': ['2000-001', '2000-002', '2000-003', '2000-004'],
        'percent_explained': np.array([100.,   0.]),
        'corr_PC1_PC2': 2.587839267904467e-17
        }

    pca_output_02 = {
        'method': 'pca',
        'loadings_independent': [],
        'loadings_dependent': np.array([[ 0.99999675, -0.002548  ],[-0.002548  , -0.99999675]]),
        'names_dependent': ['nitrate', 'oxygen'],
        'names_independent': [],
        'scores': np.array([[ 4.44999192e+01, -8.83862725e-02],
                            [-7.25012298e+01, -3.90267822e-01],
                            [-7.44991849e+01,  4.14825590e-01],
                            [ 1.02500495e+02,  6.38285042e-02]]),
        'sample_index': ['2000-001', '2000-002', '2000-003', '2000-004'],
        'percent_explained': np.array([100.,   0.]),
        'corr_PC1_PC2': 2.587839267904467e-17
        }

    cca_output_01 = {
        'method': 'cca',
        'loadings_dependent': np.array([[-1.55077018e-01,  4.70442169e-04],
               [ 3.55879473e-01, -3.72142498e-01],
               [ 8.14223408e-01,  2.77055931e-03]]),
        'loadings_independent': np.array([[ 0.73838654,  0.64988839],
               [-0.83773509,  0.26245953],
               [-0.54517573,  0.29924283],
               [ 0.21397886,  0.67168236]]),
        'names_independent': ['nitrate', 'oxygen', 'ironII', 'sulfate'],
        'names_dependent': ['naphthalene', 'toluene', 'benzene'],
        'scores': np.array([[-0.40987246,  1.32585167],
               [-0.98163421,  0.24972093],
               [ 0.16585265, -1.44306525],
               [ 1.76833504,  0.67352295]]),
        'sample_index': ['2000-001', '2000-002', '2000-003', '2000-004']
        }

    def test_ordination_plot_01(self):
        """Testing routine ordination_plot().

        Testing Error message that input data not in required data format.
        """
        with pytest.raises(TypeError):
               # match="Input data must be given as dictionary with standard output of ordination methods."):
            ordination_plot([1,2,3])

    def test_ordination_plot_02(self):
        """Testing routine ordination_plot().

        Testing Error message that input dictionary does not contain all required data.
        """
        test ={key:value for key, value in self.pca_output_01.items() if key != 'loadings_independent'}

        with pytest.raises(KeyError):
               # match="Input dictionary does not contain data on loadings ('loadings_independent')\n"):
            ordination_plot(test)

    def test_ordination_plot_03(self):
        """Testing routine ordination_plot().

        Testing Error message that input dictionary does not contain all required data.
        """
        test ={key:value for key, value in self.pca_output_01.items() if key != 'scores'}

        with pytest.raises(KeyError):
               # match="Input dictionary does not contain data on scores ('scores')\n"):
            ordination_plot(test)

    def test_ordination_plot_04(self):
        """Testing routine ordination_plot().

        Testing that routine produces a plot when data is provided as dictionary
        of pca data without dependent variables.
        And standard plot settings.
        """
        fig, ax = ordination_plot(self.pca_output_01)

        assert isinstance(fig,plt.Figure)
        plt.close(fig)

    def test_ordination_plot_05(self):
        """Testing routine ordination_plot().

        Testing that routine produces a plot when data is provided as dictionary
        of pca data without independent variables.
        And standard plot settings.
        """
        fig, ax = ordination_plot(self.pca_output_02)

        assert isinstance(fig,plt.Figure)
        plt.close(fig)

    def test_ordination_plot_06(self):
        """Testing routine ordination_plot().

        Testing that routine produces a plot when data is provided as dictionary
        of cca data with independent and dependent variables.
        And standard plot settings.
        """
        fig, ax = ordination_plot(self.cca_output_01)

        assert isinstance(fig,plt.Figure)
        plt.close(fig)


    def test_ordination_plot_07(self):
        """Testing routine ordination_plot().

        Testing that routine produces a plot when data is provided as dictionary
        of pca data with optional keys (sample index and dependent_variables).
        And standard plot settings.
        """
        test ={key:value for key, value in self.pca_output_01.items() if key not
               in ["sample_index",'loadings_dependent']}
        fig, ax = ordination_plot(test)

        assert isinstance(fig,plt.Figure)
        plt.close(fig)

    def test_ordination_plot_08(self):
        """Testing routine ordination_plot().

        Testing keyword 'axis_ranges' and adjust_test.
        """
        fig, ax = ordination_plot(self.cca_output_01,
                                  axis_ranges = [-2,2,-2,2],
                                  adjust_text = False,
                                  )

        assert isinstance(fig,plt.Figure)
        plt.close(fig)

    def test_ordination_plot_09(self):
        """Testing routine ordination_plot().

        Testing keyword 'plot_loadings' and adjust_test.
        """
        fig, ax = ordination_plot(self.cca_output_01,
                                  plot_loadings = False,
                                  )

    def test_ordination_plot_10(self):
        """Testing routine ordination_plot().

        Testing keyword 'plot_scores'.
        """
        fig, ax = ordination_plot(self.cca_output_01,
                                  plot_scores = False,
                                  )

        assert isinstance(fig,plt.Figure)
        plt.close(fig)

    def test_ordination_plot_11(self):
        """Testing routine ordination_plot().

        Testing keyword 'rescale_loadings_scores'.
        """
        fig, ax = ordination_plot(self.cca_output_01,
                                  rescale_loadings_scores = True,
                                  )

        assert isinstance(fig,plt.Figure)
        plt.close(fig)

    def test_ordination_plot_12(self):
        """Testing routine ordination_plot().

        Testing keyword 'scale_focus'.
        """
        fig, ax = ordination_plot(self.cca_output_01,
                                  plot_loadings = True,
                                   plot_scores = True,
                                   scale_focus = "scores",
                                  )

        assert isinstance(fig,plt.Figure)
        plt.close(fig)

    def test_ordination_plot_13(self,capsys):
        """Testing routine ordination_plot().

        Testing keyword save_fig. Checks output of Warning that given file path
        does not match for writing figure to file.
        """
        save_fig = '../dir_does_not_exist/file.png'
        out_text = "WARNING: Figure could not be saved. Check provided file path and name: {}\n".format(save_fig)
        ordination_plot(self.pca_output_01,save_fig = save_fig)
        out,err=capsys.readouterr()

        assert out==out_text
