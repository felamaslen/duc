## class to scan a directory

from os import listdir
from os.path import join, getsize, isdir, islink, isfile

class Scanner:
    def onError(self):
        print "An error occurred!"

    def scanDir(self, root, rootName):
        tree = [rootName, 0, []]

        for name in listdir(root):
            filename = join(root, name)

            if (isdir(filename) and not islink(filename)):
                scan = self.scanDir(filename, name)

                tree[2].append(scan)

                tree[1] += scan[1]

            elif (isfile(filename)):
                size = getsize(filename)

                tree[2].append([name, size, None])

                tree[1] += size

        return tree


    def scan(self):
        self.tree = self.scanDir(self.dir, self.dir)

    def __init__(self, theDir):
        self.dir = theDir

        self.tree = []
