from sys import stderr as perr
from pqdict import maxpq
from deeperlib.entity_resolution import simjoin
import fim


def queryGene(D1, thre):
    """
    Use fpgrowth to generate a finite queries pool

    :param D1: local database {'uniqueid':['database'. 'laboratory']}
    :param thre: threshold of queries' frequency
    :return: a closed frequency itemset of local database
    """
    D1bags = []
    for k, v in D1.iteritems():
        D1bags.append(v)
    queries_old = fim.fpgrowth(D1bags, 'c', 100.0 * thre / len(D1bags))
    queries = {}
    for i in queries_old:
        queries[frozenset(i[0])] = i[1]
    print >> perr, len(queries), 'queries generated in total.'
    return queries


def forwardIndex(D1index):
    """
     A forward index maps a local record to all the queries that the record satisfies. Such a list is
     called a forward list. To build the index, we initialize a hash map F and let F(d)denote the
     forward list for d.

    :param D1index: inverted index of local database.
    :return: a dict of forward index.
    """
    findex = {}
    for q, v in D1index.iteritems():
        for d in v:
            if d not in findex:
                findex[d] = set()
            findex[d].add(q)
    return findex


def invertedIndex(queries, data):
    """
     An inverted index maps each keyword to a list of local records that contain the keyword. Such a list
     is called an inverted list. To build the index, we initialize a hash map I and let I(w) denote the
     inverted list of key-word w. For each local record d belongs to D, we enumerate each keyword in
     document(d) and add d into I(w). Given a query q, we generate q(D) by getting the intersection of
     the inverted list of each keyword in the query.

    :param queries: query pool which is a closed frequency itemset of local database
    :param data: local database or sample database
    :return: an inverted index {query: set(uniqueid)}
    """
    sindex = {}
    for k, v in data.iteritems():
        for w in v:
            if w not in sindex:
                sindex[w] = set()
            sindex[w].add(k)
    index = {}
    for q in queries:
        tempSet = set()
        for w in q:
            if w in sindex:
                if len(tempSet) == 0:
                    tempSet = sindex[w]
                else:
                    tempSet = tempSet.intersection(sindex[w])
        index[q] = tempSet
    return index


def add_naiveIndex(queries, data, index):
    """
    To improve the efficiency of building index, naive queries would be added to query pool and inverted
    index after processing the queries whose frequency are larger than threshold.

    :param queries: query pool without naive queries
    :param data: local database
    :param index: inverted index without naive queries
    :return: query pool and inverted index with naive queries
    """
    naiveQueries = {}
    naiveIndex = {}
    for q, v in data.iteritems():
        naiveQueries[frozenset(v)] = 0
        naiveIndex[frozenset(v)] = set()
    for q, v in data.iteritems():
        naiveQueries[frozenset(v)] += 1
        naiveIndex[frozenset(v)] = naiveIndex[frozenset(v)].union(set([q]))
    naiveQueries.update(queries)
    queries = naiveQueries
    naiveIndex.update(index)
    index = naiveIndex
    return queries, index


def initScore_biased(sampleindex, k, sr, Dratio, queries):
    """
    Biased benefit estimation.

    :param sampleindex: inverted index of sample
    :param k: top-k restriction
    :param sr: sample rate
    :param Dratio: local database rate
    :param queries: query pool
    :return: query pool with biased benefit
    """
    query_pool = maxpq()
    for q, l1 in queries.iteritems():
        if len(sampleindex[q]) != 0:
            ls = len(sampleindex[q])
            est_score = ls / sr
            if est_score > k:
                score = k * l1 / (est_score * 1.0)
            else:
                score = l1
        else:
            if l1 > k * Dratio:
                score = 1.0 * k * Dratio
            else:
                score = l1
        query_pool[q] = score
    return query_pool


def updateList(D1index):
    """
    Update information stored into update list rather than update the priority of each query in-place in
    the priority queue.

    :param D1index: inverted index of local database.
    :return: a dict of update information
    """
    updatelist = {}
    for q in D1index:
        updatelist[q] = 0
    return updatelist


def initScore_unbiased(sampleindex, D1index, k, sr, queries):
    """
    Unbiased benefit estimation.

    :param sampleindex: inverted index of sample
    :param k: top-k restriction
    :param sr: sample rate
    :param Dratio: local database rate
    :param queries: query pool
    :return: query pool with biased benefit
    """
    query_pool = maxpq()
    for q, l1 in queries.iteritems():
        if len(sampleindex[q]) != 0:
            ls = len(sampleindex[q])
            lcap = len(sampleindex[q].intersection(D1index[q]))
            est_score = lcap / sr
            if est_score > k:
                score = lcap * k / (ls * 1.0)
            else:
                score = est_score
        else:
            score = 0
        query_pool[q] = score
    return query_pool


def results_simjoin(er_result, D1_ER, jaccard_thre):
    """
    An adapter for similarity join and smart crawl.

    :param er_result: documents returned by api at each iteration
    :param D1_ER: local database
    :param jaccard_thre: jaccard threshold
    :return: match index and pair at each iteration
    """
    sj = simjoin.SimJoin(D1_ER)
    w_res = sj.join(er_result, jaccard_thre, True)
    match_ids = set()
    match_pair = []
    for r in w_res:
        match_ids.add(r[0][1])
        match_pair.append((r[0][1], r[1][1]))
    return match_ids, match_pair
