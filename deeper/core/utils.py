import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from sys import stderr as perr
from pqdict import maxpq
from deeper.entity_resolution import simjoin
import fim


def queryGene(D1, thre):
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
    findex = {}
    for q, v in D1index.iteritems():
        for d in v:
            if d not in findex:
                findex[d] = set()
            findex[d].add(q)
    return findex


def invertedIndex(queries, data):
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
    updatelist = {}
    for q in D1index:
        updatelist[q] = 0
    return updatelist


def initScore_unbiased(sampleindex, D1index, k, sr, queries):
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
    sj = simjoin.SimJoin(D1_ER)
    w_res = sj.join(er_result, jaccard_thre, True)
    match_ids = set()
    match_pair = []
    for r in w_res:
        match_ids.add(r[0][1])
        match_pair.append((r[0][1], r[1][1]))
    return match_ids, match_pair
