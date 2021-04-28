class Poslist:
    def __init__(self, suffix, prefix=None, first_row=False, dataset=None):
        positions = {}
        if first_row:
            for i in range(len(dataset)):
                sequence = dataset[i]
                line = []
                while True:
                    j = 0
                    try:
                        ind = sequence.index(suffix.sequence, start=j)
                        line.append(ind)
                        j = ind + 1
                    except ValueError:
                        break
                if line:
                    position[i] = line
            self.sequence = suffix
        else:
            for i in prefix.poslist:
                suffix_list = suffix.poslist.get(i)
                if suffix_list:
                    j = 0
                    while (suffix_list[j] <= prefix.poslist[i][0] and
                                                    j < len(suffix_list)):
                        j += 1
                    line = suffix_list[j:]
                if line:
                    position[i] = line
            self.sequence = prefix.sequence + suffix.sequence[-1]

        self.poslist = positions
        self.support = len(positions)

def spade(dataset, minsup, alphabet):
    level = []
    for char in alphabet:
        candidate = Poslist(char, first_row=True, dataset=dataset)
        if candidate.support >= minsup:
            level.append(candidate)
    frequent = {}
    mine_spade(level, minsup, frequent)
    return frequent

def mine_spade(level, minsup, frequent):
    for leaf in level:
        frequent[leaf.sequence] = leaf.support
        new_level = []
        for sibling in level:
            new_seq = Poslist(sibling, leaf)
            if new_seq.support >= minsup:
                new_level.append(new_seq)
        if new_level:
            mine_spade(new_level, minsup, frequent)
