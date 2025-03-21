# `mibipret` Data handling

## General

We designed data handling for field sample data typical for biodegradation processes. This data includes
* sample specification data, 
* contaminant concentrations, focusing on petroleum hydrocarbons, 
* hydrogeochemical data and habitat conditions, e.g. redox potential, pH, electron acceptor concentrations, such as oxygen, nitrate, sulfate
* microbiome data (i.e. the occurrence of DNA and functional genes), 
* metabolite data (i.e. intermediate products of the degradation process)
* measurements on stable isotope fractions (particularly for hydrogen and carbon within the sample and/or of individual contaminant)

Data has to be provided in a standardized form. 

Data transformation is implemented in functions performing:
* loading data from csv or excel files
* check of input data on 
    * correct units provided
    * numerical values
* standardisation, e.g. of column names to standard names
* selection of data

A workflow of data handling is illustrated for the Griftpark data (folder ex01_Griftpark) in the jupyter-notebook “example_01_grift_data.ipynb”. 
