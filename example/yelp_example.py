import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from deeper.core import smartcrawl
from deeper.api.yelp.searchapi import SearchApi
from deeper.data_processing.sample_data import SampleData
from deeper.data_processing.local_data import LocalData
from deeper.data_processing.hidden_data import HiddenData

top_k = 50
count = 1000000
pool_thre = 2
jaccard_thre = 0.9
threads = 1
budget = 10

client_id = "kCe2YbZePXsPnC204ZrXoQ"
client_secret = "s9KnvEEQW7jaA2wlrBi4X2fnDQ0F7asdklXVvJUidWp8i50ov24E8EjkHX2AUhoL"
search_term = 'term'
parameters = {'limit':50, 'location': 'AZ'}
yelp = SearchApi(client_id=client_id, client_secret=client_secret, top_k=50, delay=5, search_term=search_term,
                 **parameters)
sample_file = 'yelp_sample'
localdata_file = 'yelp_3000'
result_file = 'yelp_result'
match_file = 'yelp_match'
sampledata = SampleData(sample_file, "row['id']", ["row['name']"])
localdata = LocalData(localdata_file, "row['business_id']", ["row['name']"], ["row['name']", "row['full_address']"])
hiddendata = HiddenData(result_file, match_file, "row['id']", ["row['name']", "' '.join(row['location']['display_address'])"])
smartcrawl.smartCrawl(top_k, count, pool_thre, jaccard_thre, threads, budget, yelp, sampledata, localdata, hiddendata)