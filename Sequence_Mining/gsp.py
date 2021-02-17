from itertools import combinations

class Prefix_tree:
    '''Node for a sequence prefix tree.

    Parameters
    ----------
    sequence: str
        A string with the sequence the node represents. If `None`, the
        node is supposed to be the root.
    parent: Prefix_tree object
        The Prefix_tree object of which the current node is a child of.
        If `None`, the node is supposed to be the root.

    Attributes:
    sequence: str
        A string with the sequence the node represents. If `None`, the
        node is supposed to be the root.
    parent: Prefix_tree object
        The Prefix_tree object of which the current node is a child of.
        If `None`, the node is supposed to be the root.
    childrem: list
        A list of childrem of this node.
       '''
    def __init__(self, sequence=None, parent=None):
        self.sequence = sequence
        self.parent = parent
        self.childrem = []
        self.support = 0

    def add_child(self, name):
        new_node = Prefix_tree(name, self)
        self.childrem.append(new_node)

def gsp(dataset, alphabet, minsup):
    '''
    Finds all sequences of characters in alphabet that appear in the
    dataset.

    Parameters
    -----------
    dataset: iterable
        A iterable of strings to be mined.
    alphabet:
        The characters that the subsequences are supposed to be composed of.
    minsup: int
        Number of times that a sequence must appear in the dataset as a
        subsequence to be considered frequent.

    Returns
    --------
    A dictonary with the frequent sequences along with its respectives supports.
    '''
    frequent = dict()
    root = Prefix_tree()
    for char in alphabet: #O(|alphabet|)
        root.add_child(char)
    level = root.childrem

    while level: #O(|L|) -- L = largest element in dataset
        print('old:', [item.sequence for item in level])
        new_level = []
        sup_list = compute_support(level, dataset) #O(|level|*|dataset|*|L|)

        for i in range(len(level)): #O(|alphabet| ^ |L|)
            if sup_list[i] >= minsup:
                level[i].support = sup_list[i]
                frequent[level[i].sequence] = sup_list[i]
                new_level.append(level[i])
        print('new:', [item.sequence for item in new_level])
        level = extend_prefix_tree(new_level, frequent)
    return frequent

def compute_support(level, dataset): #O(|level| * |dataset| * |sequence|)
    '''
    Counts how many times each sequence in level appear in the dataset as
    a subsequence.
    
    Parameters
    ----------
    level: `list` of `Prefix_tree` objects
    dataset: iterable of strings

    Returns
    -------
    A `list` of `int`s with the support of each element in `level`.
    '''
    support = [0 for i in level] #O(|level|)
    for i in range(len(level)): #O(|level|)
        candidate = level[i].sequence
        for sequence in dataset: #O(|dataset|)
            if is_subsequence(candidate, sequence): #O(|sequence|)
                support[i] += 1
    return support

def extend_prefix_tree(level, frequent): #O(|level|^2 * |leaf|)
    '''
    Creates a new level of the prefix tree.

    Parameters
    ----------
    level: `list` of `Prefix_tree` objects
    frequent: `dict`
        The dictionary that stores the frequent sequences.

    Returns
    -------
    A `list` of `Prefix_tree` objects linked to their parents accordingly.
    '''
    new_level = []
    for leaf in level: #O(|level|)
        for sibling in leaf.parent.childrem: #O(|level|)
            if sibling.support:
                new_seq = leaf.sequence + sibling.sequence[-1]
                for subseq in combinations(new_seq, len(new_seq) - 1): #O(|leaf|)
                    if not subseq[0] in frequent: #O(1)
                        break
                else:
                    leaf.add_child(new_seq)
                    new_level.append(leaf.childrem[-1])
    return new_level

def is_subsequence(seq1, seq2): #O(|seq2|)
    '''
    Checks if seq1 is substring of seq2
    '''
    i = len(seq1) - 1
    j = len(seq2) - 1
    while i >= 0 and j >= 0:
        if seq1[i] == seq2[j]:
            i -= 1
        j -= 1
    return i < 0

