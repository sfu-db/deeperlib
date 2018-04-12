import unittest

from deeperlib.api.yelp.searchapi import SearchApi


class YelpSearchapiTestCase(unittest.TestCase):
    def setUp(self):
        client_id = "QhqrWe9agsd0Ad6Gs0qgMQ"
        client_secret = "6WQWRMV8edOhaThyWgm96wAJkIzJ1pHOhm5N0AD20edrnzv0lwi3wfgZAFp0IqQ6WIc-pZki83kjpViwptlcsiV0-Ij3HI6AJxhOTE4jsjNOoZOHZI3823twg8yZWXYx"
        search_term = 'term'
        parameters = {'limit': 50, 'location': 'AZ'}
        self.yelp = SearchApi(client_id=client_id, client_secret=client_secret, top_k=300, delay=5,
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
        print(len(results))
        assert len(results) >= 20

    def test_callMulApi_term(self):
        queries = [['tai'], ['restaurant']]
        results = self.yelp.callMulAPI(queries)
        assert len(results) >= 200

    def test_callMulApi_categories(self):
        self.yelp.setSearchTerm('categories')
        categories = [['bars'], ['french']]
        results = self.yelp.callMulAPI(categories)
        assert len(results) >= 200

    def test_callMulApi_sort(self):
        self.yelp.setSearchTerm('sort_by')
        sort_by = [['rating'], ['best_match']]
        results = self.yelp.callMulAPI(sort_by)
        self.yelp.getSession().close()
        print(len(results))
        assert len(results) >= 200
