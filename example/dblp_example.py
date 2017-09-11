import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from deeper.core import smartcrawl
from deeper.api.dblp.publapi import PublApi
from deeper.data_processing.sample_data import SampleData
from deeper.data_processing.local_data import LocalData
from deeper.data_processing.hidden_data import HiddenData

top_k = 800
count = 3000000
pool_thre = 4
jaccard_thre = 0.9
threads = 5
budget = 50

search_term = 'q'
parameters = {'h': 800}
dblp = PublApi(delay=5, search_term=search_term, **parameters)
sample_file = 'dblp_sample'
localdata_file = 'dblp_10000'
result_file = 'dblp_result'
match_file = 'dblp_match'
sampledata = SampleData(sample_file, "row['key']", ["row['title']"])
localdata = LocalData(localdata_file, "row['key']", ["row['title']"], ["row['title']"])
hiddendata = HiddenData(result_file, match_file, "row['info']['key']", ["row['info']['title']"])
smartcrawl.smartCrawl(top_k, count, pool_thre, jaccard_thre, threads, budget, dblp, sampledata, localdata, hiddendata)