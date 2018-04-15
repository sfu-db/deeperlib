import sys

reload(sys)
sys.setdefaultencoding('utf-8')
from deeperlib.core import smartcrawl
from deeperlib.api.google.textsearchapi import TextSearchApi
from deeperlib.data_processing.sample_data import SampleData
from deeperlib.data_processing.local_data import LocalData
from deeperlib.data_processing.hidden_data import HiddenData

"""
full description provided in https://developers.google.cn/places/web-service/search
                             https://developers.google.com/places/web-service/details
                             
A Text Search request is an HTTP URL of the following form:
https://maps.googleapis.com/maps/api/place/textsearch/output?parameters
where output may be either of the following values:
    * json (recommended) indicates output in JavaScript Object Notation (JSON)
    * xml indicates output as XML
Required parameters
    * query - The text string on which to search, for example: "restaurant" or "123 Main Street". 
      The Google Places service will return candidate matches based on this string and order the results 
      based on their perceived relevance. This parameter becomes optional if the type parameter is also 
      used in the search request.
    * key - Your application's API key. This key identifies your application for purposes of quota management 
      and so that places added from your application are made immediately available to your app. See Get a key 
      for Google Places API Web Service to see how to create an API Project and obtain your key.
"""
search_term = 'query'
parameters = {'key': 'AIzaSyDhBJSPqHfcEkPGQGbH7l3eWyF_PhF10iw'}
google = TextSearchApi(location='in+Toronto', top_k=60, delay=5, search_term=search_term, **parameters)

"""
\yelp_sample_Toronto.pkl
 yelp_3000_Toronto.csv
 google_result\\result_file.pkl
              result_file.csv
              match_file.pkl
              match_file.csv
"""
sample_file = 'yelp_sample_Toronto.pkl'
localdata_file = 'yelp_3000_Toronto.csv'
result_dir = 'google_result'
sampledata = SampleData(sample_ratio=0.5, samplepath=sample_file, filetype='pkl', uniqueid="business_id",
                        querylist=["name"])
localdata = LocalData(localpath=localdata_file, filetype='csv', uniqueid="business_id",
                      querylist=["name"],
                      matchlist=["name", "full_address"])
hiddendata = HiddenData(result_dir=result_dir, uniqueid="place_id",
                        matchlist=["name", "formatted_address"])
budget = 20
smartcrawl.smartCrawl(budget, google, sampledata, localdata, hiddendata)
"""
pool_thre = 2
jaccard_thre = 0.85
threads = 4
smartcrawl.smartCrawl(budget, google, sampledata, localdata, hiddendata, pool_thre, jaccard_thre, threads)
"""
