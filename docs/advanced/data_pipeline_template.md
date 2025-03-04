
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

### Scenario: MiBiPreT data analysis mock-up

1. **Ingestion:**
```python
from mibipret.data import test_data
# some example data provided by the package, either a small dataset in the repository or downloading it from an online resource
test_data = mibipret.data.test_data()

# first load data per sheet
metabolites_data = mibipret.data.load_excel(file_path="path/to/data/data.xlsx", sheet=1, verbose=True, store_provenance=True)
hydro_data = mibipret.data.load_excel(file_path="path/to/data/data.xlsx", sheet=2, verbose=True, store_provenance=True)
contaminants_data = mibipret.data.load_excel(file_path="path/to/data/data.xlsx", sheet=5, verbose=True, store_provenance=True)

# or in one go
metabolites, hydro, contaminants = mibipret.data.load_excel(file_path="path/to/data/data.xlsx", sheet=[1,2,5], verbose=True, store_provenance=True)

# could also do this with csv files
metabolites_data = mibipret.data.load_csv(file_path="path/to/data/data.csv", verbose=True, store_provenance=True)

Warning: While importing your data from "path/to/data/data.xlsx" mibipret detected macros. Mind that these are not imported. 
Error: The second line in "path/to/data/data.xlsx" is supposed to specify the units. No units were detected in this line, check www.mibipretdocs.nl/dataloading.
```

2. **Preprocessing:** 
```python
# standardize runs check_units, check_columns and/or validation under the hood
# validation is similar to standardize, it combines various checks, but it does not create a new standardized dataset as standardize does
st_sample_data = mibipret.data.standardize(data=[contaminants, metabolites], data_type="sample", store_csv=True, verbose=True, store_provenance=True)

Warning: Column "O2" standardized to "oxygen"
Warning: Unit "kg/m3" of column "oxygen" was assumed to be "microgram/liter", make sure this conversion is valid. Check www.mibipretdocs.nl/unit-conversion.
```

3. **Transformation:** 
```python
# merging all data pooints in one file
metabolites, hydro, contaminants = mibipret.data.load_excel(file_path="path/to/data/data.xlsx", sheet=[1,2,5], verbose=True, store_provenance=True)
# not available for calculating new parameters
```

4. **Storage:**
not available

5. **Validation:** 
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
na_output = mibipret.analysis.sample.na_screening(data=st_data, contaminants=["name1", "name2", "name3"], in_place=True)
na_output

# once we did the na_analysis we can visualize the data as traffic lights plotted for each sample in space
# for this it is required that the spatial information is provided.
# because we ran na_screening analysis with in_place=True, the output was also added to the original st_data 
# we could therefore also run this method on st_data instead. 
mibipret.visualize.na_traffic3d(data=na_output, save_fig="plot_name.jpg")
```

