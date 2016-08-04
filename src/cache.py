"""
Manages the cache storage
and retrieval for a given character
"""
import json
import pymel.core as pm
import os

class Cache:

    def __init__(self, setName, fileName):
        self.setName = setName
        self.fileName = fileName
        self.baseDirSet = False

    def store(self, frameNo, data):
        """
        Finds file and encodes json
        """
        f = open(self.getFilePath(frameNo), 'w')
        json.dump(data, f)
        f.close()
        return True

    def fetch(self, frameNo):
        """
        Finds file and reads json data
        """
        f = open(self.getFilePath(frameNo), 'r')
        data = json.load(f)
        f.close()
        return data

    def getBaseDir(self):
        """
        Gets the base directory for this cacheFile
        """
        projectRoot = os.path.abspath(pm.workspace.getPath())
        cacheDir = os.path.join(
                projectRoot,
                'cache',
                'characterCrowd',
                self.setName,
                self.fileName
                )

        if not self.baseDirSet and not os.path.isdir(cacheDir):
            # make the directory
            os.makedirs(cacheDir)

        self.baseDirSet = True

        return cacheDir

    def getFileName(self, frameNo):
        return self.fileName + ".cache." + str(frameNo).zfill(4) + ".json"

    def getFilePath(self, frameNo):
        return os.path.join(
                self.getBaseDir(),
                self.getFileName(frameNo)
                )




