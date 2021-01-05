from itertools import chain, combinations

#bruteforce itemset mining
def mine_itemset_BF(dataset, items, minsup):
    '''
    dict, iterable, int -> list
    
    -dataset is a dict in which each key is a transaction that maps to
    a set of items.
    
    -items is the itemset that one wants to mine.
    
    -minsup is the minimum suport threshold
    '''
    #O(|I| * |D| * (2 ** |I|))
    frequent = []
    for itemset in power_set(items): # O(2 ** (len(items)))
        sup = compute_support(itemset, dataset) # O(|I| * |D|)
        if sup >= minsup:
            frequent.append(itemset)
            
    return frequent

def compute_support(itemset, dataset):
    #O(|I| * |D|)
    sup = 0
    for tid in dataset: # len(dataset)
        if dataset[tid].issuperset(itemset): # O(len(itemset))
            sup += 1
    return sup

def power_set(items):
    return chain.from_iterable(combinations(items, r) 
                               for r in range(len(items) + 1))

#itertools.combinations returns each r-length combination from
#the given iterable

#chain gets an iterable of subiterable and return elements from each
#subiterable untill untill it is exhausted and then moves on to the next one

