import unittest

from deeperlib.api.google.textsearchapi import TextSearchApi


class GoogleTextsearchapiTestCase(unittest.TestCase):
    def setUp(self):
        search_term = 'query'
        parameters = {'key': 'AIzaSyDhBJSPqHfcEkPGQGbH7l3eWyF_PhF10iw'}
        self.google = TextSearchApi(location='in+Toronto', top_k=60, delay=5, search_term=search_term, **parameters)

    def tearDown(self):
        self.google = None

    def test_callApi(self):
        query = ['restaurant']
        query.append('in+Toronto')
        params = self.google.getKwargs()
        params[self.google.getSearchTerm()] = '+'.join(query)
        results = self.google.callAPI(params)['results']
        assert len(results) >= 10

    def test_callMulApi_term(self):
        queries = [['subway'], ['restaurant']]
        results = self.google.callMulAPI(queries)
        assert len(results) >= 50
