def genmax(prefix_class, minsup, maximal_list):
    uni = set()
    uni = uni.union(item[0]) for item in prefix_class
    for maximal in maximal_list:
        if uni.issubset(item):
            return
    for i in range(len(prefix_class)):
        item_i = prefix_class[i]
        new_prefix_class = []

        for j in range(i + 1,  prefix_class):
            item_j = prefix_class[j]
            new_item = item_i[0].union(item_j[0])
            t_new_item = item_i[1].difference(item_j[1])
            if len(t_new_item) >= minsup:
                new_prefix_class.append((new_item, t_new_item))
        if new_prefix_class:
            genmax(new_prefix_class,  minsup, maximal_list)
        for maximal in maximal_list:
            if item_i[0].issubset(maximal):
                maximal_list.append(item_i[0])
