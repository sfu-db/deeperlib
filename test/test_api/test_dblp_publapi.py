import unittest

from deeperlib.api.dblp.publapi import PublApi


class DblpPublapiTestCase(unittest.TestCase):
    def setUp(self):
        search_term = 'q'
        parameters = {'h': 1000}
        self.dblp = PublApi(top_k=1000, delay=5, search_term=search_term, **parameters)

    def tearDown(self):
        self.dblp = None

    def test_callApi(self):
        query = ['set', 'cover']
        params = self.dblp.getKwargs()
        params[self.dblp.getSearchTerm()] = '+'.join(query)
        hitList = self.dblp.callAPI(params=params)
        assert len(hitList) >= 900

    def test_callMulApi(self):
        queries = [['set', 'cover'], ['approximate', 'query']]
        hitList = self.dblp.callMulAPI(queries)
        self.dblp.getSession().close()
        assert len(hitList) >= 1200
