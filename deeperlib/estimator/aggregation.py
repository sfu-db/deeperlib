import math
import random
from deeperlib.data_processing.data_process import alphnum, getElement


def sota_estimator(query_pool, api, match_term, uniqueid, query_num):
    """
    A method to estimate the aggregation of a search engine's corpus efficient
    ------**Efficient search engine measurements**

    :param query_pool: A dict contains the queries and their benefits. {set(['yong','jun']):5}
    :param api: An implementation of simapi for specific api.
    :param match_term: Some fields for matching queries and returned document.
    :param uniqueid: The uniqueid of returned messages.
    :param query_num: The number of queries you want to estimate
    :return: count(*) of the search engine
    """
    count = 0
    query_cost = 0
    params = api.getKwargs()

    uniqueId = uniqueid.split('.')
    matchlist = []
    for m in match_term:
        matchlist.append(m.split('.'))

    for i in range(query_num):
        # choose one query
        curQuery = random.choice(query_pool.items())
        params[api.getSearchTerm()] = '+'.join(curQuery[0])
        result = api.callAPI(params=params)
        query_cost += 1
        if len(result) == 0:
            continue

        # estimate weight for each query
        for row in result:
            r_id = getElement(uniqueId, row)
            document = ''
            for term in matchlist:
                document += alphnum(getElement(term, row).lower()) + ' '

            # get a set of queries match document
            match_query = []
            for q in query_pool:
                match_query.append(q)
                for subq in q:
                    if subq not in document:
                        match_query.pop()
                        break

            if curQuery[0] not in match_query:
                match_query.append(curQuery[0])

            # estimate weight for each edge
            t = 0
            while True:
                t += 1
                query = random.choice(match_query)
                if query == curQuery[0]:
                    count += 1.0 * t / len(match_query)
                    print 'count: ', count, ' query cost: ', query_cost
                    break

                params[api.getSearchTerm()] = '+'.join(query)
                mresult = api.callAPI(params=params)
                query_cost += 1

                if len(mresult) == 0:
                    continue
                for mrow in mresult:
                    try:
                        if r_id == getElement(uniqueId, mrow):
                            count += 1.0 * t / len(match_query)
                            print 'count: ', count, ' query cost: ', query_cost
                            break
                    except KeyError:
                        continue
                else:
                    continue
                break
    count = 1.0 * count * len(query_pool) / query_num
    print 'query cost: ', query_cost, ' count: ', count


def stratified_estimator(query_pool, api, match_term, candidate_rate, query_num, layer=5):
    """
    A method to estimate the aggregation of a search engine's corpus efficient yet unbiased
    ------**Mining a search engine's corpus: efficient yet unbiased sampling and aggregate estimation**

    :param query_pool: A dict contains the queries and their benefits. {set(['yong','jun']):5}
    :param api: An implementation of simapi for specific api.
    :param match_term: Some fields for matching queries and returned document.
    :param candidate_rate: A proportion of match query would be the candidate_rate..
    :param query_num: The number of queries you want to estimate
    :param layer: The number of queries you want to estimate
    :return: count(*) of the search engine
    """
    stratified_pool, pool_sample = __query_pool_Sample(query_pool, query_num, api, layer)
    print 'sample generated successfully.'

    params = api.getKwargs()
    matchlist = []
    for m in match_term:
        matchlist.append(m.split('.'))

    total_weight = []
    for i in range(layer):
        total_weight.append(0)
    for i in range(layer):
        for query in pool_sample[i]:
            params[api.getSearchTerm()] = '+'.join(query)
            result = api.callAPI(params=params)
            if len(result) == 0:
                continue
            for row in result:
                match_query, candidate_query = __candidate_construction(query, row, query_pool, matchlist,
                                                                        candidate_rate)
                total_weight[i] += __topl_queryTesting(query, row, match_query, candidate_query, api)
                print total_weight
    count = 0
    for i in range(layer):
        count += 1.0 * len(stratified_pool[i]) * total_weight[i] / len(pool_sample[i])
    return count


def __query_pool_Sample(query_pool, query_num, api, layer):
    params = api.getKwargs()
    # divide the query pool into L strata
    stratified_pool = []
    for i in range(layer):
        stratified_pool.append([])
    for q, v in query_pool.iteritems():
        if v <= layer:
            stratified_pool[v - 2].append(q)
        else:
            stratified_pool[layer - 1].append(q)

    # pilot step
    pilot_result = []
    for i in range(layer):
        pilot_result.append([])
    for i in range(layer):
        for r in range(5):
            if len(stratified_pool[i]) > 0:
                query = random.choice(stratified_pool[i])
                params[api.getSearchTerm()] = '+'.join(query)
                result = api.callAPI(params=params)
                pilot_result[i].append(len(result))

    # Neyman allocation
    n_std = []
    for p in pilot_result:
        if len(p) != 0:
            n_std.append(len(p) * __std(p))
        else:
            n_std.append(0)

    issue_num = []
    for s in n_std:
        issue_num.append(int(query_num * (1.0 * s / sum(n_std))))

    # build estimator query_pool
    pool_sample = []
    for i in range(layer):
        pool_sample.append([])
    for i in range(len(stratified_pool)):
        if len(stratified_pool[i]) <= issue_num[i]:
            pool_sample[i].extend(stratified_pool[i])
        else:
            pool_sample[i].extend(random.sample(stratified_pool[i], issue_num[i]))

    return stratified_pool, pool_sample


def __candidate_construction(query, row, query_pool, match_list, candidate_rate):
    # select set of queries matching X
    match_query = {}
    document = ''
    for term in match_list:
        document += alphnum(getElement(term, row).lower()) + ' '
    for q, v in query_pool.iteritems():
        match_query[q] = v
        for subq in q:
            if subq not in document:
                match_query.pop(q)
                break
    match_query[query] = query_pool[query]
    candidate_query = random.sample(match_query.keys(), int(len(match_query) * candidate_rate))
    return match_query, candidate_query


def __topl_queryTesting(query, row, match_query, candidate_query, api):
    params = api.getKwargs()
    if query in candidate_query:
        h = 0
        while True:
            h += 1
            curQuery = random.choice(candidate_query)
            params[api.getSearchTerm()] = '+'.join(curQuery)
            result = api.callAPI(params=params)
            if row in result:
                return 1.0 * h / len(candidate_query)
    else:
        match_query = sorted(match_query.iteritems(), key=lambda item: item[1], reverse=False)
        for m in match_query:
            params[api.getSearchTerm()] = '+'.join(m[0])
            result = api.callAPI(params=params)
            if row in result:
                if m[0] == query:
                    return 1
                else:
                    return 0


def __std(iterable):
    """
    Calculate standard deviation for sample

    :param iterable: sample iterable
    :return: standard deviation
    """
    avg = math.fsum(iterable) / len(iterable)
    var = 0
    for i in iterable:
        var += math.pow((i - avg), 2)
    var = var / (len(iterable) - 1)
    std = math.sqrt(var)
    return std
