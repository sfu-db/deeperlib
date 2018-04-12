import unittest
import os
from deeperlib.data_processing.sample_data import SampleData


class SampledataTestCase(unittest.TestCase):
    def setUp(self):
        sample_file = os.path.abspath(os.path.dirname(__file__) + os.path.sep + "../../") + '/yelp_example/yelp_sample_AZ.pkl'
        self.sampledata = SampleData(0.5, sample_file, 'pkl', "business_id", ["name"])

    def tearDown(self):
        self.sampledata = None

    def test_loadSample(self):
        self.sampledata.setSample(None)
        self.sampledata.read_pickle()
        sample = self.sampledata.getSample()
        assert len(sample) == 500
