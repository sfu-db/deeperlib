import sys

reload(sys)
sys.setdefaultencoding('utf-8')
from sys import stderr as perr
from matplotlib import pyplot as plt
import timeit
import copy
import utils


def smartCrawl(top_k, count, pool_thre, jaccard_thre, threads, budget, api, sampledata, localdata, hiddendata):
    time_s = timeit.default_timer()
    sample = sampledata.getSample()
    D1_ids, D1_query, D1_er = localdata.getlocalData()

    sample_rate = 1.0 * len(sample) / count
    Dratio = 1.0 * len(D1_ids) / count

    time_e = timeit.default_timer()
    print >> perr, time_e - time_s, 'data loaded.'

    time_s = timeit.default_timer()
    initQueries = utils.queryGene(D1_query, pool_thre)
    time_e = timeit.default_timer()
    print >> perr, time_e - time_s, 'query pool finished.'

    #####inverted index #####
    time_s = timeit.default_timer()
    D1index = utils.invertedIndex(initQueries, D1_query)
    initQueries, D1index = utils.add_naiveIndex(initQueries, D1_query, D1index)
    sampleindex = utils.invertedIndex(initQueries, sample)
    time_e = timeit.default_timer()
    print >> perr, time_e - time_s, 'index building finished.'
    #####forward index #####
    time_s = timeit.default_timer()
    findex = utils.forwardIndex(D1index)
    time_e = timeit.default_timer()
    print >> perr, time_e - time_s, 'forward index'

    ##### biased #####
    D1_ids_deeper = copy.deepcopy(D1_ids)
    query_pool = utils.initScore_biased(sampleindex, top_k, sample_rate, Dratio, initQueries)
    flagNum = len(initQueries) - budget

    cov_deeper = []
    curcov = set()
    curmat = []
    updateList = utils.updateList(D1index)

    while len(query_pool) > flagNum and len(query_pool) != 0 and len(curcov) < len(D1_ids):
        queries = []
        while len(queries) < threads:
            if len(query_pool) > 0:
                top = query_pool.popitem()
                if updateList[top[0]] != 0:
                    if len(sampleindex[top[0]]) <= top_k * sample_rate:
                        if len(sampleindex[top[0]]) == 0 and len(D1index[top[0]]) > (top_k * Dratio):
                            new_priority = top[1] - updateList[top[0]] * top_k * Dratio / len(D1index[top[0]])
                        else:
                            new_priority = top[1] - updateList[top[0]]
                    else:
                        new_priority = top[1] - updateList[top[0]] * top_k * sample_rate / len(sampleindex[top[0]])
                    query_pool.additem(top[0], new_priority)
                    updateList[top[0]] = 0
                    continue
                else:
                    queries.append(list(top[0]))
            else:
                break

        cur_raw_result = api.callMulAPI(queries)
        cur_er_result = hiddendata.proResult(cur_raw_result)

        matched_ids, matched_pair = utils.results_simjoin(cur_er_result, D1_er, jaccard_thre)
        removed_ids = D1_ids_deeper.intersection(matched_ids)
        for d in removed_ids:
            for q in findex[d]:
                updateList[q] += 1

        D1_ids_deeper.difference_update(matched_ids)
        curcov = curcov.union(matched_ids)
        curmat.extend(matched_pair)
        cov_deeper.append(len(curcov))
        print len(curcov)

    api.getSession().close()
    hiddendata.setMatchPair(curmat)
    deeper_figure(cov_deeper, threads)


def deeper_figure(cov_deeper, threads):
    #####coverage figure#####
    x_range = len(cov_deeper) * threads
    x = range(1, x_range + 1, threads)
    plt.plot(x, cov_deeper[:x_range], 'g', label='records num')
    title = 'Coverage'
    plt.xlabel('times of api call')
    plt.title(title)
    plt.legend(loc='best')
    plt.show()
