import pymel.core as pm
import math
from cache import Cache
from gui import Gui
from source import Source
from coreNode import CoreNode
from standIn import StandIn
from datetime import datetime

class CharacterCrowd:

    def __init__(self, createUI=True):
        self.source = False
        self.setupCoreNode()
        if createUI:
            self.createUI()

    def setup(
            self,
            item=False,
            meshes=False,
            keyable=False,
            prefix=False,
            parentVis=False,
            ):
        """
        Sets up and initialises the source mesh
        """
        # add the parent visibility node
        # to the core node store so it can be hidden
        # on render
        self.coreNode.addParentGroup(parentVis)
        # now make the source node
        self.source = Source(
                meshes=meshes,
                keyable=keyable,
                parentVis=parentVis,
                prefix=prefix,
                node=item
                )

    def load(self):
        """
        Loads the source from the selected item
        """
        sel = pm.ls(sl=1)
        self.source = Source(selection=True)

    def generate(self, *args):
        """
        Creates a bounding box representing the mesh
        containing attributes that link back to the mesh
        AND adds the name of this new generated mesh to a string
        attribute on the original mesh
        """
        if not self.source:
            raise Exception(
                    "Must load or setup Source object first"
                    )
        newStandin = StandIn(
                coreNode=self.coreNode,
                source=self.source,
                ctrlName=(self.source.prefix + "_standInCtrl")
                )
        newStandin.create()

    def getStandInFromSelection(self):
        """
        Returns a stand in instance from
        selection
        """
        sel = pm.ls(sl=1)
        if len(sel) is not 1:
            raise Exception(
                    "Please select an stand in first"
                    )
        return StandIn(
                coreNode=self.coreNode,
                source=self.source,
                node=sel[0],
                ctrlName=(self.source.prefix + "_standInCtrl")
                )

    def selectChildren(self, *args):
        pm.select(
                self.source.children
                )

    def focusModel(self, *args):
        """
        Places the model in place of the bounding
        box and applies cached positioning if available
        """
        standIn = self.getStandInFromSelection()
        standIn.focus()

    def saveState(self, *args):
        """
        Saves snapshot and any keyed info
        to standin
        """
        standIn = self.getStandInFromSelection()
        standIn.save()

    def cacheStandin(self, *args):
        """
        Iterates through all the frames in the
        current range saving all the selected attributes
        to a json cache file
        """
        standIn = self.getStandInFromSelection()
        standIn.focus()
        standIn.cache()

    def deleteItem(self, *args):
        """
        Deletes the standin and removes references
        """
        standIn = self.getStandInFromSelection()
        standIn.delete()

    def applyMeshes(self, keyFrame=False):
        """
        Iterates through every standin found in
        the scene and replaces it with the meshes
        (run during render)
        """
        if not keyFrame:
            keyFrame = int(pm.currentTime(q=1))
        startTime = datetime.now()
        self.coreNode.applyMeshes(keyFrame)

        execTime = datetime.now() - startTime
        print("applied in %s ms"%execTime)

    def deleteMeshes(self, *args):
        """
        Deletes all the temporary stand-in meshes
        for the scene
        """
        self.coreNode.deleteMeshes()

    def createUI(self):
        """
        Creates the interaction Gui
        """
        self.gui = Gui(
            setup=self.setup,
            load=self.load,
            generate=self.generate,
            delete=self.deleteItem,
            editCurrent=self.focusModel,
            saveCurrent=self.saveState,
            selectChildren=self.selectChildren,
            cacheSelected=self.cacheStandin
        )

    def setupCoreNode(self):
        """
        Moved to coreNode.py class
        """
        self.coreNode = CoreNode()

def gui():
    CharacterCrowd()

def preRender():
    c = CharacterCrowd(createUI=False)
    c.applyMeshes()

def postRender():
    c = CharacterCrowd(createUI=False)
    c.deleteMeshes()



