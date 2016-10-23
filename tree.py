## tree view methods

def listToString(strng):
    if isinstance(strng, list):
        return "[" + ", ".join(map(listToString, strng)) + "]"

    return str(strng)

def dump(theList):
    print listToString(theList)

def addTreeData(tree, treeStore, rootRow = None):
    parentRow = treeStore.append(rootRow, ["%s" % tree[0]])

    if (tree[2] != None):
        for item in tree[2]:
            addTreeData(item, treeStore, parentRow)

