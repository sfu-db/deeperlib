from sys import stderr as perr
import timeit
import copy
import utils


def smartCrawl(budget, api, sampledata, localdata, hiddendata, pool_thre=2, jaccard_thre=0.85, threads=4):
    """
    Given a budget ofb queries, SMARTCRAWL first constructs a query pool based on the local database and then
    iteratively issues b queries to the hidden database such that the union of the query results can cover
    the maximum number of records in the local database. Finally, it performs entity resolution between the
    local database and the crawled records.
    ----**DeepER: Deep Entity Resolution**

    :param budget: the budget of api call times
    :param api: An implementation of simapi for specific api.
    :param sampledata: SampleData object
    :param localdata: LocalData object
    :param hiddendata: HiddenData object
    :param pool_thre: threshold of queries' frequency
    :param jaccard_thre: jaccard threshold
    :param threads: numbers of queries issued at each iteration
    :return:
    """
    time_s = timeit.default_timer()
    sample = sampledata.getSample()
    D1_ids, D1_query, D1_er = localdata.getlocalData()

    top_k = api.getTopk()
    sample_rate = sampledata.getRatio() / 100.0
    Dratio = 1.0 * len(D1_ids) * sample_rate / len(sample)

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
        print 'budget:', 100.0 * (len(query_pool) - flagNum) / budget, '%, coverage ratio:', \
            100.0 * len(curcov) / len(D1_ids), '%, ', len(cur_raw_result), 'results returned, ', \
            len(matched_ids), 'local records covered at this iteration. ', \
            len(hiddendata.getMergeResult()), 'different results returned, ', len(curcov), \
            'local records covered totally.'

    api.getSession().close()
    hiddendata.saveResult()
    hiddendata.setMatchPair(curmat)
    hiddendata.saveMatchPair()
