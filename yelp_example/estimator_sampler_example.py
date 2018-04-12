from deeperlib.api.yelp.searchapi import SearchApi
from deeperlib.core import utils
from deeperlib.data_processing.local_data import LocalData
from deeperlib.estimator import sampler

# ==== Sota-Sampler Yelp ====
client_id = "QhqrWe9agsd0Ad6Gs0qgMQ"
client_secret = "6WQWRMV8edOhaThyWgm96wAJkIzJ1pHOhm5N0AD20edrnzv0lwi3wfgZAFp0IqQ6WIc-pZki83kjpViwptlcsiV0-Ij3HI6AJxhOTE4jsjNOoZOHZI3823twg8yZWXYx"
search_term = 'term'
parameters = {'limit': 50, 'location': 'AZ'}
yelp = SearchApi(client_id=client_id, client_secret=client_secret, top_k=300, delay=5, search_term=search_term,
                 **parameters)
local_file = 'yelp_3000_AZ.csv'
localdata = LocalData(local_file, 'csv', "business_id", ["name"], ["name", "full_address"])
localdata_ids, localdata_query, localdata_er = localdata.getlocalData()
initQueries = utils.queryGene(localdata_query, 2)
sampler.sota_sampler(query_pool=initQueries, api=yelp, match_term=localdata.getQueryList(), top_k=300, adjustment=1)
yelp.getSession().close()
