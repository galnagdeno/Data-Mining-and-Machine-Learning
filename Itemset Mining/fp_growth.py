import numpy as np
import pandas as pd
from itertools import combinations, chain

def fp_growth(root_node, minsup):
    frequent = pd.DataFrame({'support': [],  'itemset': []})
    def mine_tree(fp_tree,  frequent_itemset):
        is_linear = is_linear(fp_tree)
        if is_linear:
            for comb in chain.from_iterable(combinations(is_linear[:-1], r)
                                            for r in range(len(is_linear))):
                #this procedure is not apropiate,  since this concatenation
                #is done in linear time. But that's the way to go without
                #writing a whole new `combinations` function, since it can
                #only return tuples.
                comb = comb + (frequent_itemset, )
                frequent.append(dict(zip([frequent_itemset.count, count])), 
                                ignore_index=True)
        else:
            

def is_linear(fp_tree,  branch=[]):
    '''
    Returns whether the passed tree is linear. If True,  also return
    a list of its node,  else,  return a header table with the nodes
    present in the subtree.
    '''
    branch.appennd(fp_tree)
    if not fp_tree.childrem:
        return True, branch
    if len(fp_tree.childrem) > 1:
        return False, []
    else:
        return is_linear(fp_tree.childrem[list(fp_tree.childrem.keys())[0]], 
                         branch)
    
def generate_FP_tree(df, minsup): #O(|D| * |I|)
    '''
    Constructs a FP-tree for use in a FP-growth algorithm.

    Parameters
    ----------
    df: pd.DataFrame
        A binary database in which each columns is an item and each
        row consists of 0/1 or True/False, indicating if a certain item
        was present in that transaction.
    minsup: int
        minimum support threshold for which an item is frequent.
    
    Returns
    -------
        `Node` object which consists of the root of the FP-tree
        constructed based on the data set provided.
        The root is the null item.
    '''
    ord_items = df.sum() #O(|D|)
    ord_items = ord_items[ord_items >= minsup] #O(|I|)
    ord_items.sort_values(ascending=False).index #O(|I| * lg |I|)
    
    root = Node('root')
    
    current_node = root
    for trans in df.index: #O(|D|)
        for occurence in ord_items: #O(|I|)
            if df.loc[trans, occurence]: #O(1)
               current_node.add_child(occurence) #O(1) 
               #points to the child
               current_node = current_node.childrem[occurence] #O(1)
               root.header_table[current_node.name].add(current_node)
               #adds 1 to the child's counter
               current_node.count += 1
        current_node = root
    
    return root

    
class Node:
    #first time implementing a tree
    '''
    A node of an arbitrary tree with a parent an a list of childrem.

    Parameters
    ----------
        name: str
            Name of the item this node represents
        parent: Node (None)
            `Node` object which has this node as a child.
            If None, this node is assumed to be the root of a tree.
    
    Attributes
    ----------
        name: str
            Name of the item this node represents
        parent: Node
            `Node` object which has this node as a child.
        childrem: dict
            Dictionary of `Node` objects which are childrem of this
            particular node. The keys are the names of the objects.
        count: int
            Number of times this node has apeared in transactions.
        header_table: dict
            Each item name is a key that identifies a set of `Node`
            objects of the same name.
            ONLY PRESENT IF THE NODE IS THE ROOT NODE.

    Methods
    -------
        add_child
            Creates a new `Node` object which is a child of this node.
    '''
    def __init__(self, name, parent=None, items):
        self.name = name
        self.parent = parent
        self.childrem = {}
        self.count = 0

        if name == 'root':
            self.header_table = {item: [] for item in items}

    def add_child(self, name):
        if not name in self.childrem:
           self.childrem[name] = Node(name, self)
