import unittest

from deeperlib.api.aminer.advanced_publapi import AdvancedPublApi


class AminerAdvancedPublapiTestCase(unittest.TestCase):
    def setUp(self):
        search_term = 'term'
        parameters = {'size': 100, 'sort':'relevance'}
        self.aminer = AdvancedPublApi(top_k=1000,delay=1,search_term=search_term,**parameters)

    def tearDown(self):
        self.aminer = None

    def test_callApi(self):
        query = ['set', 'cover']
        params = self.aminer.getKwargs()
        params[self.aminer.getSearchTerm()] = '+'.join(query)
        result = self.aminer.callAPI(params=params)
        assert len(result) >= 95

    def test_callMulApi(self):
        queries = [['set'], ['approximate']]
        result = self.aminer.callMulAPI(queries)
        self.aminer.getSession().close()
        assert len(result) >= 1950