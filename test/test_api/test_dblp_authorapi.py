import unittest

from deeperlib.api.dblp.authorapi import AuthorApi


class DblpAuthorapiTestCase(unittest.TestCase):
    def setUp(self):
        search_term = 'q'
        parameters = {'h': 1000}
        self.dblp = AuthorApi(top_k=1000, delay=5, search_term=search_term, **parameters)

    def tearDown(self):
        self.dblp = None

    def test_callApi(self):
        query = ['jian', 'nan', 'wang']
        params = self.dblp.getKwargs()
        params[self.dblp.getSearchTerm()] = '+'.join(query)
        hitList = self.dblp.callAPI(params=params)
        assert len(hitList) >= 3

    def test_callMulApi(self):
        queries = [['jian', 'nan', 'wang'],['jian', 'pei']]
        hitList = self.dblp.callMulAPI(queries)
        self.dblp.getSession().close()
        assert len(hitList) >= 30
