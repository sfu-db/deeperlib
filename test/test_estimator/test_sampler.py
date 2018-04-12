import unittest
import os
from deeperlib.api.yelp.searchapi import SearchApi
from deeperlib.data_processing.local_data import LocalData
from deeperlib.core import utils
from deeperlib.estimator import sampler


class SamplerTestCase(unittest.TestCase):
    def setUp(self):
        client_id = "QhqrWe9agsd0Ad6Gs0qgMQ"
        client_secret = "6WQWRMV8edOhaThyWgm96wAJkIzJ1pHOhm5N0AD20edrnzv0lwi3wfgZAFp0IqQ6WIc-pZki83kjpViwptlcsiV0-Ij3HI6AJxhOTE4jsjNOoZOHZI3823twg8yZWXYx"
        search_term = 'term'
        parameters = {'limit': 50, 'location': 'AZ'}
        self.yelp = SearchApi(client_id=client_id, client_secret=client_secret, top_k=300, delay=5,
                              search_term=search_term,
                              **parameters)

    def test_sota_sampler(self):
        local_file = os.path.abspath(os.path.dirname(__file__) + os.path.sep + "../../") + '/yelp_example/yelp_3000_AZ.csv'
        localdata = LocalData(local_file, 'csv', "business_id", ["name"], ["name", "full_address"])
        localdata_ids, localdata_query, localdata_er = localdata.getlocalData()
        initQueries = utils.queryGene(localdata_query, 2)
        sampler.sota_sampler(query_pool=initQueries, api=self.yelp, match_term=localdata.getQueryList(), top_k=300,
                             adjustment=1, samplenum=1)
        self.yelp.getSession().close()
        assert True
