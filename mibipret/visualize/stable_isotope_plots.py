#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Linear regression plots for stable isotope analysis in mibipret.

@author: Alraune Zech
"""
import copy
# import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

DEF_settings = dict(
    figsize = [3.75,2.8],
    fontsize = 10,
    marker = 'o',
    markersize = 45,
    fit_color = 'red',
    intercept_color = 'forestgreen',
    loc = 'best',
    dpi = 300,
    )

def Lambda_plot(delta_C,
                delta_H,
                coefficients,
                save_fig = False,
                **kwargs,
                ):
    """Creating a Lambda plot.

    A Lambda plot shows the δ13C versus δ2H signatures of a chemical compound.
    Relative changes in the carbon and hydrogen isotope ratios can indicate the
    occurrence of specific enzymatic degradation reactions. The relative changes
    are indicated by the lambda-H/C value which is the slope of the linear
    regression of hydrogen versus carbon isotope signatures. For gaining the
    regression coefficients perform a linear fitting or run

         Lambda_regression() [in the module analysis]

    Lambda-values linking to specific enzymatic reactions:
        To be added!

    Details provided in Vogt et al. [2016, 2020].

    References:
        C. Vogt, C. Dorer, F. Musat, and H. H. Richnow. Multi-element isotope
        fractionation concepts to characterize the biodegradation of hydrocarbons
        - from enzymes to the environment. Current Opinion in Biotechnology,
        41:90–98, 2016.
        C. Vogt, F. Musat, and H.-H. Richnow. Compound-Specific Isotope Analysis
        for Studying the Biological Degradation of Hydrocarbons. In Anaerobic
        Utilization of Hydrocarbons, Oils, and Lipids, pages 285-321.
        Springer Nature Switzerland, 2020.

        A. Fischer, I. Herklotz, S. Herrmann, M. Thullner, S. A. Weelink,
        A. J. Stams, M. Schl ̈omann, H.-H. Richnow, and C. Vogt. Combined Carbon
        and Hydrogen Isotope Fractionation Investigations for Elucidating
        Benzene Biodegradation Pathways. Environmental Science and Technology,
        42:4356–4363, 2008.

        S. Kuemmel, F.-A. Herbst, A. Bahr, M. Arcia Duarte, D. H. Pieper,
        N. Jehmlich, J. Seifert, M. Von Bergen, P. Bombach, H. H. Richnow,
        and C. Vogt. Anaerobic naphthalene degradation by sulfate-reducing
        Desulfobacteraceae from various anoxic aquifers.
        FEMS Microbiology Ecology, 91(3), 2015.

    Input
    -----
        delta_C : np.array, pd.series
            relative isotope ratio (delta-value) of carbon of target molecule
        delta_H : np.array, pd.series (same length as delta_C)
            relative isotope ratio (delta-value) of hydrogen of target molecule
        coefficients : tuple of lenght 2
            containing coefficients of the linear fit
        save_fig: Boolean or string, optional, default is False.
            Flag to save figure to file with name provided as string.
        **kwargs: dict
            dictionary with plot settings

    Returns:
    --------
        fig : Figure object
            Figure object of created activity plot.
        ax :  Axes object
            Axes object of created activity plot.

    """
    settings = copy.copy(DEF_settings)
    settings.update(**kwargs)

    fig, ax = plt.subplots(figsize=settings['figsize'])
    ax.scatter(delta_C, delta_H, marker=settings['marker'],zorder = 3,label= 'data')

    ### ---------------------------------------------------------------------------
    ### plot linear regression trend line

    polynomial = np.poly1d(coefficients)
    trendline_x = np.linspace(np.min(delta_C), np.max(delta_C), 100)
    trendline_y = polynomial(trendline_x)
    ax.plot(trendline_x, trendline_y, color= settings['fit_color'], label='linear fit')
    ax.text(0.4, 0.1,
             r"$\Lambda = {:.2f}$".format(coefficients[0]),
             bbox=dict(boxstyle="round", facecolor='w'),#,alpha=0.5),
             transform=ax.transAxes,
             fontsize=settings['fontsize'])
    ### ---------------------------------------------------------------------------
    ### Adapt plot optics

    ax.grid(True,zorder = 0)
    ax.set_xlabel(r'$\delta^{{13}}$C')
    ax.set_ylabel(r'$\delta^2$H')
    ax.legend(loc =settings['loc'], fontsize=settings['fontsize'])
    fig.tight_layout()

    ### ---------------------------------------------------------------------------
    ### Save figure to file if file path provided
    if save_fig is not False:
        try:
            plt.savefig(save_fig,dpi = settings['dpi'])
            print("Save Figure to file:\n", save_fig)
        except OSError:
            print("WARNING: Figure could not be saved. Check provided file path and name: {}".format(save_fig))

    return fig,ax

def Rayleigh_fractionation_plot(concentration,
                                delta,
                                coefficients,
                                save_fig = False,
                                **kwargs,
                                ):
    """Creating a Rayleigh fractionation plot.

    Rayleigh fractionation is a common application to characterize the removal
    of a substance from a finite pool using stable isotopes. It is based on the
    change in the isotopic composition of the pool due to different kinetics of
    the change in lighter and heavier isotopes.

    We follow the most simple approach assuming that the substance removal follows
    first-order kinetics, where the rate coefficients for the lighter and heavier
    isotopes of the substance differ due to kinetic isotope fractionation effects.
    The isotopic composition of the remaining substance in the pool will change
    over time, leading to the so-called Rayleigh fractionation.

    The plot shows the log-transformed concentration data against the delta-values
    along the linear regression line. For gaining the regression coefficients
    perform a linear fitting or run

        Rayleigh_fractionation() [in the module analysis]

    The parameter of interest, the kinetic fractionation factor (epsilon or alpha -1)
    of the removal process is the slope of the the linear trend line.

    Input
    -----
        concentration : np.array, pd.series
            total molecular mass/molar concentration of target substance
            at different locations (at a time) or at different times (at one location)
        delta : np.array, pd.series (same length as concentration)
            relative isotope ratio (delta-value) of target substance
        coefficients : tuple of lenght 2
            containing coefficients of the linear fit
        save_fig: Boolean or string, optional, default is False.
            Flag to save figure to file with name provided as string. =
        **kwargs: dict
            dictionary with plot settings

    Returns:
    --------
        fig : Figure object
            Figure object of created activity plot.
        ax :  Axes object
            Axes object of created activity plot.

    """
    settings = copy.copy(DEF_settings)
    settings.update(**kwargs)

    x = np.log(concentration)
    ### ---------------------------------------------------------------------------
    ### create plot
    fig, ax = plt.subplots(figsize=settings['figsize'])
    ax.scatter(x,delta, marker=settings['marker'], zorder = 3,label = 'data')

    ### ---------------------------------------------------------------------------
    ### plot linear regression trend line

    polynomial = np.poly1d(coefficients)
    trendline_x = np.linspace(np.min(x), np.max(x), 100)
    trendline_y = polynomial(trendline_x)
    ax.plot(trendline_x, trendline_y, color= settings['fit_color'], label='linear fit')
    ax.text(0.1, 0.1,
             r"$\epsilon = 1-\alpha = {:.3f}$".format(coefficients[0]),
             bbox=dict(boxstyle="round", facecolor='w'),#,alpha=0.5),
             transform=ax.transAxes,
             fontsize=settings['fontsize'])

    ### ---------------------------------------------------------------------------
    ### Adapt plot optics

    ax.set_xlabel(r'log-concentration $\ln c$',fontsize=settings['fontsize'])
    ax.set_ylabel(r'$\delta$',fontsize=settings['fontsize'])
    ax.grid(True,zorder = 0)
    ax.legend(loc =settings['loc'], fontsize=settings['fontsize'])
    fig.tight_layout()

    ### ---------------------------------------------------------------------------
    ### Save figure to file if file path provided
    if save_fig is not False:
        try:
            plt.savefig(save_fig,dpi = settings['dpi'])
            print("Save Figure to file:\n", save_fig)
        except OSError:
            print("WARNING: Figure could not be saved. Check provided file path and name: {}".format(save_fig))

    return fig,ax

def Keeling_plot(concentration,
                 delta,
                 coefficients,
                 relative_abundance = None,
                 save_fig = False,
                 **kwargs,
                 ):
    """Creating a Keeling plot.

    A Keeling plot is an approach to identify the isotopic composition of a
    contaminating source from measured concentrations and isotopic composition
    (delta) of a target species in the mix of the source and a pool. It is based
    on the linear relationship of the concentration and the delta-value
    which are measured over time or across a spatial interval.

    The plot shows the inverse concentration data against the delta-values
    along the linear regression line. For gaining the regression coefficients
    perform a linear fitting or run

        Keeling_regression() [in the module analysis]

    The parameter of interest, the delta (or relative_abundance, respectively)
    of the source quantity is the intercept of linear fit with the y-axis,
    or in other words, the absolute value of the linear fit function.

    Input
    -----
        c_mix : np.array, pd.dataframe
            total molecular mass/molar concentration of target substance
            at different locations (at a time) or at different times (at one location)
        delta_mix : np.array, pd.dataframe (same length as c_mix)
            relative isotope ratio (delta-value) of target substance
        relative_abundance : None or np.array, pd.dataframe (same length as c_mix), default None
            if not None it replaces delta_mix in the inverse estimation and plotting
            relative abundance of target substance
        coefficients : tuple of lenght 2
            containing coefficients of the linear fit
        save_fig: Boolean or string, optional, default is False.
            Flag to save figure to file with name provided as string. =
        **kwargs: dict
            dictionary with plot settings

    Returns:
    --------
        fig : Figure object
            Figure object of created activity plot.
        ax :  Axes object
            Axes object of created activity plot.

    """
    settings = copy.copy(DEF_settings)
    settings.update(**kwargs)

    if relative_abundance is not None:
        y = relative_abundance
        text = 'x'
    else:
        y = delta
        text = r"\delta"

    x = 1/concentration

    ### ---------------------------------------------------------------------------
    ### create plot
    fig, ax = plt.subplots(figsize=settings['figsize'])
    ax.scatter(x,y, marker=settings['marker'], zorder = 3,label = 'data')

    ### ---------------------------------------------------------------------------
    ### plot linear regression trend line

    polynomial = np.poly1d(coefficients)
    trendline_x = np.linspace(min(0,np.min(x)),np.max(x), 100)
    trendline_y = polynomial(trendline_x)

    ax.plot(trendline_x, trendline_y, color= settings['fit_color'], label='linear fit')
    ax.text(0.5, 0.1,
            r"${}_{{source}} = {:.3f}$".format(text,coefficients[1]),
             bbox=dict(boxstyle="round", facecolor='w'),#,alpha=0.5)
             transform=ax.transAxes,
             fontsize=settings['fontsize'])
    ax.scatter(0,coefficients[1],
               c = settings['intercept_color'],
               zorder = 3,
               label = r'intercept: ${}_{{source}}$'.format(text),
               )

    ### ---------------------------------------------------------------------------
    ### Adapt plot optics

    ax.set_xlabel('Inverse concentration $1/c$',fontsize=settings['fontsize'])
    ax.set_ylabel('${}$'.format(text),fontsize=settings['fontsize'])
    ax.grid(True,zorder = 0)
    ax.set_xlim([0-x[-1]*0.05, x[-1]*1.05])
    ax.legend(loc =settings['loc'], fontsize=settings['fontsize'])
    fig.tight_layout()

    ### ---------------------------------------------------------------------------
    ### Save figure to file if file path provided
    if save_fig is not False:
        try:
            plt.savefig(save_fig,dpi = settings['dpi'])
            print("Save Figure to file:\n", save_fig)
        except OSError:
            print("WARNING: Figure could not be saved. Check provided file path and name: {}".format(save_fig))

    return fig,ax
