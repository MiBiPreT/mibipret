# `mibipret` Methods Overview

Methods implemented for data analysis reflect the basic standards for data analysis and visualisation of field sampling data typically gathered during field remediation efforts. This includes:

## Analysis of electron balance for natural attenuation (NA) screening

Evaluating the potential and extent of biodegradation going on at a site based on relating concentrations of contaminants and electron acceptors. When concentrations of environmental conditions (oxygen, etc) and concentrations of contaminants (e.g. benzene, naphtalene) are provided in tabular (standard) form the routines reductors() and oxidators() can be used to determine the total amount electrons available for reduction and needed for oxidation are calculated per sample. The routine electron_balance() put that into ratio and the routine NA_traffic() provides a “traffic light” indication: Red corresponds to an electron balance below 1 where available electrons for reduction are not sufficient and thus NA is potentially not taking place. Green corresponds to an electron balance above 1 indicating that NA is potentially taking place. Yellow corresponds to a case where information is not sufficient for an evaluation. 

Results can be visualized in an activity plot.

## Threshold concentrations
Routines for identifying threshold concentrations allows evaluating if a site poses a risk and which contaminant is exceeding regulatory limits. When concentrations of
of contaminants are provided in tabular (standard) form the routine total_contaminant_concentration() provides the total amount or that of a
selected subgroup of contaminants for each sample. The function thresholds_for_intervention() identifies for each sample those contaminants that exceed intervention thresholds. Again a traffic light system (red/yellow/green) indicates if the sample requires intervention. It further provides the number of contaminants exceeding the intervention value and a list of contaminants above the threshold of intervention.

## Metabolite analysis 
Evaluating the occurrence of metabolites can serve as indicator for ongoing biodegradation. When metabolite data is provided in tabular (standard) form
the routines total_concentration() and total_count() can be used to determine the total amount per sample (in microgram) and the total amount of
quantities exceeding a certain threshold value, e.g. exceeding zero concentration for identifying the total number of observed metabolites. The gained information can be
stored in the data frame and used for visualization in an activity plot. 

## Stable isotope analysis
Performing linear regression of stable isotope measurements, particularly of carbon 13 and deuterium for particular contaminants can provide information on changes of in the contaminant source or the occurrence of specific enzymatic degradation reactions. 

##  Multivariate statistical analysis: Ordination
Workflows for multivariate statistical analysis of observational data (contaminant concentrations, habitat conditions,
microbiome data, and/or metabolite data) identifying correlations between these quantities. Three ordination methods are available: Principal Component Analysis
pca(), Canonical Correspondence Analysis cca() and Redundancy Analysis rda().

Output of the ordination methods is input for diagnostic plots (implemented in visualization).

Example workflows of the analysis methods are implemented for the example data from the Vetgas Amersfoort site and the Griftpark field site and can be found in notebooks in the folders ex01_Griftpark and ex02_Amersfoort.
