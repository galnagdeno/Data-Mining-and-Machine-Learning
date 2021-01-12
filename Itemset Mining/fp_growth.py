def mine_tree(df):
    pass

def fp_growth(root_node, prefix, frequent_items, minsup):
    linearity = _is_linear(root_node)
    if linearity:
        for comb in _get_combinations(linearity):
            new_seq = prefix.extend(comb[1])
            frequent_items.append(dict(zip([comb[0], new_seq])), 
                                  ignore_index=True)
    else:
        for freq in reversed(root_node.header_order):
            new_seq = prefix.append(freq)
            sup = ord_items[freq]
            frequent_items.append(dict(zip([sup, new_seq])), 
                                  ignore_index=True)
            
