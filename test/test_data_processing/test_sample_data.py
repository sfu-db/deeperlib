import unittest
import os
from deeperlib.data_processing.sample_data import SampleData


class SampledataTestCase(unittest.TestCase):
    def setUp(self):
        sample_file = os.path.abspath(os.path.dirname(__file__) + os.path.sep + "../../") + '/example/yelp_sample'
        self.sampledata = SampleData(sample_file, "row['id']", ["row['name']"])

    def tearDown(self):
        self.sampledata = None

    def test_loadSample(self):
        self.sampledata.setSample(None)
        self.sampledata.loadSample()
        sample = self.sampledata.getSample()
        assert len(sample) == 484
