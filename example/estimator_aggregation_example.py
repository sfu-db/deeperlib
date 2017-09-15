from deeperlib.api.dblp.publapi import PublApi
from deeperlib.core import utils
from deeperlib.data_processing.local_data import LocalData
from deeperlib.estimator import aggregation

# ==== Sota-Estimator Dblp ====
search_term = 'q'
parameters = {'h': 1000}
dblp = PublApi(delay=5, search_term=search_term, **parameters)
localdata_file = 'dblp_10000'
localdata = LocalData(localdata_file, "row['key']", ["row['title']"], ["row['title']"])
localdata_ids, localdata_query, localdata_er = localdata.getlocalData()
initQueries = utils.queryGene(localdata_query, 2)
aggregation.sota_estimator(query_pool=initQueries, api=dblp, match_term=["row['info']['title']"],
                           uniqueid="row['info']['key']",
                           query_num=1)

# ==== Stratified-Estimator Dblp ====
dblp = PublApi(delay=5, search_term=search_term, **parameters)
aggregation.stratified_estimator(query_pool=initQueries, api=dblp,
                                 match_term=["row['info']['title']"],
                                 candidate_rate=0.2,
                                 query_num=100)
dblp.getSession().close()
