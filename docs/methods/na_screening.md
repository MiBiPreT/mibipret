# `mibipret` Natural Attenuation Screening

## General

`na_screening` provides tools for data analysis regarding ongoing biodegradation. Outcome of this "quick-scan" serve as starting point for evaluating if natural attenuation is a feasible strategy for remediation. The quick-scan is based on technical and scientific analysis of existing data. Goal is to determine whether natural attenuation is occurring and to identify what type of additional data is further necessary to prognosticate long-term behavior of a contaminant plume. The tools for the NA screening are based on the *First traffic light: Quick scan of historical data* as part of the NOBIS-report of Sinke et al., 2001[^1]. The output can serve as decision support, while decisions on whether NA can be applied remain with problem owners and authorities. Relevant aspects in these discussions and decisions, such as political and practical considerations are not included here.


### What is Natural Attenuation (NA)?

*Natural Attenuation*(NA) or *monitored natural attenuation* (MAN) is a strategy for clean-up of contaminated groundwater based on allowing naturally occurring processes to reduce the toxic potential of contaminants. NA does not apply engineered solutions but builds on the recognition that certain subsurface pollutants can degrade naturally without
human intervention under appropriate conditions.

Processes involved in NA:
* hydro(geo)logy: Dilution of contaminant concentrations by spatial spreading due to dispersion and diffusion.
* biology: Reduction of contaminant mass by microbial degradation. 
* geochemistry: Immobilization of contaminants due to chemical reactions and adsorption.

All processes are linked as geochemical composition of the domain impacts microbial activity (availability of electron acceptors for their metabolism) and hydrogeological transport changes concentrations of contaminant, but also electron acceptors in space and time. 

### Assessment criteria
To decide if NA is suitable as remediation strategy, the most important questions that need to be answered are:

1) Does natural degradation of the contamination occur?
2) Is the degradation fast enough compared to the tolerated spread?
3) Is the process complete or is there stagnation in the long term?

If natural degradation of the contamination occurs, it is expected that a stable end situation will be reached in the short or long term. A remediation objective for the subsurface is for instance formulating a period of 30 years to achieve a stable end situation. Specifically, reaching acceptable concentrations of contaminants in the groundwater which are no threat to existing vulnerable objects and/or major impediments to the current or future use of the location or the environment. In many cases, but not always necessarily, there will be a sustainable equilibrium between supply and natural degradation and/or retention. Reaching a stable end situation my include temporary plume expansion. Modeling can help to evaluate for how long a plume will continue to expand until a stationary situation is reached. For the application of natural degradation, this has to be put in relation to the question if degradation is fast enough compared to the tolerated spread. If degradation stagnates, e.g. due to depletion of electron acceptors, with contaminant concentration levels exceeding acceptable levels, then NA is not a sustainable remediation strategy. 

## NA as remediation strategy


The purpose of this *NA screening* is to estimate the physical possibilities for (monitored) NA as a remediation strategy at the earliest possible stage and with the least possible resources/expenses. Simple criteria are used to determine whether location-specific remediation objectives can be achieved within a reasonable time frame.

### Traffic light principle

Data analysis provides decision support information in the form of *traffic lights*. They reflect the chances on natural attenuation as a remediation option: 
* good with green light, 
* fair chance with yellow light, 
* no chance with a red light. 

In case of an yellow traffic light, additional information is needed.

### Requirements

Analysis is based on historical location data. If these are available through reports, no additional effort or costs need to be made. Required information and requirements for sampling setup:
* position of the sampling tubes: measurements must be taken both for the source and in a path parallel to the direction of flow
* measured parameters: contaminant concentrations and the redox paramters.

Starting point is a spreadsheet/dataframe containing structured data. Raw data has to be brought into a template format with support routines provided in `data` to load, clean and standardize the data.
A template spreadsheet can be found at ...to see how data needs to be structured.


### Traffic light evaluation

#### Step 1
For each sample location, first a distinction is made between aerobic and anaerobic conditions. Aerobic conditions are more favorable for the BTEX degradation process, which means that the possibilities for natural degradation are good. Thus, aerobic conditions get `green` light. Anaerobic conditions are less favorable for the degradation process, further evaluation is done in step 2.


#### Step 2
Possibilities for natural attenuation are limited under anaerobic conditions. Monitoring is necessary to determine whether natural degradation occurs. Thus, determine
* concentrations over time 
* redox over time and/or space

#### Step 3

The traffic light assessment is not given per well, but for the **entire location** since it involves considerations of trends. 
Traffic light is determined based on:
* type of contaminant
* whether concentrations decrease over time or 
* whether a relationship exists between BTEX and the redox conditions

If the concentrations clearly decrease over time, or if the redox clearly changes over time and/or space, there is a chance that natural degradation is taking place (yellow traffic light). 
If not, it must be decided that natural degradation is not a good choice (red traffic light). Benzene is very difficult to degrade under anaerobic conditions. So its behavior in relation to the other components must be monitored critically. 

#### Overview

Based on the development of the concentrations over time and/or the changes in redox in space and time, the color of the traffic light at the location can be determined as:

| plume | redox and redox gradient and contamination in space and time      |    probability of NA    |
| ------| ----------------------------------------------------------------- | ------------------------|
| BTEX  | aerobic conditions | green |
| BTEX  | anaerobic conditions, no redox gradient in space or decrease in concentrations in time | red |
| BTEX  | anaerobic conditions, redox gradient in space: from anaerobic in the core zone to aerobic in the plume | yellow |
| BTEX  | anaerobic conditions, concentrations decrease in time | yellow |
| B     | anaerobic conditions, redox gradient in space and concentration gradient in time | yellow |
| TEX   | anaerobic conditions, redox gradient in space and concentration gradient in time | green  |

### Calculations

Calculation of electron balance are based on the redox reactions, including stochiometric relations:

Electrons are consumed through reduction. The reduction reactions for oxygen,
nitrate, and sulfate are:
* Oxygen: $4 e^- + 4 H^+ + 1 O_2 \rightarrow  H_2 O $
* Nitrate: $ 5e^- + 6 H^+ + 1 NO_3^- \rightarrow 3 H_2O + 0.5 N_2 $
* Sulfate: $ 8e^- + 9 H^+ 1 SO_4^{2-} \rightarrow 4H_2O + 1HS^{-} $

Electrons are produced during oxidation of contaminants. Reactions included for selected, typically abundant contaminants are:
* Benzene: $12 H_2O + 1 C_6H_6  \rightarrow 6CO_2 + 30 H^+ + 30e^- $
* Toluene: $14 H_2O + 1 C_7H_8  \rightarrow 7CO_2 + 36 H^+ + 36e^- $
* Ethylbenzene: $16 H_2O + 1 C_8H_{10}  \rightarrow 8CO_2 + 42 H^+ + 42e^- $
* Xylene: $16 H_2O + 1 C_8H_{10}  \rightarrow 8CO_2 + 42 H^+ + 42e^- $
* Indene: $18 H_2O + 1 C_9H_{8}  \rightarrow 9CO_2 + 44 H^+ + 44e^- $
* Indane: $18 H_2O + 1 C_9H_{10}  \rightarrow 9CO_2 + 46 H^+ + 46e^- $
* Naphtalene: $20 H_2O + 1 C_{10}H_{8}  \rightarrow 10CO_2 + 48 H^+ + 48e^- $

Concentrations of the contaminants and redox conditions are divided by their molar mass to transform to molar concentrations.
The total number of electrons is then calculated based on the stoichiometric relation for one liter of solution. Number of electrons 
are added up for all reductors and oxidators per sample location.

### Visualization

The routine `activity()`: provides a visualization of the NA screening in combination with metabolite analysis. 
The activity plot shows the scatter of the total number of metabolites versus the total concentration of contaminants per sample with color
coding of NA traffic lights: red/yellow/green corresponding to no natural attenuation going on (red), limited/unknown NA activity (yellow) 
or active natural attenuation (green).

## References

[^1]: A.J.C. Sinke, T.J. Heimovaara, H. Tonnaer, J. Ter Meer (2001); Beslissingsondersteunend systeem voor de beoordeling van natuurlijke afbraak als sanieringsvariant, 
NOBIS 98-1-21, Gouda

