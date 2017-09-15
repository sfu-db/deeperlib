from deeperlib.api.yelp.searchapi import SearchApi
from deeperlib.core import utils
from deeperlib.data_processing.local_data import LocalData
from deeperlib.estimator import sampler

# ==== Sota-Sampler Yelp ====
client_id = "kCe2YbZePXsPnC204ZrXoQ"
client_secret = "s9KnvEEQW7jaA2wlrBi4X2fnDQ0F7asdklXVvJUidWp8i50ov24E8EjkHX2AUhoL"
search_term = 'term'
parameters = {'limit': 50, 'location': 'AZ'}
yelp = SearchApi(client_id=client_id, client_secret=client_secret, top_k=300, delay=5, search_term=search_term,
                 **parameters)
local_file = 'yelp_3000'
localdata = LocalData(local_file, "row['business_id']", ["row['name']"], ["row['name']", "row['full_address']"])
localdata_ids, localdata_query, localdata_er = localdata.getlocalData()
initQueries = utils.queryGene(localdata_query, 2)
sampler.sota_sampler(query_pool=initQueries, api=yelp, match_term=localdata.getQueryList(), top_k=300, adjustment=1)
yelp.getSession().close()
