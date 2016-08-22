from nose.tools import *
import pymel.core as pm
import shutil
import os
import json
import gzip
from characterCrowd import CharacterCrowd
from gui import Gui

class GuiOverride(Gui):
    def __init__(self):
        ""


"""
End-To-End
test
"""
class testCharacterCrowd:

    @classmethod
    def setUpClass(self):
        cwd = os.path.dirname(os.path.realpath(__file__))
        # set project in tmp ddir
        self.projectPath = os.path.join(cwd, 'tmpProj')
        pm.mel.setProject(self.projectPath)
        # open mock file
        pm.openFile(os.path.join(cwd, 'mocks', 'mockController.ma'), f=1)
        self.cc = CharacterCrowd(createUI=False)
        self.item = pm.ls('main')[0]
        # clean out cache dir
        cacheDir = os.path.join(
                self.projectPath,
                'cache',
                'characterCrowd'
                )
        shutil.rmtree(cacheDir)

    @classmethod
    def tearDownClass(self):
        pm.newFile(f=1)
        # clear cache dir

    def testASetup(self):
        meshes = [
                "meshA",
                "meshB",
                "meshC",
                "meshD"
                ]
        self.meshes = pm.ls(meshes)
        keyable = [
                "controllerA",
                "controllerB",
                "controllerC",
                "controllerD",
                "main",
                ]
        self.keyableNodes = pm.ls(keyable)
        gui = GuiOverride()
        self.keyable = gui.allKeyableAttrs(self.keyableNodes)
        self.cc.setup(
                meshes = self.meshes,
                keyable = self.keyable,
                item = self.item,
                parentVis='main',
                prefix="testStandin"
                )

    def testBGenerate(self):
        # select item
        pm.select(self.item)
        # transform item
        self.item.translate.set((5,10,3))
        self.cc.generate()
        standIn = pm.ls('testStandin_standInCtrl')[0]
        eq_(int(standIn.translate.get()[0]), 5)

    def testCSelectChildren(self):
        pm.select(self.item)
        self.cc.selectChildren()
        eq_('testStandin_standInCtrl', pm.ls(sl=1)[0].name())

    def testDSaveState(self):
        self.standIn = pm.ls('testStandin_standInCtrl')[0]
        # add some keys to the controllers
        # and change some transforms
        contr1 = pm.ls('controllerA')[0]
        contr1.rotate.set((0,90,0))
        contr1.translate.set((5,3,2))
        pm.setKeyframe('controllerA.scaleX', t=1, v=1.3)
        pm.setKeyframe('controllerA.scaleX', t=5, v=1.9)
        # custom connected attribute
        # for testing dependency graph evaluations
        pm.setKeyframe('controllerB.testSrc', t=1, v=0.5)
        pm.select(self.standIn)
        self.cc.saveState()

        keys = pm.keyframe(
                'testStandin_standInCtrl.controllerAscaleX',
                q=1,
                kc=1
                )
        eq_(keys, 2)

    def testEFocusModel(self):
        self.standIn = pm.ls('testStandin_standInCtrl')[0]
        pm.select(self.standIn)
        self.cc.saveState()
        # move the main model a bit
        self.item.translate.set((40,0,0))
        self.cc.focusModel()

        trans = self.item.translate.get()

        eq_(int(trans[0]), 5)

    def testFCacheStandin(self):
        self.standIn = pm.ls('testStandin_standInCtrl')[0]
        pm.select(self.standIn)
        self.cc.cacheStandin(1,44)

        # check json file for frame
        cacheFilePath = os.path.join(
                self.projectPath,
                'cache',
                'characterCrowd',
                'testStandin',
                'testStandin_standInCtrl',
                'testStandin_standInCtrl.cache.0042.json.gz'
                )


        f = gzip.GzipFile(cacheFilePath, 'r')
        for line in f:
            data = json.loads(line)
            break
        eq_(data["controllerA.scaleX"]["value"], 1.9)
        f.close()

    def testGDuplicateStandin(self):
        self.standIn = pm.ls('testStandin_standInCtrl')[0]
        pm.select(self.standIn)
        self.cc.duplicateStandin()
        pm.setKeyframe('controllerB.testSrc', t=1, v=1.5)
        self.cc.saveState()
        # now cache that standin too
        self.cc.cacheStandin()

    def testHApplyMeshes(self):
        self.cc.applyMeshes(20)
        first = pm.getAttr('meshD1Shape.testAttr')
        second = pm.getAttr('meshD2Shape.testAttr')
        eq_(first, 0.5)
        eq_(second, 1.5)

    def testIDeleteMeshes(self):
        self.cc.deleteMeshes()
