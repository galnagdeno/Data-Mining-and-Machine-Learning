import pandas as pd
from itertools import combinations,  chain

def association_rules(frequent,  minconf):
    association_rules = pd.DataFrame({'rule':[], 'support': [],
                                      'confidence': []})
    for i in range(frequent.shape[0]):
        item = frequent.loc[i, 'itemset']
        candidates = []
        candidates.[chain.from_iterable(combinations(item,  r)
                                     for r in range(1, len(item)))]
        for j in range(len(candidates)):
            subitem = candidates.pop()
            subitem_sup = frequent['support'][frequent['itemset' == subitem]].values[0]
            conf = frequent.loc[i, 'support'] / subitem_sup
            if conf >= minconf:
                association_rules.append(dict(zip([subitem,
                                item.difference(set(subitem)),
                                frequent.loc[i,  'support'], 
                                conf])), ignore_index=True)
            else:
                for subsubitem in chain.from_iterable(combinations(subitem, r)
                                            for r in range(1,  len(subitem))):
                    candidates.remove(subsubitem)
    return association_rules
