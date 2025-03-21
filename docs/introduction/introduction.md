# Introduction

## General

Contaminated sites pose a risk to humands and the environment. Innovative cleaning technologies are needed to remediate these sites and remove contaminants such as petroleum hydrocarbons (PHC), cyanides and hexachlorocyclohexane (HCH).

Conventional methods of contaminated site remediation are often costly and upkeep intensive. Bioremediation is an alternative of particular interest, as it degrades contaminants on-site. Assessment of ongoing biodegradation is an important step to check the feasibility for bioremediation. Similarly, modeling the fate of contaminants is key for understanding the processes involved and predicting bioremediation in the field. 

Detailed data analysis of field measurements, such as sampling data on contaminant concentrations, environmental conditions (such as pH), geo-chemical parameters (such as concentrations of oxygen, nitrate, sulfate etc) is the starting point for identifying the status of the site, assessing feasibility of bioremediation and designing remediation options. For instance, multivariate statistical analysis of field observation data can provide guidance on feasibility of bioremediation by evaluating the amount of biodegradation taking place. 

Numerical simulation can provide valuable knowledge on the processes occurring on site, like groundwater flow and contaminant transport including geo-chemical processes like adsorption and biodegradation. Combining simulations on groundwater flow, contaminant transport and chemical reactions allows making predictions on amounts, locations and time scales of biodegradation as well as measures of bioremediation. A combination of (statistical) data-analysis of observational data with predictions by numerical simulations, is a promising option for decision support on bioremediation for field sites. 

The purpose of this package is to process, analyse and visualize biogeochemical and hydrogeological (field) data relevant for biodegredation and bioremediation. `mibiret` is the central repository within the GitHub organization MiBiPreT for data handling, basic data analysis and diagnostic plotting.

## MIBIREM

[MIBIREM - Innovative technological toolbox for bioremediation](https://www.mibirem.eu/) is a EU funded consortium project by 12 international partners all over Europe working together to develop an *Innovative technological toolbox for bioremediation*. The project will develop molecular methods for the monitoring, isolation, cultivation and subsequent deposition of whole microbiomes. The toolbox will also include the methodology for the improvement of specific microbiome functions, including evolution and enrichment. The performance of selected microbiomes will be tested under real field conditions. The `mibipret` package is part of this toolbox.

## Bioremediation

Bioremediation uses living organisms (including bacteria) to digest and neutralize environmental contaminants. Like the microbiome in the gut, which supports the body in digesting food, microbiomes at contaminanted sites can degrade organic contaminant in soil and groundwater.

Processes relevant for general biodegradation and bioremediation prediction are:
+ hydrogeological flow and transport: this includes groundwater flow driven by hydraulic gradients, advective transport of contaminant, diffusion and dispersion
+ transformation and phase transition processes: dissolution, volatilization, adsorption/retardation, decay
+ biochemical processes: chemical reaction and microbial degradation
+ microbiome evolution: spatial distribution and temporal development of bacteria actively degrading contaminants under various and/or changing environmental conditions.

Modeling all these processes at the same time, requires a high level of model detail, spatially resolved parameter information and knowledge on initial and boundary conditions. This is typically not feasible in the field. Thus, we follow the approach to select and combine most relevant processes and have modeling sub-modules (repositories within the MiBiPreT organization) which can be used for data analysis and predictive modeling of individual or combined processes. At the same time, modules are designed to allow for coupling of processes and (modeling) sub-modules at a advanced stage of tool development.

## Example Field data

We gathered field data from two sites for development and testing of implemented routines on field sample data:
* the Griftpark site [Faber, 2023]
* the VetGas Amersfoort site [van Leeuwen et al., 2020, 2022]

Both sites are heavily contaminated with petroleum hydrocarbons. Sampling campaigns and extensive sample analysis produced data on contaminant concentrations, geochemical conditions, metabolite concentrations, and isotope data. 

## Structure

The core elements and folders for users of `mibipret` are:
* The folder `mibipret` contains the main functionality split up into folders for:
    * `data`
    * `analysis` 
    * `visualization`
* The folder `examples` contains example workflows in the form of Jupyter-Notebooks outlining application of functionality on example data from:
  * Griftpark: `ex01_Griftpark`
  * Vetgas Amersfoort: `ex02_Amersfoort`


