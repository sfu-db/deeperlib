import unittest
from deeperlib.data_processing import data_process


class DataprocessTestCase(unittest.TestCase):
    def runTest(self):
        assert ['yong', 'jun', 'he'] == data_process.wordset('Yong@ jun# he')
