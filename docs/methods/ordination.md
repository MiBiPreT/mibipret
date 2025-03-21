# `mibipret` Ordination

## General

`ordination` provides tools for multivariate statistics to calculate and visualize 
the interactions between any kind of data measured in the field, including 
contaminants, environmental factors, metabolite concentration and microbiota counts. 

The general goal of ordination methods is to reduce the dimensionality of the data by 
arranging it along novel axes. Typically, two axis are used that represent the 
main gradients of the data. Then, the variables are evaluated by their correlation 
with these new axes. For each type of data correlation a different ordination method is defined. 

Ordination methods can be subdivided in two types, unconstrained and constrained. 
Unconstrained ordination methods do not use any prior information about the data 
and treat each type of variable similarly. `ordination` provides the unconstrained 
method *Principal Component Analysis* (PCA). Constrained ordination uses prior 
knowledge of the data, differentiating between explanatory (or independent) variables
and response (or dependent) variables. `ordination` provides two constrained 
ordination methods: *Redundancy Analysis* (RDA) and *Canonical Correspondence Analysis* (CCA).
In the context of bioremediation, the explanatory variables are typically the environmental 
variables. The response variables are typically the species variables, e.g. 
microbiotic species or proxies for microbiotic species. 

Ordination methods produce scores, called loadings, for the variables and scores 
for the measurement locations (referred to as sites). For constrained ordination methods, 
there are separate loadings for the dependent and the independent variables. 
In unconstrained ordination, there is no such separation in the loadings. 

### Principle of PCA

PCA determines the ordination axes by maximizing the amount of variance explained 
by each axis. In other words, it minimizes the total amount of residual variation per axis,
by minimizing the amount of variation not explained by the particular axis. This 
results in a number of new axes equaling the number of variables. 

The first two axes can then be used for plotting and represent the data in two 
uncorrelated directions that explain most of the variation in the data. 
The dissimilarity in the data is measured as Euclidean distance. 

### Principle of constrained ordination

Constrained ordination maximizes correlation between the independent and dependent 
variables. The implemented methods RDA and CCA are canonical ordination techniques, made to 
detect patterns in the dependent variables by the independent variables. 

RDA bases its axes on the same principles as PCA, by maximizing the total variance 
for each axis. Like PCA, it is used when the assumed relationship between the
independent and dependent variables is linear. 

CCA bases its axes on a different principle. CCA determines the axes that maximizes 
the amount of dispersion/independence among variables, measured as chi-squared distance. 
It is used when the assumed relationship between the data is unimodal, i.e. the data 
having a probability distribution with a single peak. 

### Ordination plots

Results of all ordination analysis can be visualized with `plot ordination_plot()`.
It creates ordination plot based on the results of the ordination analysis routines 
`pca()`, `cca()`, or `rda()`. The output of the analysis routines is streamlined and 
can directly be used as input to the visualization routine.

The two plot axis represent the two main axis identified by the ordination methods. 
The first ordination axis is oriented horizontally and the second vertically. 
The variable loadings are represented in the plot as arrows starting in the origin. 
The site scores shown as dots represent the coordinates of the sites in the new ordination axes.

While various axis scaling is possible, axes are generally between the minimal 
value of -1 and the maximum value of 1. Positive scores or loadings indicate 
positive correlation with the axis, where negative values indicate negative 
correlation. For example, a variable with negative loadings for the first two 
ordination axes is anticorrelated with the two largest trends in the data.

The direction of the arrow reflecting variable loading indicates to which ordination 
axis it correlates. The length of the vector is equivalent to the extent of that 
correlation. Thus arrows pointing in the same direction indicate that the variable 
are correlated. Arrows at an right angle to one another are uncorrelated.
Arrows that point in opposite directions are anti-correlated. 
A vector very close to the origin shows little to no correlation with the axes.
Proximity of the site scores in the plot indicate the similarity between 
the sample sites. 

Ordination plots are biplots, when two different elements are displayed, this are 
e.g. variable loadings and site scores for unconstrained methods or dependent and 
independent variable loadings in constrained methods. When loadings and
site scores are displayed in constrained methods, they are called a triplot.

### Data Transformation

There are various ways to transform the data before ordination analysis:
* centered: for each sample value of a variable $x_i$ the mean of the variable over all samples
$\mu$ is subtracted: $z_i = x_i − \mu$
* standardize: $z_i = \frac{x_i - \mu}{\sigma}$ where $\sigma$ is the standard deviation 
of the variable over all samples.
* log transformed: $z_i = \log( A x_i + B)$ where $A$ and $B$ scaling parameters 
(typically chosen $A =1$ and $B=1$)

Note that logarithmic transformation is performed before standardization or centering, 
since logarithms give no solution for negative values.

[not yet implemented] 
Samples or variables can be designated as supplementary. Then the values will not considered during ordnation analysis, but their scores and loadings relative to the axes will be determined for visualization.  After performing the ordination analysis, data can be scaled or transformed again, for the purpose of plotting preferences. Scaling can be focused on either variable or sample distance. 

