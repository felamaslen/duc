## class to scan a directory

from os import listdir
from os.path import join, getsize, isdir, islink, isfile

import threading

import tree

class Scanner():
    def scanDir(self, root, rootName):
        data = [rootName, 0, []]

        for name in listdir(root):
            filename = join(root, name)

            if (self.onProgress):
                self.onProgress(name)

            if (isdir(filename) and not islink(filename)):
                scan = self.scanDir(filename, name)

                data[2].append(scan)

                data[1] += scan[1]

            elif (isfile(filename)):
                size = getsize(filename)

                data[2].append([name, size, None])

                data[1] += size

        return data


    def run(self):
        self.data = self.scanDir(self.dir, self.dir)

        self.onProgress(self.statusDone)

        self.onDone(self.data)

    def __init__(
            self,
            theDir,
            onProgress = None, onDone = None,
            statusDone = None
            ):

        #threading.Thread.__init__(self)
        #self.daemon = True

        self.dir = theDir

        self.data = []

        self.onProgress = onProgress
        self.onDone     = onDone
        self.statusDone = statusDone
