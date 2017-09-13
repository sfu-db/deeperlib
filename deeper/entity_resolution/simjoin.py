import re
import math


class InvertedIndex:
    def __init__(self):
        self.index = {}

    def insert(self, word, docid):
        index = self.index
        if word in index:
            index[word].add(docid)
        else:
            index[word] = set([docid])

    def get(self, *words):
        docids = set()
        for word in words:
            docids = docids.union(self.index.get(word, set()))
        return docids


def jaccard(s, t):
    intersect = len(set(s) & set(t))
    union = len(s) + len(t) - intersect
    if union == 0:
        return 0
    else:
        return intersect * 1.0 / union


def jaccard_w(s, t, lower_case=True, alphanum_only=True):
    return jaccard(wordset(s, lower_case, alphanum_only), \
                   wordset(t, lower_case, alphanum_only))


def jaccard_g(s, t, gram_size, lower_case=True, alphanum_only=True):
    return jaccard(gramset(s, gram_size, lower_case, alphanum_only), \
                   gramset(t, gram_size, lower_case, alphanum_only))


def editsim(s, t):
    n = len(s)
    m = len(t)

    dist = [[0 for j in range(m + 1)] for i in range(n + 1)]

    for i in range(1, n + 1):
        dist[i][0] = dist[i - 1][0] + 1

    for j in range(1, m + 1):
        dist[0][j] = dist[0][j - 1] + 1

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            dist[i][j] = min(dist[i - 1][j] + 1, \
                             dist[i][j - 1] + 1,
                             dist[i - 1][j - 1] if s[i - 1] == t[j - 1] else dist[i - 1][j - 1] + 1)

    return 1 - dist[n][m] * 1.0 / max(m, n)


def alphnum(s):
    sep = re.compile(r"[\W]")
    items = sep.split(s)
    return " ".join([item for item in items if item.strip() != ""])


def wordset(s, lower_case=True, alphanum_only=True):
    if lower_case:
        s = s.lower()
    if alphanum_only:
        s = alphnum(s)
    return s.split()


def gramset(s, gram_size, lower_case=True, alphanum_only=True):
    if gram_size <= 0 or type(gram_size) is not int:
        raise Exception("'gram_size=" + str(gram_size) + "' is not a non-negative integer.")
    if lower_case:
        s = s.lower()
    if alphanum_only:
        s = alphnum(s)
    ns = len(s) + gram_size - 1
    s = "^" * (gram_size - 1) + s + "$" * (gram_size - 1)
    return [s[i:i + gram_size] for i in range(ns)]


class SimJoin:
    """
    Use jaccard coefficient and tf-idf to do similarity join.
    """

    def __init__(self, k_o_list):
        self.k_o_list = k_o_list

    def _idf(self, docs):
        word_to_idf = {}
        word_to_count = {}
        for doc in docs:
            flags = {}
            for w in doc:
                if w in flags:
                    continue
                flags[w] = True
                word_to_count[w] = word_to_count.get(w, 0) + 1
        for w, c in word_to_count.items():
            word_to_idf[w] = math.log(len(docs) * 1.0 / c)
        return word_to_idf

    def _get_idf(self, word):
        return self.word_to_idf.get(word, self.max_idf)

    def _sum_weight(self, words):
        sum_weight = 0
        for w in words:
            sum_weight += self._get_idf(w)
        return sum_weight

    def _prefix(self, key, threshold, weight_on=False):
        if len(key) == 0:
            return []

        last_pos = len(key)
        if weight_on:
            overlap_weight = self._sum_weight(key) * threshold
            for i, w in enumerate(reversed(key)):
                if overlap_weight - self._get_idf(w) <= 0:
                    last_pos = len(key) - i
                    break
                else:
                    overlap_weight -= self._get_idf(w)
        else:
            last_pos = len(key) - int(math.ceil(len(key) * threshold)) + 1

        return key[:last_pos]

    # if Jaccard(s, t) >= threshold, the function will return the real similarity; Otherwise, it will return 0.
    def _jaccard(self, s, t, threshold, weight_on):
        set_s = set(s)
        set_t = set(t)
        if weight_on:
            sum1 = self._sum_weight(set_s)
            sum2 = self._sum_weight(set_t)
            if sum1 < sum2:
                if sum1 < sum2 * threshold:
                    return 0
            else:
                if sum2 < sum1 * threshold:
                    return 0
            intersect = self._sum_weight(set_s & set_t)
            union = sum1 + sum2 - intersect
        else:
            if len(s) < len(t):
                if len(s) < len(t) * threshold:
                    return 0
            else:
                if len(t) < len(s) * threshold:
                    return 0
            intersect = len(set_s & set_t)
            union = len(set_s) + len(set_t) - intersect

        if union != 0 and intersect * 1.0 / union + 1e-6 >= threshold:
            return intersect * 1.0 / union
        else:
            return 0

    def selfjoin(self, threshold, weight_on=False):
        if threshold < 0 or threshold > 1:
            raise Exception("threshold is not in the range of [0, 1]")
        # Compute IDF for each word
        k_list = [k for k, o in self.k_o_list]
        self.word_to_idf = self._idf(k_list)
        self.max_idf = math.log(
            len(k_list) * 2.0)  # For the words that are not in docs, their idf will be set to self.max_idf

        k_o_list = self.k_o_list

        # Sort the elements in each joinkey in decreasing order of IDF
        sk_list = []
        for k, o in k_o_list:
            sk = sorted(k, key=lambda x: (self._get_idf(x), x), reverse=True)
            sk_list.append(sk)

        # (1) Generate candidate pairs whose prefixes share elements;
        # (2) Compute the similarity of the candidate pairs and return the ones whose similarity is above  the threshold
        idx = InvertedIndex()

        joined = []
        for i, sk in enumerate(sk_list):
            prefix = self._prefix(sk, threshold, weight_on)
            ids = idx.get(*prefix)
            for j in ids:
                sim = self._jaccard(sk, sk_list[j], threshold, weight_on)
                if sim != 0:
                    joined.append((k_o_list[i], k_o_list[j], sim))

            for w in prefix:
                idx.insert(w, i)

        return joined

    def join(self, other_k_o_list, threshold, weight_on=False):
        if threshold < 0 or threshold > 1:
            raise Exception("threshold is not in the range of [0, 1]")

        k_o_list1 = self.k_o_list
        k_o_list2 = other_k_o_list

        # Compute IDF for each word
        k_list = [k for k, o in k_o_list1] + [k for k, o in k_o_list2]
        self.word_to_idf = self._idf(k_list)
        self.max_idf = math.log(
            len(k_list) * 2.0)  # For the words that are not in docs, their idf will be set to self.max_idf

        # Sort the elements in each joinkey in decreasing order of IDF
        sk_list1 = []
        for k, o in k_o_list1:
            sk = sorted(k, key=lambda x: (self._get_idf(x), x), reverse=True)
            sk_list1.append(sk)

        sk_list2 = []
        for k, o in k_o_list2:
            sk = sorted(k, key=lambda x: (self._get_idf(x), x), reverse=True)
            sk_list2.append(sk)

        # (1) Generate candidate pairs whose prefixes share elements;
        # (2) Compute the similarity of the candidate pairs and return the ones whose similarity is above  the threshold
        idx = InvertedIndex()

        for i, sk in enumerate(sk_list1):
            prefix = self._prefix(sk, threshold, weight_on)
            for w in prefix:
                idx.insert(w, i)

        joined = []
        for j, sk in enumerate(sk_list2):
            prefix = self._prefix(sk, threshold, weight_on)
            ids = idx.get(*prefix)
            for i in ids:
                sim = self._jaccard(sk, sk_list1[i], threshold, weight_on)
                if sim != 0:
                    joined.append((k_o_list1[i], k_o_list2[j], sim))
        return joined
