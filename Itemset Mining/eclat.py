import numpy as np
import pandas as pd

def eclat(prefix_class, minsup, frequent):
    '''
    Finds all itemsets with support greater or equal to `minsup`.
    Function performs recursively.

    Parameters
    ----------
    prefix_class: list(tuples)
        A list in which each element is a tuple that consist of an item and
        t(item).
        The first prefix class is actually the whole itemset supposed
        to be mined. Each element of the itemset shares the prefix class
        with the empty item.
        Notice that the second item of the tuple of each item in 
        `prefix_class` should be all transactions in which the item appears.
        That is, it is supposed that the item appears at least once in the 
        data set.
    minsup: int
        The minimum support threshold for which an itemset is frequent 
        in the data base.
    frequent: pd.DataFrame
        Two columns: 'support', 'itemset'. Only frequent itemsets.

    Returns
    -------
        None. Only modifies `frequent`.
    '''

    for i in range(len(prefix_class)):
        first_item = prefix_class[i]
        frequent.append(dict(zip(frequent.columns,
                                 [len(first_item[1]), first_item[0]])),
                                 ignore_index=True)
        new_prefix_class = []

        for j in range(i+1, len(prefix_class)):
            second_item = prefix_class[j]
            uni_item = first_item[0].union(second_item[0])
            t_union = first_item[1].intersection(second_item[1])
            sup_union = len(t_union)

            if sup_union >= minsup:
                new_prefix_class.append((uni_item, t_union))
        if new_prefix_class:
            eclat(new_prefix_class, minsup, frequent)
