import sys
import os
from copy import deepcopy

def main(argv, argc):
    if not argc == 3:
        return

    with open(argv[1], 'r') as infile:
        lines = infile.readlines()

    training_set = {}
    attrs = None
    for line in lines:
        key, val = create_entry(line)
        if not attrs:
            attrs = val.keys()
        training_set.setdefault(key, []).append(val)

    decision_tree = construct_tree(training_set, attrs)

    with open(argv[2], 'r') as infile:
        lines = infile.readlines()

    k = len(training_set.keys())
    results = [[0] * k for i in range(k)]
    for line in lines:
        key, val = create_entry(line)
        result = traverse_tree(decision_tree, val)
        results[key - 1][result - 1] += 1

    for i in range(len(results)):
        line = ''
        for j in range(len(results[i])):
            line += str(results[i][j]) + ' '
        print line

def generate_tree(entries, attrs):
    training_set = {}
    for label, entry in entries:
        training_set.setdefault(label, []).append(entry)
    return construct_tree(training_set, attrs)

def traverse_tree(decision_tree, item):
    try:
        branches = decision_tree[1]
    except:
        return decision_tree

    val = item[decision_tree[0]]
    if val in branches:
        return traverse_tree(branches[val], item)
    return traverse_tree(branches.values()[0], item)

def create_entry(line):
    items = line.strip().split()
    key = int(items[0])

    val = {}
    for item in items[1:]:
        temp = item.split(':')
        val[int(temp[0])] = int(temp[1])

    return key, val

def construct_tree(training_set, attrs):
    if len(attrs) == 0:
        max_item = (-1, -1)
        for label, items in training_set.iteritems():
            if len(items) > max_item[1]:
                max_item = (label, len(items))
        return max_item[0]

    min_index = (-1, 2, None)
    for attr in attrs:
        index, vals = gini_index(training_set, attr)
        if not vals:
            return index

        if index < min_index[1]:
            min_index = (attr, index, vals)

    attrs = deepcopy(attrs)
    attrs.remove(min_index[0])
    ret = {}
    for val in min_index[2]:
        subset = create_subset(training_set, min_index[0], val)
        ret[val] = construct_tree(subset, attrs)

    return min_index[0], ret

def create_subset(training_set, attr, val):
    ret = {}
    for label, items in training_set.iteritems():
        ret[label] = [item for item in items if item[attr] == val]
        if len(ret[label]) == 0:
            del ret[label]
    return ret

def gini_index(training_set, attr):
    vals = set([])
    for label, items in training_set.iteritems():
        for item in items:
            vals.add(item[attr])

    total = 0
    counts = {}
    for label, items in training_set.iteritems():
        total += len(items)
        for val in vals:
            counts.setdefault(val, {})
            counts[val][label] = sum(1.0 for x in items if x[attr] == val)

    for label, items in training_set.iteritems():
        if len(items) == total:
            return label, None

    gini = 0
    for val in vals:
        val_sum = sum(counts[val].values())
        val_gini = 1.0
        for count in counts[val].values():
            val_gini -= (count / val_sum)**2
        gini += (val_sum / total) * val_gini

    return gini, vals

if __name__ == '__main__':
    main(sys.argv, len(sys.argv))
