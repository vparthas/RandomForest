import sys
import random
from DecisionTree import create_entry, generate_tree, traverse_tree

def main(argv, argc):
    if not argc >= 3:
        return

    with open(argv[1], 'r') as infile:
        lines = infile.readlines()

    #defaults
    num_trees = 100
    tree_size = 100
    if argc > 3:
        num_trees = int(argv[3])
    if argc > 4:
        tree_size = int(argv[4])

    items = []
    attrs = None
    for line in lines:
        key, val = create_entry(line)
        if not attrs:
            attrs = val.keys()
        items.append((key, val))

    num_attrs = len(attrs)
    if argc > 5:
        num_attrs = int(argv[5])

    trees = []
    for i in range(num_trees):
        attr_sample = [attrs[i] for i in random.sample(xrange(len(attrs)), num_attrs)]
        trees.append(generate_tree(rand_items(items, tree_size), attr_sample))

    with open(argv[2], 'r') as infile:
        lines = infile.readlines()
    entries = []
    for line in lines:
        entries.append(create_entry(line))

    k = len(set([x[0] for x in entries]))
    results = [[0] * k for i in range(k)]
    for key, val in entries:
        result = majority_vote(trees, val)
        results[key - 1][result - 1] += 1

    for i in range(len(results)):
        line = ''
        for j in range(len(results[i])):
            line += str(results[i][j]) + ' '
        print line

def majority_vote(trees, item):
    votes = {}
    for tree in trees:
        vote = traverse_tree(tree, item)
        votes.setdefault(vote, 0)
        votes[vote] += 1
    return max(votes, key=votes.get)

def rand_items(items, n):
    for i in range(n):
        yield random.choice(items)

if __name__ == '__main__':
    main(sys.argv, len(sys.argv))
