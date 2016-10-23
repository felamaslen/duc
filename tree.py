## tree view methods

import math

def listToString(strng):
    if isinstance(strng, list):
        return "[" + ", ".join(map(listToString, strng)) + "]"

    return str(strng)

def dump(theList):
    print listToString(theList)

bitsAbbrev = [
    [0, "B"],
    [10, "KiB"],
    [20, "MiB"],
    [30, "GiB"],
    [40, "TiB"]
]

def formatBits(bits):
    expIndex = -1

    log2bits = 0 if bits == 0 else math.log(bits) / math.log(2)

    while (
        expIndex < len(bitsAbbrev) - 1 and
        log2bits >= bitsAbbrev[expIndex + 1][0]
    ):
        expIndex += 1

    exp = bitsAbbrev[expIndex][0]
    text = bitsAbbrev[expIndex][1]

    value = round(bits / math.pow(2, exp), 1)

    return (str)(value) + text

def addTreeData(tree, treeStore, rootRow = None):
    parentRow = treeStore.append(rootRow, [
        "%s" % tree[0], "%s" % formatBits(tree[1])
        ])

    if (tree[2] != None):
        for item in tree[2]:
            addTreeData(item, treeStore, parentRow)

