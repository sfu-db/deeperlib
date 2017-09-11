from sys import stderr as perr
import random
import copy
import pickle
from deeper.data_processing import data_process


def sota_sampler(query_pool, api, match_term, top_k, adjustment=1, samplenum=500):
    sample = []
    query_cost = 0
    params = api.getKwargs()
    query_pool_copy = copy.deepcopy(query_pool)

    while len(sample) < samplenum:
        query_cost += 1
        curQuery = random.choice(query_pool.items())
        params[api.getSearchTerm()] = '+'.join(curQuery[0])
        result = api.callAPI(params=params)
        # choose one valid query
        if len(result) < top_k and len(result) > 0:
            # with prob of q/k
            if random.uniform(0, 1) <= len(result) / (top_k * 1.0):
                # choose one edge uniformly
                rint = random.randint(0, len(result) - 1)
                row = result[rint]
                document = ''
                for term in match_term:
                    try:
                        document += data_process.alphnum(eval(term).lower()) + ' '
                    except KeyError:
                        continue
                # accept with prob of 1/freq
                # else continue with prob(1 - q/k)
                Mx = 0
                for q in query_pool_copy.keys():
                    Mx += 1
                    for subq in q:
                        if subq not in document:
                            Mx -= 1
                            break

                for subq in curQuery[0]:
                    if subq not in document:
                        Mx += 1
                        break

                if random.uniform(0, 1) < 1.0 * adjustment / Mx:
                    sample.append(document)
                    print 'sample num:', len(sample), ' query cost:', query_cost
                    # accept with prob of 1/M(X)
                    # else continue
        else:
            query_pool.pop(curQuery[0])
    print >> perr, query_cost, 'used for sampling.'

    with open('sample_' + str(query_cost), 'wb') as f:
        pickle.dump(sample, f)
    return sample
