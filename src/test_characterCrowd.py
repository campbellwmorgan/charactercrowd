from nose.tools import *
import pymel.core as pm
import shutil
import os
import json
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
                "mesh1",
                "mesh2",
                "mesh3",
                "mesh4"
                ]
        self.meshes = pm.ls(meshes)
        keyable = [
                "controller1",
                "controller2",
                "controller3",
                "controller4",
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
        contr1 = pm.ls('controller1')[0]
        contr1.rotate.set((0,90,0))
        contr1.translate.set((5,3,2))
        pm.setKeyframe('controller1.scaleX', t=1, v=1.3)
        pm.setKeyframe('controller1.scaleX', t=5, v=1.9)
        pm.select(self.standIn)
        self.cc.saveState()

        keys = pm.keyframe(
                'testStandin_standInCtrl.controller1scaleX',
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
        self.cc.cacheStandin()

        # check json file for frame
        cacheFilePath = os.path.join(
                self.projectPath,
                'cache',
                'characterCrowd',
                'testStandin',
                'testStandin_standInCtrl',
                'testStandin_standInCtrl.cache.0042.json'
                )


        f = open(cacheFilePath, 'r')
        data = json.load(f)
        eq_(data["controller1.scaleX"]["value"], 1.9)
        f.close()

    def testApplyMeshes(self):
        self.cc.applyMeshes(20)

    def testDeleteMeshes(self):
        self.cc.deleteMeshes()
