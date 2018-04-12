import unittest
import os
from deeperlib.data_processing.hidden_data import HiddenData


class HiddendataTestCase(unittest.TestCase):
    def setUp(self):
        result_dir = os.path.abspath(os.path.dirname(__file__) + os.path.sep + "../../") + '/dblp_example/dblp_result'
        self.hiddendata = HiddenData(result_dir, "info.key", ["info.title"])

    def tearDown(self):
        self.hiddendata = None

    def test_proResult(self):
        result_raw = [{u'@score': u'2', u'info': {
            u'title': u'Radio Access Technology Selection in Heterogeneous Wireless Networks. (S\xe9lection de technologie d&apos;acc\xe8s radio dans les r\xe9seaux sans-fil h\xe9t\xe9rog\xe8nes).',
            u'url': u'http://dblp.org/rec/phd/hal/ElHelou14', u'authors': {u'author': u'Melhem El Helou'},
            u'key': u'phd/hal/ElHelou14', u'year': u'2014', u'type': u'Books and Theses'}, u'@id': u'709440',
                       u'url': u'URL#709440'}]
        result_er = [(
            [u'radio', u'access', u'technology', u'selection', u'in', u'heterogeneous', u'wireless', u'networks', u's',
             u'lection', u'de', u'technologie', u'd', u'apos', u'acc', u's', u'radio', u'dans', u'les', u'r', u'seaux',
             u'sans', u'fil', u'h', u't', u'rog', u'nes'], u'phd/hal/ElHelou14')]

        assert self.hiddendata.proResult(result_raw) == result_er
