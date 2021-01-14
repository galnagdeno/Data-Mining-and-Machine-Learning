import pandas as pd
from itertools import chain, combinations

def mine_itemset_BF(dataset, minsup):
    '''
    pandas.DataFrame, iterable, int -> list
    
    -dataset is a dict in which each key is a transaction that maps to
    a set of items.
    
    -items is the itemset that one wants to mine.
    
    -minsup is the minimum suport threshold
    '''
    #O(|I| * |D| * (2 ** |I|))
    frequent = pd.DataFrame(columns={'support', 'itemset'})
    items = dataset.columns
    for itemset in power_set(items): # O(2 ** (len(items)))
        sup = dataset[itemset].all(axis=1).sum()
        #sup = compute_support(itemset, dataset) # O(|I| * |D|)
        if sup >= minsup:
            #change the following. Reasign is probably too costly.
            frequent = frequent.append(dict(zip(frequent.columns,
                            [sup, itemset])), ignore_index=True)
            
    return frequent

def compute_support(itemset, dataset):
    #O(|I| * |D|)
    sup = 0
    for tid in dataset: # len(dataset)
        if dataset[tid].issuperset(itemset): # O(len(itemset))
            sup += 1
    return sup

def power_set(s):
    x = len(s)
    masks = [1 << i for i in range(x)]
    for i in range(1, 1 << x):
        yield [ss for mask, ss in zip(masks, s) if i & mask]

def _power_set(items):
    return chain.from_iterable(combinations(items, r) 
                               for r in range(1,len(items) + 1))
