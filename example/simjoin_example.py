from deeper.entity_resolution.simjoin import SimJoin, wordset
if __name__ == "__main__":
    # Example for join

    print "\n==== SimJoin (Wordset) ===="
    o_list1 = ["a b c d", "a b c", "b c d", "a"]
    o_list2 = ["a b c d e f", "a b c d"]
    k_o_list1 = [(wordset(o), o) for o in o_list1]
    k_o_list2 = [(wordset(o), o) for o in o_list2]

    print "Data:"
    print "o_list1 = ", o_list1
    print "o_list2 = ", o_list2

    sj = SimJoin(k_o_list1)

    res = sj.join(k_o_list2, 0.4)
    print "Result:"
    for r in res:
        print r

    w_res = sj.join(k_o_list2, 0.4, True)
    print "Result (weight):"
    for r in w_res:
        print r