from sys import stderr as perr
import numpy
import random
from deeper.data_processing import data_process


# issue queries from pool to get aggregate estimator
def sota_estimator(query_pool, api, match_term, uniqueid, query_num):
    count = 0
    query_cost = 0
    params = api.getKwargs()

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
            try:
                r_id = eval(uniqueid)
            except KeyError:
                continue
            document = ''
            for term in match_term:
                try:
                    document += data_process.alphnum(eval(term).lower()) + ' '
                except KeyError:
                    continue

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
                    break

                params[api.getSearchTerm()] = '+'.join(query)
                mresult = api.callAPI(params=params)
                query_cost += 1

                if len(mresult) == 0:
                    continue
                for mrow in mresult:
                    if r_id == eval('m' + uniqueid):
                        count += 1.0 * t / len(match_query)
                        break
                else:
                    continue
                break
    count = 1.0 * count * len(query_pool) / query_num
    print 'query cost: ', query_cost, ' count: ', count


def stratified_estimator(query_pool, api, match_term, candidate_rate, query_num, layer=5):
    stratified_pool, pool_sample = __query_pool_Sample(query_pool, query_num, api, layer)
    print >> perr, 'sample generated successfully.'
    params = api.getKwargs()
    total_weight = []
    for i in range(layer):
        total_weight.append(0)
    for i in range(layer):
        for query in pool_sample[i]:
            params[api.getSearchTerm()] = '+'.join(query)
            result = api.callAPI(params=params)
            for row in result:
                match_query, candidate_query = __candidate_construction(query, row, query_pool, match_term,
                                                                        candidate_rate)
                total_weight[i] += __topl_queryTesting(query, row, match_query, candidate_query, api)
                print >> perr, total_weight
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
            n_std.append(len(p) * numpy.std(p))
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


def __candidate_construction(query, row, query_pool, match_term, candidate_rate):
    # select set of queries matching X
    match_query = {}
    document = ''
    for term in match_term:
        try:
            document += data_process.alphnum(eval(term).lower()) + ' '
        except KeyError:
            continue
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
