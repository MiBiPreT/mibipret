"""Tests for the mibipret.data module.

@author: Alraune Zech
"""
import numpy as np
import pandas as pd
import pytest
from mibipret.data.check_data import check_columns
from mibipret.data.check_data import check_data_frame
from mibipret.data.check_data import check_units
from mibipret.data.check_data import check_values
from mibipret.data.check_data import standard_names
from mibipret.data.check_data import standardize
from mibipret.data.example_data import example_data
from mibipret.data.load_data import load_csv
from mibipret.data.load_data import load_excel
from mibipret.data.set_data import compare_lists
from mibipret.data.set_data import determine_quantities
from mibipret.data.set_data import extract_data
from mibipret.data.set_data import merge_data

path_data = "./mibipret/data"
#path_data = "../mibipret/data"

class TestLoadData:
    """Class for testing data loading routines in data module of mibipret."""

    def test_load_csv_01(self):
        """Testing routine load_csv().

        Testing correct loading of example data from csv file.
        """
        data_t1 = load_csv("{}/example_data.csv".format(path_data))[0]
        data = example_data(with_units = True)
        assert data_t1.shape == data.shape

    def test_load_csv_02(self):
        """Testing routine load_csv().

        Testing Error message that no path to csv file is given.
        """
        with pytest.raises(ValueError, match="Specify file path and file name!"):
            load_csv()

    def test_load_csv_03(self):
        """Testing routine load_csv().

        Testing Error message that given file path does not match.
        """
        with pytest.raises(OSError):
            load_csv("ThisFileDoesNotExist.csv")

    def test_load_csv_04(self,capsys):
        """Testing routine load_csv().

        Testing verbose flag.
        """
        load_csv("{}/example_data.csv".format(path_data),verbose=True)
        out,err=capsys.readouterr()

        assert len(out)>0

    def test_load_excel_01(self):
        """Testing routine load_excel().

        Testing correct loading of example data from excel file.
        """
        data_t2= load_excel("{}/example_data.xlsx".format(path_data),sheet_name= 'contaminants')[0]
        data = example_data(data_type = 'contaminants',with_units = True)
        assert data_t2.shape == data.shape

    def test_load_excel_02(self):
        """Testing routine load_excel().

        Testing Error message that no path to excel file is given.
        """
        with pytest.raises(ValueError, match="Specify file path and file name!"):
            load_excel()

    def test_load_excel_03(self):
        """Testing routine load_excel().

        Testing Error message that given file path does not match.
        """
        with pytest.raises(OSError):
            load_excel("ThisFileDoesNotExist.xlsx")

    def test_load_excel_04(self,capsys):
        """Testing routine load_excel().

        Testing verbose flag.
        """
        load_excel("{}/example_data.xlsx".format(path_data),verbose=True)
        out,err=capsys.readouterr()

        assert len(out)>0


class TestExampleData:
    """Class for testing example data of data module of mibipret."""

    def test_example_data_01(self):
        """Testing correct loading of example data as pandas data frame."""
        data = example_data(with_units = True)

        assert data.shape == (5,29)

    def test_example_data_02(self):
        """Testing correct loading of example data as pandas data frame."""
        data = example_data(data_type = 'set_env_cont',with_units = True)
        assert data.shape == (5,24)

    def test_example_data_03(self):
        """Testing correct loading of example data as pandas data frame."""
        # assert isinstance(self.data_02, pd.DataFrame) == True
        data = example_data(data_type = 'contaminants',with_units = True)
        assert data.shape == (5,11)

    def test_example_data_04(self):
        """Testing correct loading of example data as pandas data frame."""
        # assert isinstance(self.data_03, pd.DataFrame) == True
        data = example_data(data_type = 'setting',with_units = True)
        assert data.shape == (5,3)

    def test_example_data_05(self):
        """Testing correct loading of example data as pandas data frame."""
        # assert isinstance(self.data_04, pd.DataFrame) == True
        data = example_data(data_type = 'environment',with_units = True)
        assert data.shape == (5,16)

    def test_example_data_06(self):
        """Testing correct loading of example data as pandas data frame."""
        # assert isinstance(self.data_04, pd.DataFrame) == True
        data = example_data(data_type = 'metabolites',with_units = True)
        assert data.shape == (5,6)

    def test_example_data_07(self):
        """Testing correct loading of example data as pandas data frame."""
        # assert isinstance(self.data_04, pd.DataFrame) == True
        data = example_data(data_type = 'isotopes',with_units = True)
        assert data.shape == (5,5)

    def test_example_data_08(self):
        """Testing correct loading of example data as pandas data frame."""
        data = example_data(with_units = False)

        assert data.shape == (4,29)

    def test_example_data_09(self):
        """Testing Error message that given data type not defined."""
        with pytest.raises(ValueError):
            example_data(data_type = 'test_data')


class TestStandardNames:
    """Testing routines on column name handling."""

    names_standard = ['sample_nr', 'obs_well', 'depth', 'pH', 'redoxpot', 'sulfate',\
                      'methane', 'iron2', 'benzene', 'naphthalene']
    names_mod = ["sample","well","Depth",'pH', 'redox' , 'Sulfate', 'CH4','iron','c6h6', 'Naphthalene']
    unknown  = ['unknown_contaminant']
    names_isotopes = ['delta_2H-unknown_contaminant', 'delta_13C-Toluene']

    def test_standard_names_01(self):
        """Testing routine standard_names().

        Testing routine on standard routine settings. It should provides
        a list with standardized names for those identified, plus those
        names (unchanged) which have not been identified.
        """
        results = standard_names(self.names_mod + self.unknown)

        assert results == self.names_standard + self.unknown

    def test_standard_names_02(self):
        """Testing routine standard_names().

        Testing that routine provides list with standardized column names
        containing only all names identified.
        """
        results = standard_names(self.names_mod + self.unknown,
                                  reduce = True,
                                  )

        assert results == self.names_standard

    def test_standard_names_03(self):
        """Testing routine standard_names().

        Testing when standardize is False.
        Routine provides tuple of lists with:
                * standardized column names
                * known column names
                * unknown column names
                * dictionary with transformation references
        """
        results = standard_names(self.names_mod + self.unknown,
                                  standardize = False,
                                  verbose = True,
                                  )

        assert results[0] == self.names_standard and results[1] == self.names_mod and \
                results[2] == self.unknown and isinstance(results[3],dict)


    def test_standard_names_04(self):
        """Testing routine standard_names().

        Testing standardization of metabolites by checking that routine identifies
        column names for metabolites in example data.
        """
        names_meta = ['Phenol','benzoic_acid']

        results = standard_names(names_meta,
                                 reduce = True,
                                 )
        assert len(results) == 2

    def test_standard_names_05(self):
        """Testing routine standard_names() on isotope sample names.

        Testing routine on isotope data by checking that routine identifies
        column names for isotopes in example data.
        """
        result  = standard_names(self.names_isotopes,
                                  reduce = True,
                                  )

        assert result == ['delta_13C-toluene']

    def test_standard_names_06(self):
        """Testing routine standard_names() on isotope names.

        Testing on isotope data by checking one name with identifiable name
        and one with unknown name combination.
        """
        result  = standard_names(self.names_isotopes,
                                  standardize = False,
                                  )

        assert len(result[1]) == 1 and len(result[2]) == 1


    def test_standard_names_07(self):
        """Testing routine standard_names().

        Testing that routine works also with single string, to be put into
        a list.
        """
        result  = standard_names('unknown_contaminant',
                                  standardize = False)

        assert len(result[0]) == 0 and len(result[1]) == 0 and len(result[2]) == 1


    def test_standard_names_08(self,capsys):
        """Testing routine standard_names().

        Testing verbose flag.
        """
        standard_names(self.names_mod + self.unknown,
                        verbose=True)
        out,err=capsys.readouterr()

        assert len(out)>0

    def test_standard_names_09(self,capsys):
        """Testing routine standard_names().

        Testing verbose flag for non-standard keyword settings.
        """
        standard_names(self.names_mod + self.unknown,
                       standardize = False,
                       reduce = True,
                       verbose=True)
        out,err=capsys.readouterr()

        assert len(out)>0

    def test_standard_names_10(self):
        """Testing routine standard_names().

        Testing Error if list contains values other than strings.
        """
        with pytest.raises(ValueError):
            standard_names(['unknown_contaminant',7.0])



class TestCheckDataFrame:
    """Testing routines on function check_data_frame()."""

    data_01 = example_data(with_units = False)
    cols = data_01.columns.to_list()

    def test_check_data_frame_01(self):
        """Testing routine check_data_frame().

        Check on correct identification of data as dataframe and
        returning dataframe and the list of column names for standard settings.
        """
        df, cols = check_data_frame(self.data_01)

        assert np.all(self.cols == cols)

    def test_check_data_frame_02(self):
        """Testing routine check_data_frame().

        Correct error message when data is not a pd.dataframe.
        """
        with pytest.raises(ValueError):
            check_data_frame(self.data_01.iloc[:,3])

    def test_check_data_frame_03(self):
        """Testing routine check_data_frame().

        Check keyword 'sample_name_to_index' which makes column of sample names
        (standard name) the indices.
        """
        df, cols = check_data_frame(self.data_01,sample_name_to_index=True)

        assert df.shape[1] == self.data_01.shape[1]-1

    def test_check_data_frame_04(self):
        """Testing routine check_data_frame().

        Check on keyword "inplace" which modifies dataframe inplace.
        """
        data_01b = example_data(with_units = False)

        check_data_frame(data_01b,
                         inplace = True,
                         sample_name_to_index=True)

        assert data_01b.shape[1] == self.data_01.shape[1]-1

    def test_check_data_frame_05(self,capsys):
        """Testing routine check_data_frame().

        Check on keyword "inplace" providing a warning when no sample name
        is provided.
        """
        data_01c = example_data(with_units = False)
        data_01c.drop(labels = 'sample_nr',axis = 1,inplace=True)

        check_data_frame(data_01c,sample_name_to_index=True)

        out,err=capsys.readouterr()

        assert len(out)>0


class TestCheckDataColumns:
    """Testing routines on checking and standardizing data.

    Class for testing routines on checking and standardizing data
    in data module of mibipret.
    """

    columns = ['sample_nr', 'obs_well', 'depth', 'pH', 'redoxpot', 'sulfate',\
                'methane', 'iron2', 'benzene', 'naphthalene']
    columns_mod = ["sample","well","Depth",'pH', 'redox' , 'Sulfate', 'CH4','iron','c6h6', 'Naphthalene']
    units = [' ',' ','m',' ','mV', 'mg/l', 'mg/l', 'mg/l', 'ug/l', 'ug/l']
    s01 = ['2000-001', 'B-MLS1-3-12',-12, 7.23, -208, 23, 748, 3,263,2207]

    new_column = pd.Series(data = ['ug/L',27.0], name = 'unknown_contaminant')

    data4check = pd.DataFrame([units,s01],columns = columns_mod)

    def test_check_columns_01(self):
        """Testing check_column() on complete example data.

        Testing that routine  check_column() identifies all standard names in
        data frame of complete example data.
        """
        results = check_columns(self.data4check)

        assert len(results) == 3

    def test_check_columns_02(self):
        """Testing routine check_column() on check and standardization of column names.

        Testing that data column names have been properly standardies.
        """
        check_columns(self.data4check,
                      standardize = True)

        assert np.all(self.data4check.columns == self.columns)

    def test_check_columns_03(self):
        """Testing routine check_column() on check and standardization of column names.

        Testing that data column names have been properly standardies.
        """
        data = pd.concat([self.data4check,self.new_column],axis = 1)
        check_columns(data,
                      reduce = True)

        assert self.data4check.shape[1] == data.shape[1]


    def test_check_columns_04(self,capsys):
        """Testing routine check_column() on check and standardization of column names.

        Testing verbose flag.
        """
        check_columns(self.data4check,
                      verbose=True)
        out,err=capsys.readouterr()

        assert len(out)>0


class TestCheckDataUnits:
    """Class for testing data module of mibipret."""

    columns = ['sample_nr', 'obs_well', 'depth', 'pH', 'redoxpot', 'sulfate',\
                'methane', 'iron2', 'benzene', 'naphthalene']
    units =     [' ',' ', 'm',' ','mV', 'mg/l', 'mg/l', 'mg/l', 'ug/l', 'ug/l']
    units_mod = [' ',' ','cm',' ','',   'ug/L', 'mg/L', 'ppm', 'mg/L',  'ug/L']
    check_list = ['depth', 'redoxpot','sulfate', 'benzene']
    s01 = ['2000-001', 'B-MLS1-3-12',-12, 7.23, -208, 23, 748, 3,263,2207]

    def test_check_units_01(self):
        """Testing check of units.

        Testing that routine check_units() provides correct list of
        quantities where units are not in expected format when input is
        the entire data frame.

        """
        data4units = pd.DataFrame([self.units_mod,self.s01],columns = self.columns)
        col_check_list = check_units(data4units)

        assert col_check_list == self.check_list

    def test_check_units_02(self):
        """Testing check of units.

        Testing that routine check_units() provides correct list of
        quantities where units are not in expected format when input is
        the data frame with only the unit-row.
        """
        data4units = pd.DataFrame([self.units_mod],columns = self.columns)
        col_check_list = check_units(data4units)

        assert col_check_list == self.check_list

    def test_check_units_03(self):
        """Testing check of units.

        Testing routine check_units() with metabolites.
        Testing of quantities where units are not in expected format when input is
        the data frame with only the unit-row.
        """
        data4units = pd.DataFrame([self.units_mod+['-']],columns = self.columns+['Phenol'])
        col_check_list = check_units(data4units)

        assert col_check_list == self.check_list+['phenol']

    def test_check_units_04(self):
        """Testing check of units.

        Testing routine check_units() with isotope data.
        Testing of quantities where units are not in expected format when input is
        the data frame with only the unit-row.
        """
        data4units = pd.DataFrame([self.units_mod+['-']],columns = self.columns+['delta_13C-benzene'])
        col_check_list = check_units(data4units)

        assert col_check_list == self.check_list+['delta_13C-benzene']

    def test_check_units_05(self):
        """Testing check of units.

        Testing Error message that provided input is not a data frame.
        """
        with pytest.raises(ValueError, match="Provided data is not a data frame."):
            check_units(self.s01)

    def test_check_units_06(self):
        """Testing check of units.

        Testing Error message that provided data frame does not contain units.
        """
        with pytest.raises(ValueError):
            data4units = pd.DataFrame([self.s01],columns = self.columns)
            check_units(data4units)

    def test_check_units_07(self,capsys):
        """Testing routine check of units.

        Testing verbose flag (When all units are correct).
        """
        data4units = pd.DataFrame([self.units,self.s01],columns = self.columns)

        check_units(data4units,verbose=True)
        out,err=capsys.readouterr()

        assert len(out)>0

    def test_check_units_08(self,capsys):
        """Testing routine check of units.

        Testing verbose flag  (When some units need correction).
        """
        data4units = pd.DataFrame([self.units_mod,self.s01],columns = self.columns)

        check_units(data4units,verbose=True)
        out,err=capsys.readouterr()

        assert len(out)>0


class TestCheckDataValues:
    """Class for testing data module of mibipret."""

    data_00 = example_data(with_units = True)

    def test_check_values_01(self,capsys):
        """Testing check_values() on complete example data.

        Testing that values in example data frame have been transformed to numerics.
        Testing verbose flag.
        """
        data = check_values(self.data_00,
                            inplace = False,
                            verbose = True)
        out,err=capsys.readouterr()

        assert len(out)>0 and isinstance(data.iloc[-1,-1], (np.float64,np.int64))

    def test_check_values_02(self):
        """Testing routine check_values().

        Testing that data frame is cut clean from units row.
        """
        data = check_values(self.data_00,
                            inplace = False,
                            )

        assert data.shape[0] == self.data_00.shape[0]-1

    def test_check_values_03(self):
        """Testing routine check_values().

        Testing 'inplace' keyword.
        """
        data_01 =self.data_00.copy()
        check_values(data_01,
                     inplace = True,
                     verbose = False)

        assert data_01.shape[0] == self.data_00.shape[0]-1

class TestDataStandardize:
    """Class for testing data module of mibipret."""

    columns = ['sample_nr', 'obs_well', 'depth', 'pH', 'redoxpot', 'sulfate',\
                'methane', 'iron2', 'benzene', 'naphthalene']
    units = [' ',' ','m',' ','mV', 'mg/l', 'mg/l', 'mg/l', 'ug/l', 'ug/l']
    s00 = ['2000-001', 'B-MLS1-3-12',-12, 7.23, -208, 23, 748, 3,263,2207]
    data4standard_0 = pd.DataFrame([units,s00],columns = columns)

    columns_mod = ["sample","well","Depth",'pH', 'redox' , 'Sulfate', 'CH4',
                   'iron','c6h6', 'Naphthalene','Phenol','delta_13C-Benzene','unknown_contaminant']
    units_mod = [' ',' ','cm',' ','','ug/L', 'mg/L', 'ppm', 'mg/L',  'ug/L', 'ppm', '-',' ']
    s01 = ['2000-001', 'B-MLS1-3-12',-12, 7.23, -208, 23, 748, 3,263,2207 , 10., 20.,30.]
    data4standard_1 = pd.DataFrame([units_mod,s01],columns = columns_mod)

    def test_standardize_01(self):
        """Testing routine standardize().

        Testing that data has been properly standardies,
        here that data frame is cut from unidentified quantities.
        """
        data_standard,units = standardize(self.data4standard_1,
                                          verbose=False)

        print(data_standard.columns[-2:])
        assert data_standard.shape[1] == self.data4standard_1.shape[1]-1 and \
                data_standard.shape[0] == self.data4standard_1.shape[0]-1

    def test_standardize_02(self,capsys):
        """Testing routine standardize().

        Testing Warning that data could not be saved to file given that not
        all quantities are given in requested units.
        """
        file_name = '../dir_does_not_exist/file.csv'
        out_text_end = 'quantities are given in requested units.'

        standardize(self.data4standard_1,
                    store_csv = file_name,
                    verbose=False)

        out,err=capsys.readouterr()
        # print(out[-40:])

        assert out[-41:-1]== out_text_end

    def test_standardize_03(self,capsys):
        """Testing routine standardize().

        Testing Error message that given file path does not match for writing
        standarized data to file.
        """
        file_name = '../dir_does_not_exist/file.csv'

        standardize(self.data4standard_0,
                    store_csv = file_name,
                    verbose=False)
        out,err=capsys.readouterr()

        assert out[-len(file_name)-1:-1]==file_name

    def test_standardize_04(self,capsys):
        """Testing routine standardize().

        Testing verbose flag.
        """
        standardize(self.data4standard_1,  verbose=True)
        out,err=capsys.readouterr()

        assert len(out)>0

class TestDataCompareLists:
    """Class for testing data module of mibipret."""

    list1 = ['test1','test2']
    list2 =  ['test1','test3']

    def test_compare_lists_01(self):
        """Testing routine compare_lists().

        Testing functionality of routines in standard settings.
        """
        inter,r1,r2 = compare_lists(self.list1,self.list2)

        assert inter == ['test1'] and r1 == ['test2'] and r2 == ['test3']

    def test_compare_lists_02(self,capsys):
        """Testing routine compare_lists().

        Testing verbose flag.
        """
        compare_lists(self.list1,self.list2,verbose=True)
        out,err=capsys.readouterr()

        assert len(out)>0

class TestDetermineQuantities:
    """Class for testing determine_quantities() of mibipret."""

    setting_data = ["sample_nr","obs_well","well_type","depth",'aquifer']
    list1 = ['pH', 'sulfate','benzene']
    list2 = ['sulfate','benzene']
    list3 = ['sulfate','benzene','test_quantity']
    list4 = ['benzene','pm_xylene','o_xylene', 'xylene', 'indane']
    list5 =  ['pH','oxygen', 'sulfate', "iron2" ,'methane']

    cols1 = setting_data+list1
    cols2 = setting_data+list2+['test_name']
    cols4 = setting_data+list4
    cols5 = setting_data+list5


    def test_determine_quantities_01(self):
        """Testing routine determine_quantities().

        Testing functionality of routine in standard settings.
        """
        quantities = determine_quantities(cols = self.cols1,
                                          verbose = True)

        assert set(quantities) == set(self.list1)

    def test_determine_quantities_02(self,capsys):
        """Testing routine determine_quantities().

        Testing functionality when specific list is provided.
        """
        quantities = determine_quantities(cols = self.cols2,
                                          name_list = self.list2,
                                          verbose = True)

        out,err=capsys.readouterr()
        assert set(quantities) == set(self.list2) and len(out)>0

    def test_determine_quantities_03(self,capsys):
        """Testing routine determine_quantities().

        Testing functionality when specific list is provided which
        also contains names not in the list of column names.
        """
        quantities = determine_quantities(cols = self.cols2,
                                          name_list = self.list3,
                                          verbose = False)

        out,err=capsys.readouterr()
        assert set(quantities) == set(self.list2) and len(out)>0

    def test_determine_quantities_04(self,capsys):
        """Testing routine determine_quantities().

        Testing functionality for short notation of selection of contaminants.
        """
        quantities = determine_quantities(cols = self.cols4,
                                          name_list = 'BTEX',
                                          verbose = False)

        out,err=capsys.readouterr()
        assert set(quantities) == set(['benzene', 'pm_xylene', 'o_xylene']) and len(out)>0

    def test_determine_quantities_05(self,capsys):
        """Testing routine determine_quantities().

        Testing functionality for short notation of selection of electron acceptors.
        """
        quantities = determine_quantities(cols = self.cols5,
                                          name_list = 'all_ea',
                                          verbose = False)

        out,err=capsys.readouterr()
        assert set(quantities) == set(self.list5[1:]) and len(out)>0


    def test_determine_quantities_06(self):
        """Testing routine determine_quantities().

        Testing functionality of routines in standard settings.
        """
        quantities = determine_quantities(cols = self.cols2,
                                          name_list = 'benzene',
                                          verbose = True)

        assert quantities == ['benzene']

    def test_determine_quantities_07(self):
        """Testing routine determine_quantities().

        Testing Error message if no quantity found.
        """
        with pytest.raises(ValueError):
            determine_quantities(cols = self.cols2,
                                 name_list = 'test_quantity',
                                 )


    def test_determine_quantities_8(self):
        """Testing routine determine_quantities().

        Testing correct handling if keyword name_list not correcty provided.
        """
        with pytest.raises(ValueError,match = "Keyword 'name_list' in correct format"):
            determine_quantities(cols = self.cols2,
                                 name_list = 7.0,
                                 )


class TestDataExtract:
    """Class for testing data module of mibipret."""

    columns = ['sample_nr', 'obs_well', 'pH', 'sulfate','benzene']
    s00 = ['2000-001', 'B-MLS1-3-12',7.23,  23, 263]
    data4extract = pd.DataFrame(data = [s00],columns = columns)

    name_list1 = ['sulfate','benzene']
    name_list2 = ['sample_nr','benzene']
    name_list3 = ['sulfate','benzene','naphtalene']

    def test_extract_data_01(self):
        """Testing routine extract_data().

        Testing functionality of routines in standard settings.
        """
        data = extract_data(self.data4extract,
                            name_list = self.name_list1)

        assert set(data.columns) == {'sample_nr', 'obs_well', 'sulfate','benzene'}

    def test_extract_data_02(self):
        """Testing routine extract_data().

        Testing functionality of routines in standard settings.
        """
        data = extract_data(self.data4extract,
                            name_list = self.name_list1,
                            keep_setting_data=False
                            )

        assert set(data.columns) == {'sulfate','benzene'}

    def test_extract_data_03(self):
        """Testing routine extract_data().

        Testing functionality of routines in standard settings.
        """
        data = extract_data(self.data4extract,
                            name_list = self.name_list2)

        assert set(data.columns) == {'sample_nr', 'obs_well', 'benzene'}

    def test_extract_data_04(self):
        """Testing routine extract_data().

        Testing functionality of routines in standard settings.
        """
        data = extract_data(self.data4extract,
                            name_list = self.name_list2,
                            keep_setting_data=False,
                            )

        assert set(data.columns) == {'sample_nr', 'benzene'}


    def test_extract_data_05(self,capsys):
        """Testing routine extract_data().

        Testing functionality of routines in standard settings.
        """
        data = extract_data(self.data4extract,
                            name_list = self.name_list3)

        out,err=capsys.readouterr()

        assert set(data.columns) == {'sample_nr', 'obs_well', 'sulfate','benzene'} and len(out)>0

class TestDataMerge:
    """Class for testing data module of mibipret."""

    columns = ['sample_nr', 'obs_well', 'pH', 'sulfate','benzene']
    s01 = ['2000-001', 'B-MLS1-3-12']
    s02 = ['2000-002', 'B-MLS1-5-15']
    s03 = ['2000-003', 'B-MLS1-6-17']
    s04 = ['2000-004', 'B-MLS1-7-19']

    e01 = [7.23,1.6]
    e02 = [7.67,0]
    e03 = [7.75,0.8]
    e04 = [7.53, 0.1]

    c01 = [263.]
    c02 = [179.]
    c03 = [853.]
    c04 = [1254.]

    data4merge_1 = pd.DataFrame(data = [s01+e01,s02+e02,s03+e03],
                                columns = ['sample_nr', 'obs_well', 'pH', 'sulfate'])

    data4merge_2 = pd.DataFrame(data = [s01+c01,s02+c02,s04+c04],
                                columns = ['sample_nr', 'obs_well','benzene'])

    def test_merge_data_01(self):
        """Testing routine merge_data().

        Testing functionality of routines in standard settings.
        """
        data1 = merge_data([self.data4merge_1,self.data4merge_2])

        assert data1.shape[1] == 5


    def test_merge_data_02(self):
        """Testing routine merge_data().

        Testing keywork 'clean'.
        """
        data1 = merge_data([self.data4merge_1,self.data4merge_2],
                           clean = False)

        assert data1.shape[1] == 6

    def test_merge_data_03(self):
        """Testing routine merge_data().

        Testing error message if not suffient data frames are provided.
        """
        with pytest.raises(ValueError,match = 'Provide List of DataFrames.'):
            merge_data([self.data4merge_1])

