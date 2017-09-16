import unittest
import os
from deeperlib.data_processing.local_data import LocalData


class LocaldataTestCase(unittest.TestCase):
    def setUp(self):
        data_file = os.path.abspath(os.path.dirname(__file__) + os.path.sep + "../../") + '/example/yelp_3000.pkl'
        self.localdata = LocalData(data_file, 'pkl', "row['business_id']", ["row['name']"],
                                   ["row['name']", "row['full_address']"])

    def tearDown(self):
        self.localdata = None

    def test_loadLocalData(self):
        self.localdata.setlocalData(None, None, None)
        self.localdata.read_pickle()
        localdata_ids, localdata_query, localdata_er = self.localdata.getlocalData()
        assert len(localdata_ids) == 3000
