#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ordination plot.

@author: Alraune Zech
"""

import copy
import matplotlib.pyplot as plt
import numpy as np

DEF_settings = dict(
    figsize = [3.75,3.75],
    title = False,
    label_fontsize = 8,
    loading_fontsize = 8,
    score_fontsize = 6,
    arrow_color_independent = 'blue',
    arrow_color_dependent = 'red',
    fontstyle_independent = 'normal',
    fontstyle_dependent = 'italic',
    weight_independent = "bold",
    weight_dependent = 'normal',
    arrow_width = 0.002,
    arrow_head_width = 0.02,
    arrow_head_length = 0.02,
    score_color = 'gray',
    score_edgecolor = 'gray',
    score_facecolor = 'none',
    score_marker = 'o',
    score_marker_size = 45,
    dpi = 300,
    )

def ordination_plot(ordination_output,
                    plot_loadings = True,
                    plot_scores = True,
                    rescale_loadings_scores = False,
                    adjust_text = True,
                    scale_focus = "loadings",
                    axis_ranges = False,
                    save_fig=False,
                    **kwargs,
                    ):
    """Function creating ordination plot.

    Based on ordination analysis providing ordination loadings and scores.

    Input
    -----
        ordination_output : Dictionary
            contains ordination results:
                - as numpy arrays; ordination loading and scores
                - names of the samples and the Environmental and Species variables
                - method : String (pca, cca, rda) The ordination method used in the analysis.
        plot_loadings : Boolean; default is True
            flag to plot the ordination loadings
        plot_scores : Boolean; default is True
            flag to plot the ordiantion scores
        rescale_loadings_scores : Boolean; default is False
            flag to rescale loadings and scores to have a loading close to 1
        adjust_text : Boolean, default is True
            flag to perform automized adjustment of text labes of loadings and scores to avoid overlap
        scale_focus : String, default is "loadings"
            flag to specify if scaling focusses on either 'loadings' or 'scores' or 'none'.
        axis_ranges : Boolean or list/array of 4 values, default is False,
            if array or list it gives fixed x and y axis dimensions [x_min, x_maxm y_min, y_max]
        save_fig: Boolean or string, optional, default is False.
            Flag to save figure to file with name provided as string.
        **kwargs: dict
            dictionary with plot settings (e.g. fonts, arrow specifics, etc)

    Output
    ------
        fig : Figure object
            Figure object of created activity plot.
        ax :  Axes object
            Axes object of created activity plot.
    """
    settings = copy.copy(DEF_settings)
    settings.update(**kwargs)

    ### ---------------------------------------------------------------------------
    ### check on completeness of input ordination_output

    if not isinstance(ordination_output,dict):
        raise TypeError("Input data must be given as dictionary with standard output of ordination methods.")

    if "loadings_independent" not in ordination_output.keys():
        raise KeyError("Input dictionary does not contain data on loadings ('loadings_independent')")
    else:
        loadings_independent = ordination_output["loadings_independent"]
        names_independent = ordination_output["names_independent"]
        if len(loadings_independent) == 0:
            loadings_independent = np.array([[],[]]).T

    if "scores" not in ordination_output.keys():
        raise KeyError("Input dictionary does not contain data on scores ('scores')")
    else:
        scores = ordination_output["scores"]

    if "sample_index" not in ordination_output.keys():
        sample_index = np.arange(scores.shape[0])
    else:
        sample_index = ordination_output["sample_index"]

    if "loadings_dependent" in ordination_output.keys():
        loadings_dependent = ordination_output["loadings_dependent"]
        names_dependent = ordination_output["names_dependent"]
        if len(loadings_dependent) == 0:
            loadings_dependent = np.array([[],[]]).T
        loadings = np.append(loadings_independent, loadings_dependent, axis=0)
    else:
        loadings = loadings_independent

    ### ---------------------------------------------------------------------------
    ### Rescale ordination_output given plot specifics

    # Determing the largest values in the PCA scores.
    max_load = np.max(np.abs(loadings))
    max_score = np.max(np.abs(scores))

    if max_load > 1 or rescale_loadings_scores:
        # loadings = loadings / (max_load*1.05)
        loadings = loadings / (max_load)
    if max_score > 1 or rescale_loadings_scores:
        # scores = scores / (max_score*1.05)
        scores = scores / (max_score)

    if axis_ranges is not False:
        # Takes the given axis dimensions for both ordination axes
        x_lim_neg,x_lim_pos,y_lim_neg,y_lim_pos = axis_ranges
    else:
        # Adjusts axis dimensions for both ordination axes to ordination_output
        if plot_scores and plot_loadings:
            # When plotting both scores and loadings, scores or loadings are scaled
            # depending on the extent of the other. Depends on the input of Scale_focus.
            if scale_focus == "loadings":
                scores = scores * np.max(np.abs(loadings))
            elif scale_focus == "scores":
                loadings = loadings *  np.max(np.abs(scores))
            full_coords = np.append(loadings, scores, axis=0)
        elif plot_loadings:
            full_coords = loadings
        else:
            full_coords = scores

        x_lim_pos = 0.11*np.ceil(np.max(full_coords[:,0])*10)
        y_lim_pos = 0.11*np.ceil(np.max(full_coords[:,1])*10)
        x_lim_neg = 0.11*np.floor(np.min(full_coords[:,0])*10)
        y_lim_neg = 0.11*np.floor(np.min(full_coords[:,1])*10)

    ### ---------------------------------------------------------------------------
    ### Create Figure, finally!
    fig, ax = plt.subplots(figsize=settings['figsize'])
    texts = []

    # Plotting the ordination scores by iterating over every coordinate
    # in the scores array, if the Plot_scores parameter is set to true.
    if plot_scores:
        for i, (x, y) in enumerate(scores):
            plt.scatter(x, y,
                        color=settings['score_color'],
                        marker = settings['score_marker'],
                        s = settings['score_marker_size'],
                        facecolor=settings['score_facecolor'],
                        edgecolor=settings['score_edgecolor'],
                        zorder = 7,
                        )
            # Plotting the name of the scores and storing it in a list for the purpose of adjusting the position later
            tex = plt.text(x, y, sample_index[i], color='black', fontsize = settings['score_fontsize'],zorder = 9)
            texts.append(tex)

    if plot_loadings:
        # Plots independent (=environmental) and dependent (=species) variables
        # with different colours and text formatting.
        for i, (x, y) in enumerate(loadings_independent):
            plt.arrow(0, 0, x, y,
                      color = settings['arrow_color_independent'],
                      width = settings['arrow_width'],
                      head_length = settings['arrow_head_length'],
                      head_width = settings['arrow_head_width'],
                      zorder = 10,
                      )
            #Plotting the name of the loading
            tex = plt.text(x, y, names_independent[i],
                            color='black',
                            fontstyle = settings['fontstyle_independent'],
                            weight = settings['weight_independent'],
                            fontsize = settings['loading_fontsize'],
                            zorder = 11,
                            )
            texts.append(tex)
        if "loadings_dependent" in ordination_output.keys():
            for i, (x, y) in enumerate(loadings_dependent):
                plt.arrow(0, 0, x, y,
                          color=settings['arrow_color_dependent'],
                          width = settings['arrow_width'],
                          head_length = settings['arrow_head_length'],
                          head_width = settings['arrow_head_width'],
                          zorder = 8,
                          )
                tex = plt.text(x, y, names_dependent[i],
                                color='black',
                                fontstyle = settings['fontstyle_dependent'],
                                weight = settings['weight_dependent'],
                                fontsize = settings['loading_fontsize'],
                                zorder = 9,
                                )
                # and storing it in a list for the purpose of adjusting the position later
                texts.append(tex)

    ### ---------------------------------------------------------------------------
    ### Adapt plot optics

    # Plotting lines that indicate the origin
    plt.plot([-1, 1], [0, 0], color='grey', linewidth=0.75, linestyle='--')
    plt.plot([0, 0], [-1, 1], color='grey', linewidth=0.75, linestyle='--')

    # Setting the x and y axis limits with the previously determined values
    plt.xlim(x_lim_neg, x_lim_pos)
    plt.ylim(y_lim_neg, y_lim_pos)
    plt.tick_params(axis="both",which="major",labelsize=settings['label_fontsize'])

    if ordination_output["method"]=='pca':
        percent_explained = ordination_output["percent_explained"]
        plt.xlabel('PC1 ({:.1f}%)'.format(percent_explained[0]), fontsize = settings['label_fontsize'])
        plt.ylabel('PC2 ({:.1f}%)'.format(percent_explained[1]), fontsize = settings['label_fontsize'])
    else:
        plt.xlabel('ordination axis 1', fontsize = settings['label_fontsize'])
        plt.ylabel('ordination axis 2', fontsize = settings['label_fontsize'])

    if adjust_text:
        try:
            from adjustText import adjust_text
            adjust_text(texts)
        except ImportError:
            print("WARNING: packages 'adjustText' not installed.")
            print(" For making text adjustment, install package 'adjustText'.")

    ### ---------------------------------------------------------------------------
    ### Save figure to file if file path provided

    if isinstance(settings['title'],str):
        plt.title(settings['title'],fontsize = settings['label_fontsize'])

    plt.tight_layout()
    if save_fig is not False:
        try:
            plt.savefig(save_fig,dpi = settings['dpi'])
            print("Figure saved to file:\n", save_fig)
        except OSError:
            print("WARNING: Figure could not be saved. Check provided file path and name: {}".format(save_fig))

    return fig, ax
