import unittest

from deeperlib.api.dblp.venueapi import VenueApi


class DblpVenueapiTestCase(unittest.TestCase):
    def setUp(self):
        search_term = 'q'
        parameters = {'h': 1000}
        self.dblp = VenueApi(delay=5, search_term=search_term, **parameters)

    def tearDown(self):
        self.dblp = None

    def test_callApi(self):
        query = ['sigmod']
        params = self.dblp.getKwargs()
        params[self.dblp.getSearchTerm()] = '+'.join(query)
        hitList = self.dblp.callAPI(params=params)
        assert len(hitList) >= 20

    def test_callMulApi(self):
        queries = [['sigmod'], ['vldb']]
        hitList = self.dblp.callMulAPI(queries)
        self.dblp.getSession().close()
        assert len(hitList) >= 30
