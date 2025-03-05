
In the following you could read all the steps to create data pipeline for your project: 

## 1. Data Ingestion (Collection of Raw Data)
This is the first stage, where raw data is gathered from various sources and ingested into the pipeline. It can be structured as per our case (databases, CSV files, APIs, Excels).

```
Discussion point: what type of raw data sources we want to have? I think we need to have databases for microbial data analysis and APIs for recieving fiels measurement data from servers (like the redox measurement data of constucted wetland)
```

#### Examples:
- Batch Data: importing a CSV file of site data regularly like once a day.
- API Data: Pulling real-time data streams from the API.
- Database Extraction: Replicating data from a MySQL database to our own database.


## 2. Data Preprocessing (Cleaning and Standardization)
Before analysis, raw data is often messy and inconsistent. This step ensures data quality, removes duplicates, corrects errors, and formats it for the next processes. This step can be done manually or automated by code.

### Tasks in this stage:
- Check format like the headings and units per column
- Handling missing values (e.g., filling gaps with averages)
- Data deduplication (removing repeated records)
- Converting different formats (e.g., date formats across multiple sources, unit conversion)
- Encoding Data: Create identifiers for the samples name based on their location and country
- Normalization (converting text values to lowercase, trimming spaces, etc.)

#### Examples:
- Standardizing dates from different sources (e.g., converting MM-DD-YYYY to YYYY-MM-DD)
- Convert units to SI units(e.g., pound to Kg, ft to m)
- Removing duplicate sample records from different sources
- Filtering out irrelevant data (e.g., the columns that we don't need)
- Sample name identifier example: NL_GRI_W_1

## 3. Data Transformation (Processing and Enrichment)
In this step, data is converted into a useful format, enriched with additional information, or aggregated for reporting. This step also can be done manually or automated by code.

### Common tasks in this stage:
- Joining Data: Merging datasets from multiple sources
- Data Enrichment: Calculating new values from initial data

#### Examples:
- Merging site measurments data with lab analyized data in one csv file
- Calculating isotop ratio according to Raleigh equation

## 4. Data Storage (Centralized Data Repository)
Once data is transformed, it is stored in an appropriate system depending on the use case.

### Types of Storage:
- Databases like UU YODA, MySQL
- GitHub repository

### Examples:
- Storing processed data in YODA

## 5. Data Validation & Monitoring for Each Data Analysis Module  (Quality Control)
This stage ensures that processed data is accurate, complete, and meets requirements to run different analysis.

### Common Checks:
- Schema validation (ensuring expected columns, required input data or calculated parameters exists)
- Anomaly detection (flagging unexpected values)
- Data freshness checks (ensuring updates occur within expected timeframes)

#### Examples:
- Checking if any contaminant are missing calculated isotope ratios baed on Raliegh equation exist for isoptoppe analysis. 
  - Validating all the concentration values are positive numbers.  
- Monitoring real-time streaming data for sudden spikes in API errors (if we want to recive redox data of Grift park constructed wetlan from online server)

## 6. Data Analytics & Delivery (Insights & Output)
At this stage, we extract insights from processed data, either through graphs or reports.

### Examples:
- Graph: Visualize na_analysis data as traffic lights plotted for each sample
- Graph: creat Rayleigh plots
- Reports: prepare TAUW report
- APIs that serve the processed data to other services or researchers



## End-to-End Example of the Data Pipeline

### Scenario: Python script for data handling

1. **Ingestion:**

```python
# load_data script
import os.path
import numpy as np
import pandas as pd


def load_excel(
        file_path = None,
        sheet_name = 0,
        verbose = False,
        store_provenance = False,
        **kwargs,
        ):
    """Function to load data from excel file.

    Args:
    -------
        file_path: str
            Name of the path to the file
        sheet_name: int
            Number of the sheet in the excel file to load
        verbose: Boolean
            verbose flag
        store_provenance: Boolean
            To add!
        **kwargs: optional keyword arguments to pass to pandas' routine
            read_excel()

    Returns:
    -------
        data: pd.DataFrame
            Tabular data
        units: pd.DataFrame
            Tabular data on units

    Raises:
    -------
        ValueError: If `file_path` is not a valid file location

    Example:
    -------
       This function can be called with the file path of the example data as
       argument using:

        >>> from mibipret.data import load_excel
        >>> load_excel(example_data.xlsx)

    """
    if file_path is None:
        raise ValueError('Specify file path and file name!')
    if not os.path.isfile(file_path):
        raise OSError('Cannot access file at : ',file_path)

    data = pd.read_excel(file_path,
                         sheet_name = sheet_name,
                         **kwargs)
    if ";" in data.iloc[1].iloc[0]:
        data = pd.read_excel(file_path,
                             sep=";",
                             sheet_name = sheet_name,
                             **kwargs)

    units = data.drop(labels = np.arange(1,data.shape[0]))

    if verbose:
        print('==============================================================')
        print(" Running function 'load_excel()' on data file ", file_path)
        print('==============================================================')
        print("Unit of quantities:")
        print('-------------------')
        print(units)
        print('________________________________________________________________')
        print("Loaded data as pandas DataFrame:")
        print('--------------------------------')
        print(data)
        print('================================================================')

    return data, units

def load_csv(
        file_path = None,
        verbose = False,
        store_provenance = False,
        ):
    """Function to load data from csv file.

    Args:
    -------
        file_path: str
            Name of the path to the file
        verbose: Boolean
            verbose flag
        store_provenance: Boolean
            To add!

    Returns:
    -------
        data: pd.DataFrame
            Tabular data
        units: pd.DataFrame
            Tabular data on units

    Raises:
    -------
        ValueError: If `file_path` is not a valid file location

    Example:
    -------
       This function can be called with the file path of the example data as
       argument using:

        >>> from mibipret.data import load_excel
        >>> load_excel(example_data.csv)

    """
    if file_path is None:
        raise ValueError('Specify file path and file name!')
    if not os.path.isfile(file_path):
        raise OSError('Cannot access file at : ',file_path)

    data = pd.read_csv(file_path, encoding="unicode_escape")
    if ";" in data.iloc[1].iloc[0]:
        data = pd.read_csv(file_path, sep=";", encoding="unicode_escape")
    units = data.drop(labels = np.arange(1,data.shape[0]))

    if verbose:
        print('================================================================')
        print(" Running function 'load_csv()' on data file ", file_path)
        print('================================================================')
        print("Units of quantities:")
        print('-------------------')
        print(units)
        print('________________________________________________________________')
        print("Loaded data as pandas DataFrame:")
        print('--------------------------------')
        print(data)
        print('================================================================')

    return data, units
    
```
    
2. **Preprocessing:(Cleaning and Standardization)**
```python
import numpy as np
import pandas as pd
import mibipret.data.names_data as names
import mibipret.data.names_metabolites as names_meta
from mibipret.data.unit_settings import all_units
from mibipret.data.unit_settings import standard_units
from mibipret.data.unit_settings import units_env_cond

to_replace_list = ["-",'--','',' ','  ']
to_replace_value = np.nan
```
# Function transforming list of names to standard names.

Function that looks at the names (of e.g. environmental variables, contaminants,metabolites, isotopes, etc) and provides the corresponding standard names.

```python
def standard_names(name_list,
                   check_metabolites = False,
                   standardize = True,
                   reduce = False,
                   verbose = False,
                   ):
"""Function transforming list of names to standard names.

    Function that looks at the names (of e.g. environmental variables, contaminants,
    metabolites, isotopes, etc) and provides the corresponding standard names.

    Args:
    -------
        name_list: string or list of strings
            names of quantities to be transformed to standard
        check_metabolites: Boolean, default False
            Whether to check on metabolite names
        standardize: Boolean, default False
            Whether to standardize identified column names
        reduce: Boolean, default False
            Whether to reduce data to known quantities
        verbose: Boolean, default True
            verbosity flag

    Returns:
    -------
        tuple: three list containing names of
                list with identitied quantities in data (but not standardized names)
                list with unknown quantities in data (not in list of standardized names)
                list with standard names of identified quantities

    Raises:
    -------
    None (yet).

    Example:
    -------
    Todo's:
        - complete list of potential contaminants, environmental factors
        - add name check for metabolites?
    """

names_standard = []
    names_known = []
    names_unknown = []
    names_transform = {}

    dict_names = names.col_dict.copy()

    if check_metabolites is not False:
        dict_names.update(names_meta.names_metabolites)

    if isinstance(name_list, str):
        name_list = [name_list]
    elif isinstance(name_list, list):
        for name in name_list:
            if not isinstance(name, str):
                raise ValueError("Entry in provided list of names is not a string:", name)

    for x in name_list:
        y = dict_names.get(x, False)
        x_isotope = x.split('-')[0]
        y_isotopes = names.names_isotopes.get(x_isotope.lower(), False)

        if y_isotopes is not False:
            x_molecule = x.removeprefix(x_isotope+'-')
            y_molecule = names.names_contaminants.get(x_molecule.lower(), False)
            if y_molecule is False:
                names_unknown.append(x)
            else:
                y = y_isotopes+'-'+y_molecule
                names_known.append(x)
                names_standard.append(y)
                names_transform[x] = y
        else:
            y = dict_names.get(x.lower(), False)
            if y is False:
                names_unknown.append(x)
            else:
                names_known.append(x)
                names_standard.append(y)
                names_transform[x] = y

    if verbose:
        print('================================================================')
        print(" Running function 'standard_names()'")
        print('================================================================')
        print("{} of {} quantities identified in name list.".format(len(names_known),len(name_list)))
        print("List of names with standard names:")
        print('----------------------------------')
        for i,name in enumerate(names_known):
            print(name," --> ",names_standard[i])
        print('----------------------------------')
        if standardize:
            print("Identified column names have been standardized")
        else:
            print("\nRenaming can be done by setting keyword 'standardize' to True.\n")
        print('________________________________________________________________')
        print("{} quantities have not been identified in provided data:".format(len(names_unknown)))
        print('---------------------------------------------------------')
        for i,name in enumerate(names_unknown):
            print(name)
        print('---------------------------------------------------------')
        if reduce:
            print("Not identified quantities have been removed from data frame")
        else:
            print("\nReduction to known quantities can be done by setting keyword 'reduce' to True.\n")
        print('================================================================')

    if standardize:
        if reduce:
            return names_standard
        else:
            return names_standard + names_unknown
    else:
        return (names_standard, names_known, names_unknown, names_transform)
```        
# Checking data on correct format.

Tests if provided data is a pandas data frame and provides column names.
Optionally it sets the sample name as index.

```python
def check_data_frame(data_frame,
                     sample_name_to_index = False,
                     inplace = False,
                     ):
    """Checking data on correct format.

    Tests if provided data is a pandas data frame and provides column names.
    Optionally it sets the sample name as index.

    Input
    -----
        data_frame: pd.DataFrame
            quantities for data analysis given per sample
        sample_name_to_index:  Boolean, default False
            Whether to set the sample name to the index of the DataFrame
        inplace: Boolean, default False
            Whether to modify the DataFrame rather than creating a new one.

    Output
    ------
        data: pd.DataFrame
            copy of given dataframe with index set to sample name
        cols: list
            List of column names
    """
    if not isinstance(data_frame, pd.DataFrame):
        raise ValueError("Data has to be a panda-DataFrame or Series \
                          but is given as type {}".format(type(data_frame)))

    if inplace is False:
        data = data_frame.copy()
    else:
        data = data_frame

    if sample_name_to_index:
        if names.name_sample not in data.columns:
            print("Warning: No sample name provided for making index. Consider standardizing data first")
        else:
            data.set_index(names.name_sample,inplace = True)

    cols = data.columns.to_list()

    return data, cols
```
# Function checking names of columns of data frame.

Function that looks at the column names and links it to standard names.
Optionally, it renames identified column names to the standard names of the model.

```python
def check_columns(data_frame,
                  check_metabolites = False,
                  standardize = False,
                  reduce = False,
                  verbose = True):
    """Function checking names of columns of data frame.

    Function that looks at the column names and links it to standard names.
    Optionally, it renames identified column names to the standard names of the model.

    Args:
    -------
        data_frame: pd.DataFrame
            dataframe with the measurements
        check_metabolites: Boolean, default False
            Whether to also check on metabolite names
        standardize: Boolean, default False
            Whether to standardize identified column names
        reduce: Boolean, default False
            Whether to reduce data to known quantities
        verbose: Boolean, default True
            verbosity flag

    Returns:
    -------
        tuple: three list containing names of
                list with identitied quantities in data (but not standardized names)
                list with unknown quantities in data (not in list of standardized names)
                list with standard names of identified quantities

    Raises:
    -------
    None (yet).

    Example:
    -------
    Todo's:
        - complete list of potential contaminants, environmental factors
        - add name check for metabolites?
    """
    if verbose:
        print('==============================================================')
        print(" Running function 'check_columns()' on data")
        print('==============================================================')

    data,cols= check_data_frame(data_frame,
                                sample_name_to_index = False,
                                inplace = True)

    results = standard_names(cols,
                             standardize = False,
                             reduce = False,
                             check_metabolites = check_metabolites,
                             verbose = False,
                             )

    column_names_standard = results[0]
    column_names_known = results[1]
    column_names_unknown = results[2]
    column_names_transform = results[3]

    if standardize:
        data.columns = [column_names_transform.get(x, x) for x in data.columns]

    if reduce:
        data.drop(labels = column_names_unknown,axis = 1,inplace=True)

    if verbose:
        print("{} quantities identified in provided data.".format(len(column_names_known)))
        print("List of names with standard names:")
        print('----------------------------------')
        for i,name in enumerate(column_names_known):
            print(name," --> ",column_names_standard[i])
        print('----------------------------------')
        if standardize:
            print("Identified column names have been standardized")
        else:
            print("\nRenaming can be done by setting keyword 'standardize' to True.\n")
        print('________________________________________________________________')
        print("{} quantities have not been identified in provided data:".format(len(column_names_unknown)))
        print('---------------------------------------------------------')
        for i,name in enumerate(column_names_unknown):
            print(name)
        print('---------------------------------------------------------')
        if reduce:
            print("Not identified quantities have been removed from data frame")
        else:
            print("\nReduction to known quantities can be done by setting keyword 'reduce' to True.\n")
        print('================================================================')

    return (column_names_known,column_names_unknown,column_names_standard)
```
# Function to check the units of the measurements.
```python
def check_units(data,
                check_metabolites = False,
                verbose = True):
    """Function to check the units of the measurements.

    Args:
    -------
        data: pandas.DataFrames
            dataframe with the measurements where first row contains
            the units or a dataframe with only the column names and units
        check_metabolites: Boolean, default False
            flag to check on metabolites' units
        verbose: Boolean
            verbose statement (default True)

    Returns:
    -------
        col_check_list: list
            quantities whose units need checking/correction

    Raises:
    -------
        None (yet).

    Example:
    -------
        To be added.
    """
    if verbose:
        print('================================================================')
        print(" Running function 'check_units()' on data")
        print('================================================================')

    if not isinstance(data, pd.DataFrame):
        raise ValueError("Provided data is not a data frame.")
    elif data.shape[0]>1:
        units = data.drop(labels = np.arange(1,data.shape[0]))
    else:
        units = data.copy()

    ### testing if provided data frame contains any unit
    test_unit = False
    for u in all_units:
        if u in units.iloc[0].to_list():
            test_unit = True
            break
    if not test_unit:
        raise ValueError("Error: The second line in the dataframe is supposed\
                         to specify the units. No units were detected in this\
                         line, check www.mibipretdocs.nl/dataloading.")

    # standardize column names (as it might not has happened for data yet)
    check_columns(units,standardize = True, check_metabolites=check_metabolites, verbose = False)
    col_check_list= []

    for quantity in units.columns:
        if quantity in names.chemical_composition:
            if units[quantity][0].lower() not in standard_units['mgperl']:
                col_check_list.append(quantity)
                if verbose:
                    print("Warning: Check unit of {}!\n Given in {}, but must be milligramm per liter (e.g. {})."
                              .format(quantity,units[quantity][0],standard_units['mgperl'][0]))

        if quantity in names.contaminants['all_cont']:
            if units[quantity][0].lower() not in standard_units['microgperl']:
                col_check_list.append(quantity)
                if verbose:
                    print("Warning: Check unit of {}!\n Given in {}, but must be microgramm per liter (e.g. {})."
                              .format(quantity,units[quantity][0],standard_units['microgperl'][0]))

        if quantity in list(units_env_cond.keys()):
            unit_type = units_env_cond[quantity]
            if units[quantity][0].lower() not in standard_units[unit_type]:
                col_check_list.append(quantity)
                if verbose:
                    print("Warning: Check unit of {}!\n Given in {}, but must be in {} (e.g. {}).".format(
                            quantity,units[quantity][0],unit_type,standard_units[unit_type][0]))

        if quantity.split('-')[0] in names.isotopes:
            if units[quantity][0].lower() not in standard_units['permil']:
                col_check_list.append(quantity)
                if verbose:
                    print("Warning: Check unit of {}!\n Given in {}, but must be per mille (e.g. {})."
                              .format(quantity,units[quantity][0],standard_units['permil'][0]))

        if check_metabolites:
            if quantity in names_meta.metabolites['all_meta']:
                if units[quantity][0].lower() not in standard_units['microgperl']:
                    col_check_list.append(quantity)
                    if verbose:
                        print("Warning: Check unit of {}!\n Given in {}, but must be microgramm per liter (e.g. {})."
                                  .format(quantity,units[quantity][0],standard_units['microgperl'][0]))

    if verbose:
        print('________________________________________________________________')
        if len(col_check_list) == 0:
            print(" All identified quantities given in requested units.")
        else:
            print(" All other identified quantities given in requested units.")
        print('================================================================')

    return col_check_list
```

# Function that checks on value types and replaces non-measured values.

```python
def check_values(data_frame,
                 inplace = False,
                 verbose = True,
                 ):
    """Function that checks on value types and replaces non-measured values.

    Args:
    -------
        data_frame: pandas.DataFrames
            dataframe with the measurements (without first row of units)
        inplace: Boolean, default False
            Whether to modify the DataFrame rather than creating a new one.
        verbose: Boolean
            verbose statement (default True)

    Returns:
    -------
        data_pure: pandas.DataFrame
            Tabular data with standard column names and without units

    Raises:
    -------
        None (yet).

    Example:
    -------
        To be added.
    """
    if verbose:
        print('================================================================')
        print(" Running function 'check_values()' on data")
        print('================================================================')

    data,cols= check_data_frame(data_frame, inplace = inplace)

    ### testing if provided data frame contains first row with units
    for u in data.iloc[0].to_list():
        if u in all_units:
            print("WARNING: First row identified as units, has been removed for value check")
            print('________________________________________________________________')
            data.drop(labels = 0,inplace = True)
            break

    for sign in to_replace_list:
        data.iloc[:,:] = data.iloc[:,:].replace(to_replace=sign, value=to_replace_value)

    # standardize column names (as it might not has happened for data yet)
    # check_columns(data,
    #               standardize = True,
    #               check_metabolites=True,
    #               verbose = False)

    # transform data to numeric values
    quantities_transformed = []
    for quantity in cols: #data.columns:
        try:
            # data_pure.loc[:,quantity] = pd.to_numeric(data_pure.loc[:,quantity])
            data[quantity] = pd.to_numeric(data[quantity])
            quantities_transformed.append(quantity)
        except ValueError:
            print("WARNING: Cound not transform '{}' to numerical values".format(quantity))
            print('________________________________________________________________')
    if verbose:
        print("Quantities with values transformed to numerical (int/float):")
        print('-----------------------------------------------------------')
        for name in quantities_transformed:
            print(name)
        print('================================================================')

    return data
```    
# Function providing condensed data frame with standardized names.

Function is checking names of columns and renames columns,
condenses data to identified column names, checks units and  names
sof data frame.

Function that looks at the column names and renames the columns to
the standard names of the model.

```python
def standardize(data_frame,
                check_metabolites = False,
                reduce = True,
                store_csv = False,
                verbose=True,
                ):
    """Function providing condensed data frame with standardized names.

    Function is checking names of columns and renames columns,
    condenses data to identified column names, checks units and  names
    sof data frame.

    Function that looks at the column names and renames the columns to
    the standard names of the model.

    Args:
    -------
        data_frame: pandas.DataFrames
            dataframe with the measurements
        check_metabolites: Boolean, default False
            whether to check on metabolites' values
        reduce: Boolean, default True
            whether to reduce data to known quantities (default True),
            otherwise full dataframe with renamed columns (for those identifyable) is returned
        store_csv: Boolean, default False
            whether to save dataframe in standard format to csv-file
        verbose: Boolean, default True
            verbose statement

    Returns:
    -------
        data_numeric, units: pandas.DataFrames
            Tabular data with standardized column names, values in numerics etc
            and table with units for standardized column names

    Raises:
    -------
        None (yet).

    Example:
    -------
    Todo's:
        - complete list of potential contaminants, environmental factors
        - add name check for metabolites?
        - add key-word to specify which data to extract
            (i.e. data columns to return)

    """
    if verbose:
        print('================================================================')
        print(" Running function 'standardize()' on data")
        print('================================================================')
        print(' Function performing check of data including:')
        print('  * check of column names and standardizing them.')
        print('  * check of units and outlining which to adapt.')
        print('  * check of values, replacing empty values by nan \n    and making them numeric')

    data,cols= check_data_frame(data_frame,
                                sample_name_to_index = False,
                                inplace = False)

    # general column check & standardize column names
    check_columns(data,
                  standardize = True,
                  reduce = reduce,
                  check_metabolites = False,
                  # check_metabolites = check_metabolites,
                  verbose = verbose)

    # general unit check
    units = data.drop(labels = np.arange(1,data.shape[0]))
    col_check_list = check_units(units,
                                 check_metabolites = check_metabolites,
                                 verbose = verbose)

    # transform data to numeric values
    data_numeric = check_values(data.drop(labels = 0),
                                inplace = False,
                                verbose = verbose)

    # store standard data to file
    if store_csv:
        if len(col_check_list) != 0:
            print('________________________________________________________________')
            print("Data could not be saved because not all identified \n quantities are given in requested units.")
        else:
            try:
                data.to_csv(store_csv,index=False)
                if verbose:
                    print('________________________________________________________________')
                    print("Save standardized dataframe to file:\n", store_csv)
            except OSError:
                print("WARNING: data could not be saved. Check provided file path and name: {}".format(store_csv))
    if verbose:
        print('================================================================')
```
3. **Transformation:(processing and enrichment)**

# Extracting data of specified variables from dataframe

```python
import pandas as pd
import mibipret.data.names_data as names

def extract_data(data_frame,
                 name_list,
                 keep_setting_data = True,
                 ):
    """Extracting data of specified variables from dataframe.

    Args:
    -------
        data_frame: pandas.DataFrames
            dataframe with the measurements
        name_list: list of strings
            list of column names to extract from dataframes
        keep_setting_data: bool, default True
            Whether to keep setting data in the DataFrame.

    Returns:
    -------
        data: pd.DataFrame
            dataframe with the measurements

    Raises:
    -------
    None (yet).

    Example:
    -------
    To be added.

    """
    inter_names,r_columns,r_name_list = compare_lists(data_frame.columns.to_list(),name_list)
    if len(inter_names)<len(name_list):
        print("Warning: Not all variables in name_list are identified in the data frame columns: ",r_name_list)

    if keep_setting_data:
        # inter,r1,r2 = compare_lists(data_frame.columns.to_list(),names.setting_data+name_list)

        inter_settings,r1,r2 = compare_lists(data_frame.columns.to_list(),names.setting_data)
        i1,rim_names,r2 = compare_lists(inter_names,names.setting_data)
        inter1 = inter_settings + rim_names
    else:
        inter1 = inter_names

    data = data_frame[inter1].copy()

    return data
```

# Merging dataframes along columns on similar sample name

```python
def merge_data(data_frames_list,
               how='outer',
               on=[names.name_sample],
               clean = True,
               **kwargs,
               ):
    """Merging dataframes along columns on similar sample name.

    Args:
    -------
        data_frames_list: list of pd.DataFrame
            list of dataframes with the measurements
        how: str, default 'outer'
            Type of merge to be performed.
            corresponds to keyword in pd.merge()
            {‘left’, ‘right’, ‘outer’, ‘inner’, ‘cross’}, default ‘outer’
        on: list, default "sample_nr"
            Column name(s) to join on.
            corresponds to keyword in pd.merge()
        clean: Boolean, default True
            Whether to drop columns which are in all provided data_frames
            (on which not to merge, potentially other settings than sample_name)
        **kwargs: dict
            optional keyword arguments to be passed to pd.merge()

    Returns:
    -------
        data: pd.DataFrame
            dataframe with the measurements

    Raises:
    -------
    None (yet).

    Example:
    -------
    To be added.

    """
    if len(data_frames_list)<2:
        raise ValueError('Provide List of DataFrames.')

    data_merge = data_frames_list[0]
    for data_add in data_frames_list[1:]:
        if clean:
            intersection,remainder_list1,remainder_list2 = compare_lists(
                data_merge.columns.to_list(),data_add.columns.to_list())
            intersection,remainder_list1,remainder_list2 = compare_lists(intersection,on)
            data_add = data_add.drop(labels = remainder_list1+remainder_list2,axis = 1)
        data_merge = pd.merge(data_merge,data_add, how=how, on=on,**kwargs)
        # complete data set, where values of porosity are added (otherwise nan)

    return data_merge
```
# Auxilary Functions: Checking overlap of two given list

```python
def compare_lists(list1,
                  list2,
                  verbose = False,
                  ):
    """Checking overlap of two given list.

    Input
    -----
        list1: list of strings
            given extensive list (usually column names of a pd.DataFrame)
        list2: list of strings
            list of names to extract/check overlap with strings in list 'column'
        verbose: Boolean, default True
            verbosity flag

    Output
    ------
        (intersection, remainder_list1, reminder_list2): tuple of lists
            * intersection: list of strings present in both lists 'list1' and 'list2'
            * remainder_list1: list of strings only present in 'list1'
            * remainder_list2: list of strings only present in 'list2'

    Example:
    -------
    list1 = ['test1','test2']
    list2 =  ['test1','test3']

    (['test1'],['test2']['test3']) = compare_lists(list1,list2)

    """
    intersection = list(set(list1) & set(list2))
    remainder_list1 = list(set(list1) - set(list2))
    remainder_list2 = list(set(list2) - set(list1))

    if verbose:
        print('================================================================')
        print(" Running function 'extract_variables()'")
        print('================================================================')
        print("strings present in both lists:", intersection)
        print("strings only present in either of the lists:", remainder_list1 +  remainder_list2)

    return (intersection,remainder_list1,remainder_list2)
```

4. **Storage:**
Once data is transformed, it is stored in an appropriate system depending on the use case.

### Types of Storage:
- Databases like UU YODA, MySQL
- GitHub repository

### Examples:
- Storing processed data in YODA

5. **Validation & Monitoring for Each Data Analysis Module**
This is intended task to do but not implemented yet.
```python
# we use the `options` function to check what types of analyses/modeling/visualization/reports we can do on the dataset
# if func argument is provided, it will check whether this function is possible and if not what else is needed
mibipret.decision_support.options(st_sample_data, func=mibipret.visualize.traffic3d)

# To perform mibipret.visualize.traffic3d you need to run mibipret.analysis.na_screening
# the workflow requires the following columns: [x,y, depth]
# Row 4-19 and 28-39 have these columns defined, you can apply the function on these rows.
```

6. **Analytics:** 

```python
# perform natural attenuation screening for contaminants provided in list or defaulting to the default set "BTEXIIN"
# na_screening uses stochiometric equations to analyze electron balance, these equations are contained in included file
# potentially link to online database
# if geographical data (x,y,z) for each well is in the original dataset, this will be also stored in the na_output
# the mibipret.analysis.sample collection of methods all have output per sample (that was analyzed) and can potentially 
# be added to the original standardized dataframe using the in_place argument

### run full NA screening with results in separate DataFrame
data_na = na.screening_NA(data,verbose = verbose)

### run full NA screening with results added to data
na.screening_NA(data,inplace = True,verbose = verbose)

# once we did the na_analysis we can visualize the data as traffic lights plotted for each sample 
#Calculation of "traffic light" based on electron balance Returns pandas-Series with traffic light (red/yellow/green) if NA is taking place based on electron balance. Red corresponds to a electron balance below 1 where available electrons for reduction are not sufficient and thus NA is potentially not taking place.

na_traffic = na.NA_traffic(data,verbose = True)
==============================================================
 Running function 'NA_traffic()' on data
==============================================================
WARNING: No data on oxygen given, zero concentration assumed.
________________________________________________________________
WARNING: No data on nitrate given, zero concentration assumed.
________________________________________________________________
Evaluation if natural attenuation (NA) is ongoing:
--------------------------------------------------
Red light: Reduction is limited at 7 out of 26 locations
Green light: Reduction is limited at 17 out of 26 locations
Yellow light: No decision possible at 2 out of 26 locations
```
