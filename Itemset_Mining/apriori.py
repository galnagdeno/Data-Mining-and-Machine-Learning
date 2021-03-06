import numpy as np
import pandas as pd
from itertools import combinations

def apriori(df, minsup):
    '''
    Finds all itemsets with support greater of equal to `minsup`

    Parameters
    ----------
    df: pd.DataFrame
        one-hot DataFrame. Each entry can be either 0/1 or True/False.

    itemset: iterable
        Any iterable of characters or strings (if itemset is a string, 
        each character will be considered an item) to be mined.

    minsup: int
        The minum support threshold for which an itemset is frequent
        in the data base.

    Returns
    -------
    Pandas DataFrame with columns ['support', 'itemset'] of all itemsets
        whose support >= `minsup`.
    '''
    frequent = pd.DataFrame({'support':[], 'itemset':[]})
    #columns = set(df.columns) #|I|
    #level = [item for item in itemset if item in columns]
    level = [[item] for item in df.columns]
    call = 0
    while level:
        #print(f'CALL {call}')
        call += 1
        #print('frequent', frequent)
        #print('level:', level)
        to_pop = []
        support_list = compute_support(level, df)
        #print('support_list:', support_list)
        for i in range(len(level)): 
            if support_list[i] >= minsup:
                frequent = frequent.append(dict(zip(frequent.columns, 
                                         [support_list[i], level[i]])),
                                         ignore_index=True)
                #print(support_list[i], level[i])
            else:
                to_pop.append(i)
        #pops in reverse order to avoid index issues
        to_pop.reverse()
        #print('level:', level)
        #print('to_pop', to_pop)
        for i in to_pop:
            level.pop(i)
        level = extend_prefix_tree(level)

    return frequent
    

def compute_support(level, df):
    '''
    Computes the support of the elements of the level of a tree.

    Parameters
    ----------
    level: list
        Each element of the list is assumed to be a set of elements
        that could be in `df.columns`. Also, these elements are strings.
    df: pd.DataFrame
        one-hot DataFrame. Each entry can be either 0/1 or True/False.

    Returns
    -------
    list with the same length as level containing the support of each item.


    O(|I| * |D|)
    '''
    sup_list = []
    for item in level: 
        #transactions in which all entries are 1
        sup_list.append(df[item].all(axis=1).sum())

    return sup_list


def extend_prefix_tree(previous_level):
    '''
    Creates a new level for the prefix tree in which each new item is
    derived from the union of two previous frequent parents for optimization.

    Parameters
    ----------
    previous_level: list
        The previous level of the tree. Only frequent elements are present.
        Each element of the list is assumed to be a set of elements
        that could be in `df.columns`. Also, these elements are strings.
    
    Returns
    -------
    A list o lists with possible frequent candidates.


    O(|I|)
    '''

    new_level = []
    
#    comb = [item[0].union(item[1]) for item 
#                                        in combinations(previous_level, 2)]
#    size = len(previous_level) + 1
#    for item in comb:
#        if len(item) == size:
#            new_level.append(item)
    #print(len(previous_level))
    l = 0
    r = 1
    while l < len(previous_level):
        #print(f'l: {l}, r: {r}')
        if r >= len(previous_level):
            l += 1
            r = l + 1
        elif previous_level[l][:-1] == previous_level[r][:-1]:
            new_level.append(previous_level[l] + [previous_level[r][-1]])
            r += 1
        else:
            l += 1
            r = l + 1

    return new_level
