def charm(prefix_class,  minsup, closed_list):
    prefix_class.sort(key=lambda x: x[1])
    i = 0
    list_size = len(prefix_class)
    while i < list_size:
        item_i = prefix_class[i]
        new_prefix_class = []
        
        j = i + 1
        while j < list_size:
            item_j = prefix_class[j]
            new_item = item_i[0].union(item_j[0])
            t_new_item = item_i[1].difference(item_j[1])
            if len(t_new_item) >= minsup:
                if item_i[1] == item_j[1]:
                    prefix_class[i][0] = new_item
                    prefix_class.pop(j)
                elif item_i[1].issubset(item_j[1]):
                    prefix_class[i][0] = new_item
                    j += 1
                else:
                    new_prefix_class.append((new_item,  t_new_item))
                    j += 1
            list_size = len(prefix_class)
        i += 1
        if new_prefix_class:
            charm(new_prefix_class, minsup, closed_list)
        eq_tidset = False
        is_subset = False
        for closed in closed_list:
            is_subset = item[0].issubset(closed[0])
            eq_tidset = item[0]
        if not eq_tidset or is_subset:
            closed_list.append()
