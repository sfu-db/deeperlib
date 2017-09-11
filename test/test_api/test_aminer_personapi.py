import unittest

from deeper.api.aminer.personapi import PersonApi


class AminerPersonTestCase(unittest.TestCase):
    def setUp(self):
        search_term = 'query'
        parameters = {'size': 100, 'sort': 'relevance'}
        self.aminer = PersonApi(top_k=1000, delay=1, search_term=search_term, **parameters)

    def tearDown(self):
        self.aminer = None

    def test_callApi(self):
        query = ['jian', 'nan', 'wang']
        params = self.aminer.getKwargs()
        params[self.aminer.getSearchTerm()] = '+'.join(query)
        result = self.aminer.callAPI(params=params)
        assert len(result) >= 95

    def test_callMulApi(self):
        queries = [['jian', 'nan', 'wang'], ['jian', 'pei']]
        result = self.aminer.callMulAPI(queries)
        self.aminer.getSession().close()
        assert len(result) >= 400
