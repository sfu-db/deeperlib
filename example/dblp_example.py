import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from deeperlib.core import smartcrawl
from deeperlib.api.dblp.publapi import PublApi
from deeperlib.data_processing.sample_data import SampleData
from deeperlib.data_processing.local_data import LocalData
from deeperlib.data_processing.hidden_data import HiddenData

top_k = 800
count = 3000000
pool_thre = 4
jaccard_thre = 0.9
threads = 5
budget = 50

"""
full description provided in the links of readme  
Parameter  Description                                                       Default  Example
q          The query string to search for, as described on a separate page.           ...?q=test+search
format     The result format of the search. Recognized values are "xml",     xml      ...?q=test&format=json
           "json", and "jsonp".
h          Maximum number of search results (hits) to return. For bandwidth  30       ...?q=test&h=100
           reasons, this number is capped at 1000.
f          The first hit in the numbered sequence of search results 
           (starting with 0) to return. In combination with the h parameter, 0        ...?q=test&h=100&f=300  
           this parameter can be used for pagination of search results.
c          Maximum number of completion terms (see below) to return. For     10       ...?q=test&c=0
           bandwidth reasons, this number is capped at 1000.
"""
search_term = 'q'
parameters = {'h': 800}
dblp = PublApi(delay=5, search_term=search_term, **parameters)

sample_file = 'dblp_sample'
localdata_file = 'dblp_10000'
result_dir = 'dblp_result'
sampledata = SampleData(sample_file, "row['key']", ["row['title']"])
localdata = LocalData(localdata_file, "row['key']", ["row['title']"], ["row['title']"])
hiddendata = HiddenData(result_dir, "row['info']['key']", ["row['info']['title']"])
smartcrawl.smartCrawl(top_k, count, pool_thre, jaccard_thre, threads, budget, dblp, sampledata, localdata, hiddendata)