from itertools import chain

def _is_linear(node):
    '''
    Returns wheter the passed tree is linear.
    '''
    branch = [node]
    while True:
        if not node.childrem:
            return branch
        elif len(node.childrem) > 1:
            return False
        else:
            node = next(iter(node.childrem.values()))
            branch.append(node)

def _get_paths(item):

def _get_combinations(iterable):
    return chain.from_iterable(_combinations(iterable, r)
                        for r in range(len(iterable) + 1))

def _combinations(iterable, r):
    pool = iterable
    n = len(pool)
    if r > n:
        return
    indices = list(range(r))
    r_el = []
    sup = float('inf')
    for i in indices:
        r_el.extend(iterable[i])
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
            r_el.extend(iterable[i])
            if iterable[i].count < sup:
                sup = iterable[i].count
        yield sup, r_el

def get_ord_items(df, minsup):
    ord_items = df.sum() #O(|D|)
    ord_items = ord_items[ord_items >= minsup] #O(|I|)
    ord_items.sort_values(ascending=False) #O(|I| * lg |I|)
    return ord_items

def _generate_conditional_tree():
    pass

def generate_FP_tree(df, minsup, ord_items): #O(|D| * |I|)
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
    root = Node('root', ord_items.index)
    
    for trans in df.index: #O(|D|)
        current_node = root
        for occurence in ord_items.index: #O(|I|)
            if df.loc[trans, occurence]: #O(1)
                #add child if not `occurence` in childrem
                current_node.add_child(occurence)
                #changes `current_node` to its child `occurence`
                current_node = current_node.childrem[occurence]
                #populates the header table
                if not occurence in root.header_table:
                    root.header_table = current_node
                    root.last_occ[occurence] = current_node #instead of None

                #makes the node link from the last occurence of `occurence`
                #to this node
                previous = root.last_occ[occurence]
                previous.node_link = current_node
                #changes the last occurence of `occurence` to this node
                root.last_occ[occurence] = current_node

                #adds 1 to the child's counter
                current_node.count += 1
    
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
        node_link: Node
            Pointer to the next element of the same name as `self`
        last_occ: dict
            Each key is an item name and each corresponding item is the
            last occurence of an item with such name.
            ONLY PRESENT IF THE NODE IS THE ROOT NODE.
        header_table: dict
            Each key is an item name and each corresponding item is the
            firs occurence of an item with such name

    Methods
    -------
        add_child
            Creates a new `Node` object which is a child of this node.
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
            self.header_order = items.copy()

    def add_child(self, name):
        if not name in self.childrem:
           self.childrem[name] = Node(name, self)
