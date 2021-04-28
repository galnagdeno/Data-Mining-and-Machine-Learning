from itertools import combinations, chain
from collections import OrderedDict

def mine_association_rules(frequent, minconf):
    rules = {}
    for itemset in frequent:
        if len(itemset) >= 2:
            subsets = OrderedDict((sub, 0) for sub in powerset(itemset))
            while subsets:
                maximal = subsets.popitem()[0]
                conf = frequent[itemset] / frequent[maximal]
                if conf >= minconf:
                    rules[f'{maximal} -> {itemset} \\ {maximal}'] = f'sup: {frequent[itemset]}, conf: {conf}'
                else:
                    for sub in powerset(maximal):
                        if sub in subsets:
                            del subsets[sub]


def powerset(iterator):
    return chain.from_iterable(combinations(iterator, r) for
                                r in range(1, len(iterator) + 1))
