import numpy as np
import pandas as pd

def declat(prefix_class, minsup, frequent):
    for i in range(len(prefix_class)):
        first_item = prefix_class[i]
        frequent.append(dict(zip(frequent.columns,
                                 [first_item[2], first_item[0]])),
                                 ignore_index=True)
        new_prefix_class = []

        for j in range(i+1, len(prefix_class)):
            second_item = prefix_class[j]
            uni_item = first_item[0].union(second_item[0])
            d_union = first_item[1].difference(second_item[1])
            sup_union = first_item[2] - len(d_union)
            
            if sup_union >= minsup:
                new_prefix_class.append((uni_item, d_union, sup_union))
        if new_prefix_class:
            declat(new_prefix_class, minsup, frequent)
