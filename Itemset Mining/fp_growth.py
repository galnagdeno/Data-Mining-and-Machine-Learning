import pandas as pd
from fp_utils import *

def fp_growth(df, minsup):
    frequent = {'support':[], 'itemset': []}
    tree = generate_FP_tree(df, minsup)
    mine_tree(tree, [], frequent, minsup)
    frequent = pd.DataFrame(frequent)
    return frequent

def mine_tree(root_node, sufix, frequent_items, minsup):
    '''
    Parameters
    ----------
    sufix: list
        list of objects already in the current mining path. Each item is
        the name of the object type and not a pointer to a node.
    '''
    linearity = is_linear(root_node)
    if linearity:
        for comb in get_combinations(linearity):
            new_seq = sufix + comb[1]

            frequent_items['support'].append(comb[0])
            frequent_items['itemset'].append(new_seq)
    else:
        for freq in reversed(root_node.header_order):
            item = root_node.header_table[freq]
            sup = item.count
            while item.node_link and not item.node_link is item:
                item = item.node_link
                sup += item.count
            new_seq = sufix + [freq]
            frequent_items['support'].append(sup)
            frequent_items['itemset'].append(new_seq)
            new_tree = generate_conditional_tree(root_node, freq, minsup)
            if new_tree.childrem:
                mine_tree(new_tree, new_seq, frequent_items, minsup)
