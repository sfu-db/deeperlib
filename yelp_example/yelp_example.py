import sys

reload(sys)
sys.setdefaultencoding('utf-8')
from deeperlib.core import smartcrawl
from deeperlib.api.yelp.searchapi import SearchApi
from deeperlib.data_processing.sample_data import SampleData
from deeperlib.data_processing.local_data import LocalData
from deeperlib.data_processing.hidden_data import HiddenData

"""
full description provided in https://www.yelp.com/developers/documentation/v3/business_search

Name        Type    Description
term        string  Optional. Search term (e.g. "food", "restaurants"). If term isn't included we search everything. 
                    The term keyword also accepts business names such as "Starbucks".
location    string  Required if either latitude or longitude is not provided. Specifies the combination of "address, 
                    neighborhood, city, state or zip, optional country" to be used when searching for businesses.
categories  string  Optional. Categories to filter the search results with. See the list of supported categories. 
                    The category filter can be a list of comma delimited categories. For example, "bars,french" 
                    will filter by Bars and French. The category identifier should be used (for example "discgolf", 
                    not "Disc Golf").
limit       int     Optional. Number of business results to return. By default, it will return 20. Maximum is 50.
offset      int     Optional. Offset the list of returned business results by this amount.
sort_by     string  Optional. Sort the results by one of the these modes: best_match, rating, review_count or distance. 
                    By default it's best_match. The rating sort is not strictly sorted by the rating value, but by an 
                    adjusted rating value that takes into account the number of ratings, similar to a bayesian average. 
                    This is so a business with 1 rating of 5 stars doesn't immediately jump to the top. 
"""
client_id = "QhqrWe9agsd0Ad6Gs0qgMQ"
client_secret = "6WQWRMV8edOhaThyWgm96wAJkIzJ1pHOhm5N0AD20edrnzv0lwi3wfgZAFp0IqQ6WIc-pZki83kjpViwptlcsiV0-Ij3HI6AJxhOTE4jsjNOoZOHZI3823twg8yZWXYx"
search_term = 'term'
parameters = {'limit': 50, 'location': 'AZ'}
yelp = SearchApi(client_id=client_id, client_secret=client_secret, top_k=300, delay=5, search_term=search_term,
                 **parameters)

"""
\yelp_sample.pkl
 yelp_10000.pkl
 yelp_result\\result_file.pkl
              result_file.csv
              match_file.pkl
              match_file.csv
"""
sample_file = 'yelp_sample_AZ.pkl'
localdata_file = 'yelp_3000_AZ.csv'
result_dir = 'yelp_result'
sampledata = SampleData(sample_ratio=0.5, samplepath=sample_file, filetype='pkl', uniqueid="business_id", querylist=["name"])
localdata = LocalData(localpath=localdata_file, filetype='csv', uniqueid="business_id",
                      querylist=["name"],
                      matchlist=["name", "full_address"])
hiddendata = HiddenData(result_dir=result_dir, uniqueid="id",
                        matchlist=["name", "location.display_address.*"])
budget = 20
smartcrawl.smartCrawl(budget, yelp, sampledata, localdata, hiddendata)
"""
pool_thre = 2
jaccard_thre = 0.85
threads = 4
smartcrawl.smartCrawl(budget, yelp, sampledata, localdata, hiddendata, pool_thre, jaccard_thre, threads)
"""
