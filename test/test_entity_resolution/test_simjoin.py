from deeper.entity_resolution import simjoin
import unittest


class SimjoinTestCase(unittest.TestCase):
    def testSelfSimjoin(self):
        # ==== Self-SimJoin (Wordset) ====
        o_list = ["a b c d", "a b c", "b c d", "a", "a b c d e f", "a b c d e"]
        k_o_list = [(simjoin.wordset(o), o) for o in o_list]
        sj = simjoin.SimJoin(k_o_list)
        res = sj.selfjoin(0.4)
        w_res = sj.selfjoin(0.4, True)

        assert (len(res), len(w_res)) == (10, 4)

        # ==== Self-SimJoin (Gramset) ===="

        o_list = ["abcd", "abc", "bcd", "a", "abcdef", "abcde"]
        k_o_list = [(simjoin.gramset(o, 2), o) for o in o_list]
        sj = simjoin.SimJoin(k_o_list)
        res = sj.selfjoin(0.4)
        w_res = sj.selfjoin(0.4, True)
        assert (len(res), len(w_res)) == (6, 1)

    def testJoin(self):
        # ==== SimJoin (Wordset) ====
        o_list1 = ["a b c d", "a b c", "b c d", "a"]
        o_list2 = ["a b c d e f", "a b c d e"]
        k_o_list1 = [(simjoin.wordset(o, 2), o) for o in o_list1]
        k_o_list2 = [(simjoin.wordset(o, 2), o) for o in o_list2]
        sj = simjoin.SimJoin(k_o_list1)
        res = sj.join(k_o_list2, 0.4)
        w_res = sj.join(k_o_list2, 0.4, True)
        assert (len(res), len(w_res)) == (6, 1)

        # ==== SimJoin (Gramset) ====
        o_list1 = ["abcd", "abc", "a"]
        o_list2 = ["abcdef", "bcd", "abcde"]
        k_o_list1 = [(simjoin.gramset(o, 2), o) for o in o_list1]
        k_o_list2 = [(simjoin.gramset(o, 2), o) for o in o_list2]
        sj = simjoin.SimJoin(k_o_list1)
        res = sj.join(k_o_list2, 0.4)
        w_res = sj.join(k_o_list2, 0.4, True)
        assert (len(res), len(w_res)) == (4, 1)
