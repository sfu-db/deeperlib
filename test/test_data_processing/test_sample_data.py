import unittest
import os
from deeperlib.data_processing.sample_data import SampleData


class SampledataTestCase(unittest.TestCase):
    def setUp(self):
        sample_file = os.path.abspath(os.path.dirname(__file__) + os.path.sep + "../../") + '/example/yelp_sample.pkl'
        self.sampledata = SampleData(sample_file, 'pkl', "row['id']", ["row['name']"])

    def tearDown(self):
        self.sampledata = None

    def test_loadSample(self):
        self.sampledata.setSample(None)
        self.sampledata.read_pickle()
        sample = self.sampledata.getSample()
        assert len(sample) == 484
