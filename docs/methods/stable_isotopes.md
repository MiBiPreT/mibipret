# `mibipret` Stable Isotope Analysis

## General

`stable_isotope_regression` provides tools for stable isotope analysis by linear regression, including calculation and visualization. 
[Polerecky, 2023]:

## Keeling regression: 

Applying the function `Keeling_regression()` performs a linear regression linked to the Keeling plot which is an approach to identify the isotopic composition of a contaminating source from measured concentrations and isotopic composition (delta) of a target species in the mix of the source and a pool. It is based on the linear relationship of the given quantities (concentration) and delta-values which are measured over time or across a spatial interval.

Results can be visualized with the function `Keeling_plot()`. Its input is streamlined with the output created by the analysis routine `Keeling_regression()`. The plot shows the inverse concentration data against the delta-values along the linear regression line.

## Lambda regression: 

Applying the routine `Lambda_regression()` provides *Lambda* value based on linear regression: The Lambda values relates the $\delta 13C$ versus $\delta 2H$ signatures of a chemical compound. Relative changes in the ratio can indicate the occurrence of specific enzymatic degradation reactions. The analysis is based on a linear regression of the hydrogen versus carbon isotope signatures. The parameter of interest, the Lambda values is the slope of the the linear trend line. 

Results can be visualized with the routine `Lambda_plot()`. It shows the δ13C versus δ2H signatures of a chemical compound. Its input is streamlined with the output created by the analysis routine.

## Rayleigh fractionation

Rayleigh fractionation analysis using `Rayleigh_fractionation()` is a common application to characterize the removal of a substance from a finite pool using stable isotopes. It is based on the change in the isotopic composition of the pool due to different kinetics of the change in lighter and heavier isotopes. The analysis is based on a linear regression of the log-transformed concentration data against the delta-values. The parameter of interest, the kinetic fractionation factor of the removal process is the slope of the linear trend line. 

Results can be visualized with `Rayleigh_fractionation_plot()` whose input is streamlined with the output created by the analysis routine.



