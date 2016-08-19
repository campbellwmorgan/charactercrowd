"""
Manages the cache storage
and retrieval for a given character
"""
import json
import gzip
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
        with gzip.GzipFile(self.getFilePath(frameNo), 'w') as f:
            f.write(json.dumps(data))
            f.close()
        return True

    def fetch(self, frameNo):
        """
        Finds file and reads json data
        """
        with gzip.GzipFile(self.getFilePath(frameNo), 'r') as lines:
            data = False
            for line in lines:
                data = json.loads(line)
                break
            lines.close()
        if not data:
            raise Exception("No lines in file")
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
        return self.fileName + ".cache." + str(frameNo).zfill(4) + ".json.gz"

    def getFilePath(self, frameNo):
        return os.path.join(
                self.getBaseDir(),
                self.getFileName(frameNo)
                )




