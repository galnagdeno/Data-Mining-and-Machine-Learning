def get_maximal(df, minsup):
    maximal = []
    pre = [(set(item), set(data.index[data[item] == 1])) for item in df.columns]
    return genmax(pre, minsup, maximal)

def genmax(prefix_class, minsup, maximal_list):
    uni = set()
    for item in prefix_class:
        uni = uni.union(item[0])
    for maximal in maximal_list:
        if uni.issubset(maximal):
            return
    for i in range(len(prefix_class)):
        item_i = prefix_class[i]
        new_prefix_class = []

        for j in range(i + 1,  len(prefix_class)):
            item_j = prefix_class[j]
            new_item = item_i[0].union(item_j[0])
            t_new_item = item_i[1].intersection(item_j[1])
            if len(t_new_item) >= minsup:
                new_prefix_class.append((new_item, t_new_item))
        if new_prefix_class:
            genmax(new_prefix_class,  minsup, maximal_list)
        else:
            for maximal in maximal_list:
                if item_i[0].issubset(maximal):
                    maximal_list.append(item_i[0])
