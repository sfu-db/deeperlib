import unittest

from deeper.api.yelp.searchapi import SearchApi


class YelpSearchapiTestCase(unittest.TestCase):
    def setUp(self):
        client_id = "kCe2YbZePXsPnC204ZrXoQ"
        client_secret = "s9KnvEEQW7jaA2wlrBi4X2fnDQ0F7asdklXVvJUidWp8i50ov24E8EjkHX2AUhoL"
        search_term = 'term'
        parameters = {'limit': 50, 'location': 'AZ'}
        self.yelp = SearchApi(client_id=client_id, client_secret=client_secret, top_k=1000, delay=5,
                              search_term=search_term,
                              **parameters)

    def tearDown(self):
        self.yelp = None

    def test_callApi(self):
        query = ['tai', 'restaurant']
        params = self.yelp.getKwargs()
        params[self.yelp.getSearchTerm()] = '+'.join(query)
        params['offset'] = 0
        results = self.yelp.callAPI(params)
        assert len(results) >= 20

    def test_callMulApi_term(self):
        queries = [['tai'], ['restaurant']]
        results = self.yelp.callMulAPI(queries)
        assert len(results) >= 1000

    def test_callMulApi_categories(self):
        self.yelp.setSearchTerm('categories')
        categories = [['bars'], ['french']]
        results = self.yelp.callMulAPI(categories)
        print len(results)
        assert len(results) >= 700

    def test_callMulApi_sort(self):
        self.yelp.setSearchTerm('sort_by')
        sort_by = [['rating'], ['best_match']]
        results = self.yelp.callMulAPI(sort_by)
        self.yelp.getSession().close()
        assert len(results) >= 1000
