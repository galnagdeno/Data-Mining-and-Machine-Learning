import numpy as np
import pandas as pd

def declat_mine(df, minsup):
    frequent = {'support': [], 'itemset': []}
    prefix = []
    for col in df.columns:
        d_col = set(df[df[col] == 0].index)
        support = df.shape[0] - len(d_col)
        if support >= minsup:
            prefix.append((set(col), d_col, support))
    declat(prefix, minsup, frequent)
    return pd.DataFrame(frequent)

   
def declat(prefix_class, minsup, frequent):
    '''
    Finds all itemsets with support greater or equal to `minsup`.
    Function performs recursively.

    Parameters
    ----------
    prefix_class: list(tuples)
        A list in which each element is a tuple that consist of an item, its
        diffset and its support.
        The first prefix class is actually the whole itemset supposed
        to be mined. Each element of the itemset shares the prefix class
        with the empty item (those frequent sole items).
        Notice that the second item of the tuple of each item in 
        `prefix_class` should be all transactions in which the item 
        doesn't appear in the data set.
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
        frequent['support'].append(first_item[2])
        frequent['itemset'].append(first_item[0])
        new_prefix_class = []

        for j in range(i+1, len(prefix_class)):
            second_item = prefix_class[j]
            d_union = second_item[1].difference(first_item[1])
            sup_union = first_item[2] - len(d_union)
            
            if sup_union >= minsup:
                uni_item = first_item[0].union(second_item[0])
                new_prefix_class.append((uni_item, d_union, sup_union))
        if new_prefix_class:
            declat(new_prefix_class, minsup, frequent)
