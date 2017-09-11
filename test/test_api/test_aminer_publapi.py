import unittest

from deeper.api.aminer.publapi import PublApi


class AminerPublapiTestCase(unittest.TestCase):
    def setUp(self):
        search_term = 'query'
        parameters = {'size': 100, 'sort': 'relevance'}
        self.aminer = PublApi(top_k=1000, delay=1, search_term=search_term, **parameters)

    def tearDown(self):
        self.aminer = None

    def test_callApi(self):
        query = ['sfu', 'ubc']
        params = self.aminer.getKwargs()
        params[self.aminer.getSearchTerm()] = ' '.join(query)
        result = self.aminer.callAPI(params=params)
        assert len(result) >= 5

    def test_callMulApi(self):
        queries = [['set'], ['approximate']]
        result = self.aminer.callMulAPI(queries)
        self.aminer.getSession().close()
        assert len(result) >= 1950
