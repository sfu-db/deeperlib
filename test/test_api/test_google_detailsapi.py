import unittest

from deeperlib.api.google.detailsapi import DetailsApi

class GoogleDetailsapiTestCase(unittest.TestCase):
    def setUp(self):
        search_term = 'placeid'
        parameters = {'key': 'AIzaSyDhBJSPqHfcEkPGQGbH7l3eWyF_PhF10iw'}
        self.google = DetailsApi(delay=5, search_term=search_term, **parameters)

    def tearDown(self):
        self.google = None

    def test_callApi(self):
        query = ['ChIJMbvGqzbL1IkRZerolAi13bI']
        params = self.google.getKwargs()
        params[self.google.getSearchTerm()] = '+'.join(query)
        results = self.google.callAPI(params)['result']
        assert len(results) >= 0

    def test_callMulApi_term(self):
        queries = [['ChIJMbvGqzbL1IkRZerolAi13bI'], ['ChIJh0FCAF8zK4gRjV9ua_M6srQ'], ['ChIJryijc9s0K4gRG9aU7SDTXdA']]
        results = self.google.callMulAPI(queries)
        assert len(results) ==3