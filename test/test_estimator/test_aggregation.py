import unittest
import os
from deeperlib.api.dblp.publapi import PublApi
from deeperlib.data_processing.local_data import LocalData
from deeperlib.core import utils
from deeperlib.estimator import aggregation


class AggregationTestCase(unittest.TestCase):
    def setUp(self):
        search_term = 'q'
        parameters = {'h': 1000}
        self.dblp = PublApi(top_k=1000, delay=5, search_term=search_term, **parameters)
        localdata_file = os.path.abspath(os.path.dirname(__file__) + os.path.sep + "../../") + '/dblp_example/dblp_sample.csv'
        localdata = LocalData(localdata_file, 'csv', "key", ["title"], ["title"])
        localdata_ids, localdata_query, localdata_er = localdata.getlocalData()
        initQueries = utils.queryGene(localdata_query, 2)
        self.initQueries = initQueries

    def test_stra_stratified_estimator(self):
        aggregation.stratified_estimator(query_pool=self.initQueries, api=self.dblp,
                                         match_term=["info.title"],
                                         candidate_rate=0.2,
                                         query_num=100)
        assert True

    def test_sota_estimator(self):
        aggregation.sota_estimator(query_pool=self.initQueries, api=self.dblp, match_term=["info.title"],
                                   uniqueid="info.key",
                                   query_num=1)
        self.dblp.getSession().close()
        assert True