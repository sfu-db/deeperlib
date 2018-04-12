import unittest
import os
from deeperlib.data_processing.local_data import LocalData


class LocaldataTestCase(unittest.TestCase):
    def setUp(self):
        data_file = os.path.abspath(os.path.dirname(__file__) + os.path.sep + "../../") + '/yelp_example/yelp_3000_AZ.csv'
        self.localdata = LocalData(data_file, 'csv', "business_id", ["name"],
                                   ["name", "full_address"])

    def tearDown(self):
        self.localdata = None

    def test_loadLocalData(self):
        self.localdata.setlocalData(None, None, None)
        self.localdata.read_csv()
        localdata_ids, localdata_query, localdata_er = self.localdata.getlocalData()
        assert len(localdata_ids) == 3000
