"""Tests for the mibipret.analysis.reduction.transformation module.

@author: Alraune Zech
"""

import numpy as np
import pytest
from mibipret.analysis.reduction.transformation import filter_values
from mibipret.analysis.reduction.transformation import transform_values
from mibipret.data.example_data import example_data


class Test_Filtering:
    """Class for testing data filter for ordination."""

    data = example_data(with_units = False)


    def test_filter_01(self):
        """Testing routine filter_values().

        Check that routine provides filtered data frame for default settings:
            - inplace False
            - replace_NaN = 'remove'
            - verbose = False
        """
        data_filter = filter_values(self.data)

        assert data_filter.shape[0] == self.data.shape[0]-1


    def test_filter_02(self):
        """Testing routine filter_values().

        Check that routine provides filtered data frame for replacement option
        'zero'
        """
        data_filter = filter_values(self.data,
                                    replace_NaN = 'zero')

        test = [data_filter.shape[0] == self.data.shape[0],
                data_filter['phenol'][2] == 0.0,
                ]

        assert np.all(test)

    def test_filter_03(self):
        """Testing routine filter_values().

        Check that routine provides filtered data frame for replacement option
        float or integer value
        """
        data_filter = filter_values(self.data,
                                    replace_NaN = 1.0)

        test = [data_filter.shape[0] == self.data.shape[0],
                data_filter['phenol'][2] == 1.0,
                ]

        assert np.all(test)

    def test_filter_04(self):
        """Testing routine filter_values().

        Check that routine provides filtered data frame for replacement option
        'average'
        """
        data_filter = filter_values(self.data,
                                    replace_NaN = 'average')

        test = [data_filter.shape[0] == self.data.shape[0],
                np.isclose(data_filter['phenol'][2], 0.1666, rtol=1e-02),
                ]

        assert np.all(test)

    def test_filter_05(self):
        """Testing routine filter_values().

        Check that routine provides filtered data frame for replacement option
        'median'
        """
        data_filter = filter_values(self.data,
                                    replace_NaN = 'median')

        test = [data_filter.shape[0] == self.data.shape[0],
                np.isclose(data_filter['phenol'][2], 0.2, rtol=1e-02),
                ]

        assert np.all(test)



    def test_filter_06(self):
        """Testing routine filter_values().

        Correct error message when keyword for replacement option 'replace_NaN'
        is not a valid option
        """
        replace_NaN = 'wrong option'
        with pytest.raises(ValueError,match="Value of 'replace_NaN' unknown: {}".format(replace_NaN)):
            filter_values(self.data,
                          replace_NaN = replace_NaN)

    def test_filter_07(self):
        """Testing routine filter_values().

        Check that routine provides filtered data frame for default settings:
            - inplace True
            - replace_NaN = 'remove'
            - verbose = False
        """
        data_filter = self.data.copy()
        filter_values(data_filter,
                      inplace = True)

        assert data_filter.shape[0] == self.data.shape[0]-1


    def test_filter_08(self):
        """Testing routine filter_values().

        Check keyword 'drop_rows'
        """
        data_filter = filter_values(self.data,
                                    drop_rows = [4],
                                    )


        assert data_filter.shape[0] == self.data.shape[0]-2


    def test_filter_09(self,capsys):
        """Testing routine filter_values().

        Testing verbose flag.
        """
        filter_values(self.data,
                      drop_rows = [2],
                      verbose = True,
                      )

        out,err=capsys.readouterr()

        assert len(out)>0


class Test_Transformation:
    """Class for testing data transformation for ordination."""

    data = example_data(with_units = False).iloc[:,0:19]

    def test_transform_values_01(self):
        """Testing routine transform_values().

        Check that routine provides correct tranformation results for
        type of filtering: center

        """
        data_trans = transform_values(self.data,
                         how = 'center',
                         )

        data_test = data_trans.iloc[:,3:].mean(axis = 0)

        assert np.isclose(np.mean(data_test.values), 0, rtol=1e-05)

    def test_transform_values_02(self):
        """Testing routine transform_values().

        Check that routine provides correct tranformation results for
        type of filtering: standard

        """
        data_trans = transform_values(self.data,
                         how = 'standardize',
                         )

        data_test = data_trans.iloc[:,3:].mean(axis = 0)

        assert np.isclose(np.mean(data_test.values), 0, rtol=1e-05)

    def test_transform_values_03(self):
        """Testing routine transform_values().

        Check that routine provides correct tranformation results for
        log transformation on a single quantity

        """
        variable = 'nitrate'
        data_log = transform_values(self.data,
                                    name_list = variable,
                                    )

        assert np.all(np.isclose(data_log[variable], [2.089905, 0.778151, 0.602060, 2.257679], rtol=1e-05))


    def test_transform_values_04(self):
        """Testing routine transform_values().

        Correct error message when keyword for transformation option 'how'
        is not a valid option
        """
        how = 'wrong option'
        with pytest.raises(ValueError,match="Value of 'how' unknown: {}".format(how)):
            transform_values(self.data,
                             how = how)


    def test_transform_values_05(self):
        """Testing routine transform_values().

        Check that routine provides correct tranformation results for
        log transformation on a single quantity

        """
        variables = ['nitrate', 'methane','benzene']
        data_mod = self.data.copy()
        transform_values(data_mod,
                         name_list = variables,
                         how = 'center',
                         inplace = True,
                         )

        assert np.all(np.not_equal(data_mod[variables].values,self.data[variables].values))

    def test_transform_values_065(self,capsys):
        """Testing routine transform_values().

        Check that routine provides Warning when a variable from the list
        is not identitied in the data frame
        """
        variables = ['nitrate', 'methane','benzene', 'wrong name']
        transform_values(self.data,
                         name_list = variables,
                         how = 'center',
                         )

        out,err=capsys.readouterr()
        assert len(out)>0

    def test_transform_values_07(self,capsys):
        """Testing routine transform_values().

        Testing verbose flag.
        """
        transform_values(self.data,
                         verbose = True,
                         )

        out,err=capsys.readouterr()

        assert len(out)>0
