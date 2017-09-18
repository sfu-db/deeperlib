import sys

reload(sys)
sys.setdefaultencoding('utf-8')
from deeperlib.core import smartcrawl
from deeperlib.api.dblp.publapi import PublApi
from deeperlib.data_processing.sample_data import SampleData
from deeperlib.data_processing.local_data import LocalData
from deeperlib.data_processing.hidden_data import HiddenData

top_k = 1000
count = 3000000
pool_thre = 2
jaccard_thre = 0.85
threads = 4
budget = 100

"""
full description provided in http://dblp.uni-trier.de/faq/How+to+use+the+dblp+search+API.html

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
parameters = {'h': 1000}
dblp = PublApi(delay=5, search_term=search_term, **parameters)

"""
\dblp_sample.csv
 dblp_3881.csv
 dblp_result\\result_file.pkl
              result_file.csv
              match_file.pkl
              match_file.csv
"""
sample_file = 'dblp_sample.csv'
localdata_file = 'dblp_3881.csv'
result_dir = 'dblp_result'
sampledata = SampleData(samplepath=sample_file, filetype='csv', uniqueid="key", querylist=["title"])
localdata = LocalData(localpath=localdata_file, filetype='csv', uniqueid="ID", querylist=['title'],
                      matchlist=['title'])
hiddendata = HiddenData(result_dir=result_dir, uniqueid="info.key", matchlist=["info.title"])
smartcrawl.smartCrawl(top_k, count, pool_thre, jaccard_thre, threads, budget, dblp, sampledata, localdata, hiddendata)
