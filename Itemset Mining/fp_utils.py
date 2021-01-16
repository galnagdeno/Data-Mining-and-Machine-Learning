import numpy as np
import pandas as pd
from itertools import chain

def is_linear(node):
    '''
    Returns wheter the passed tree is linear.
    If so, returns a list of `_FP_Node` objects.
    '''
    branch = []
    while True:
        if not node.childrem:
            return branch
        elif len(node.childrem) > 1:
            return False
        else:
            node = next(iter(node.childrem.values()))
            branch.append(node)

def _get_paths(node):
    '''
    Returns the conditional paths from nodes named `node` in the passed tree.
    '''
    paths = []
    while node:
        path = []
        parent_node = node.parent
        while parent_node.name != 'root':
           path.append(parent_node.name) 
           parent_node = parent_node.parent
        path = node.count, path
        paths.append(path)
        if not node is node.node_link:
            node = node.node_link
        else:
            node = None
    return paths

def get_combinations(iterable):
    return chain.from_iterable(_combinations(iterable, r)
                        for r in range(1, len(iterable) + 1))

def _combinations(iterable, r):
    '''
    Modified `itertools.combinations` function. Also returns the minimum
    support in each combination.
    '''
    pool = iterable
    n = len(pool)
    if r > n:
        return
    indices = list(range(r))
    r_el = []
    sup = float('inf')
    for i in indices:
        r_el.append(iterable[i].name)
        if iterable[i].count < sup:
            sup = iterable[i].count
    yield sup, r_el
    while True:
        for i in reversed(range(r)):
            if indices[i] != i + n - r:
                break
        else:
            return
        indices[i] += 1
        for j in range(i+1, r):
            indices[j] = indices[j-1] + 1
        r_el = []
        sup = float('inf')
        for i in indices:
            r_el.append(iterable[i].name)
            if iterable[i].count < sup:
                sup = iterable[i].count
        yield sup, r_el


def generate_conditional_tree(tree, last_obj, minsup):
    '''
    Gets the conditional tree of the passed item.

    Parameters
    ----------

    tree: _FP_Node
        The root of an arbitrary fp-tree.
    last_obj: str
        Name of the last object added to the prefix in the "iteration".
    minsup: int
        Minimum support threshold for an itemset to be considered frequent.
    '''
    #gets the paths from `last_obj` nodes' parents to `root`
    paths = _get_paths(tree.header_table[last_obj])

    #build a data frame based on the generated paths. The `count`
    #information is stored in the binary entry: 0/NaN means that an entry
    #didn't occur; 1+ means the entry occured n times.
    df = pd.DataFrame(columns=tree.header_order[0
                        :tree.header_order.index(last_obj)])
    index = 0
    for path in paths:
        count = path[0]
        df.loc[index, path[1]] = count
        index += 1
    return generate_FP_tree(df, minsup)


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
        `_FP_Node` object which consists of the root of the FP-tree
        constructed based on the data set provided.
        The root is the null item.
    '''
    ord_items = df.sum(skipna=True) #O(|D|*|I|)
    ord_items = ord_items[ord_items >= minsup] #O(|I|)
    ord_items.sort_values(ascending=False, inplace=True) #O(|I| * lg |I|)

    root = _FP_Node('root', items=ord_items.index)
    
    for trans in df.index: #O(|D|)
        current_node = root
        for occurence in ord_items.index: #O(|I|)
            count = df.loc[trans, occurence]
            if count != np.NaN and count > 0: #O(1)
                #add child if not `occurence` in childrem
                current_node.add_child(occurence)
                #changes `current_node` to its child `occurence`
                current_node = current_node.childrem[occurence]
                #populates the header table
                if not occurence in root.header_table:
                    root.header_table[current_node.name] = current_node
                    root.last_occ[occurence] = current_node #instead of None

                #makes the node link from the last occurence of `occurence`
                #to this node
                if current_node.count == 0:
                    previous = root.last_occ[occurence]
                    previous.node_link = current_node
                    #changes the last occurence of `occurence` to this node
                    root.last_occ[occurence] = current_node

                #adds 1 to the child's counter
                current_node.count += count
    
    return root

class _FP_Node:
    '''
    A node of an arbitrary FP-tree.

    Parameters
    ----------
        name: str
            Name of the item this node represents
        parent: _FP_Node (None)
            `_FP_Node` object which has this node as a child.
            If None, this node is assumed to be the root of a tree.
    
    Attributes
    ----------
        name: str
            Name of the item this node represents
        parent: _FP_Node
            `_FP_Node` object which has this node as a child.
        childrem: dict
            Dictionary of `_FP_Node` objects which are childrem of this
            particular node. The keys are the names of the objects.
        count: int
            Number of times this node has apeared in transactions.
        node_link: _FP_Node
            Pointer to the next element of the same name as `self`
        last_occ: dict
            Each key is an item name and each corresponding item is the
            last occurence of an item with such name.
            Helps in the construction of the links between same name nodes.
            ONLY PRESENT IF THE NODE IS THE ROOT NODE.
        header_table: dict
            Each key is an item name and each corresponding item is the
            firs occurence of an item with such name
            ONLY PRESENT IF THE NODE IS THE ROOT NODE.

    Methods
    -------
        add_child
            Creates a new `_FP_Node` object which is a child of this node.
    '''
    def __init__(self, name, parent=None, items=None):
        self.name = name
        self.parent = parent
        self.childrem = {}
        self.count = 0
        self.node_link = None
        if name == 'root':
            self.last_occ = {item: None for item in items}
            self.header_table = {}
            self.header_order = tuple(items)

    def add_child(self, name):
        if not name in self.childrem:
           self.childrem[name] = _FP_Node(name, parent=self)
