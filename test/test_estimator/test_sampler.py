import unittest
import os
from deeperlib.api.yelp.searchapi import SearchApi
from deeperlib.data_processing.local_data import LocalData
from deeperlib.core import utils
from deeperlib.estimator import sampler


class SamplerTestCase(unittest.TestCase):
    def setUp(self):
        client_id = "kCe2YbZePXsPnC204ZrXoQ"
        client_secret = "s9KnvEEQW7jaA2wlrBi4X2fnDQ0F7asdklXVvJUidWp8i50ov24E8EjkHX2AUhoL"
        search_term = 'term'
        parameters = {'limit': 50, 'location': 'AZ'}
        self.yelp = SearchApi(client_id=client_id, client_secret=client_secret, top_k=300, delay=5,
                              search_term=search_term,
                              **parameters)

    def test_sota_sampler(self):
        local_file = os.path.abspath(os.path.dirname(__file__) + os.path.sep + "../../") + '/example/yelp_3000'
        localdata = LocalData(local_file, "row['business_id']", ["row['name']"], ["row['name']", "row['full_address']"])
        localdata_ids, localdata_query, localdata_er = localdata.getlocalData()
        initQueries = utils.queryGene(localdata_query, 2)
        sampler.sota_sampler(query_pool=initQueries, api=self.yelp, match_term=localdata.getQueryList(), top_k=300,
                             adjustment=1, samplenum=1)
        self.yelp.getSession().close()
        assert True
