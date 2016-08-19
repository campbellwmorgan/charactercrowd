import pymel.core as pm
import maya.api.OpenMaya as om
from attributeStore import AttributeStore
from cache import Cache

class CoreNode:

    parentAttr = 'ccParentList'
    meshGrpAttr = 'ccMeshGroupName'

    def __init__(self):
        """
        searches for a hidden locator
        where all of the generated
        child meshes are found
        """
        base = "characterCrowdBase"
        self.store = AttributeStore()
        if pm.objExists(base):
            self.node = pm.ls(base)[0]
            self.load()
        else:
            self.node = pm.spaceLocator(
                    n=base
                    )
            self.children = []
            self.parents = []
            self.meshGroup = False
            # make invisible and lock
            self.node.setAttr(
                    "visibility",
                    0,
                    l=1
                    )



    def load(self):
        self.children = self.store.getChildren(self.node)
        self.parents = self.store.getCoreData(
                self.node,
                self.parentAttr
                )
        self.meshGroup = self.store.getCoreData(
                self.node,
                self.meshGrpAttr
                )

        return self.children, self.parents

    def save(self):
        self.store.storeChildren(
                self.node,
                self.children
                )

        self.store.storeCoreData(
                self.node,
                self.parents,
                self.parentAttr
                )

    def addChild(self, childName):
        self.children.append(childName)
        self.save()

    def addParentGroup(self, parentName):
        self.parents.append(parentName)
        self.save()

    def removeChild(self, childName):
        try:
            self.children.remove(childName)
        except:
            ""
        self.save()

    def removeParentGroup(self, parentName):
        try:
            self.parents.remove(parentName)
        except:
            ""
        self.save()

    def getNode(self):
        return self.node

    def getChildren(self):
        return self.children

    def getParents(self):
        return self.parents

    def applyMeshes(self, keyFrame):
        """
        Goes through every child
        applies the given snapshot
        to the source object, then duplicates
        the meshes at that position
        """
        # remove previous meshes
        self.deleteMeshes()
        # create a group for duplicate meshes
        if not self.meshGroup:
            meshGroup = pm.group(em=1,n="meshCache_" + str(keyFrame))
        self.storeMeshGroup(meshGroup.name())

        children, parents = self.load()
        for child in children:
            # ignore any children not found
            if not pm.objExists(child):
                print("Child " + child + " not found. Skipped")
                continue
            child = pm.ls(child)[0]
            meta = self.store.getCoreData(child)
            try:
                snapshot = self.loadCache(
                        keyFrame,
                        meta["prefix"],
                        child
                    )
                self.applySnapshot(snapshot)
                # duplicate mesh without history
                self.duplicateMeshes(meta["meshes"])
            except IOError:
                print("Cache file for %s not found. Skipping"%child)
            except:
                print("Cache file read error for %s. Skipping"%child)

        # hide the parent meshes
        self.parentVisibility(0)

    def deleteMeshes(self):
        """
        Delete the temporary meshes
        and reinstate parent visibility
        """

        if self.meshGroup:
            pm.delete(self.meshGroup)
            self.meshGroup = False
            self.storeMeshGroup(False)
        self.parentVisibility(1)

    def parentVisibility(self, vis=0):
        for parent in self.parents:
            if pm.objExists(parent):
                pm.setAttr(parent + '.visibility', vis)
            else:
                print("Parent vis %s not found "%parent)

    def loadCache(self, keyFrame, prefix, name):
        cache = Cache(prefix, name)
        return cache.fetch(keyFrame)

    def storeMeshGroup(self, groupName):
        self.meshGroup = groupName
        self.store.storeCoreData(
                self.node,
                groupName,
                self.meshGrpAttr
                )

    def applySnapshot(self, attrHash):
        """
        Applies all values to controllers
        """
        for attr, data in attrHash.iteritems():
            pm.setAttr(attr, data["value"])

    def forceDGEval(self, mesh):
        """
        Finds any connections to the relatives
        of the mesh and gets the attribute
        to trigger DG evaluation of connections
        FIXME Must be faster way of doing this!!
        """
        relatives = pm.listRelatives(mesh,c=1)
        relatives.append(mesh)
        for m in relatives:
            conns = pm.listConnections(m, d=0,s=1,p=1)
            if not len(conns):
                continue
            # now iterate through connections getting reverse
            for con in conns:
                revs = pm.listConnections(con, d=1,s=0,p=1)
                for rev in revs:
                    # get attribute to force update
                    pm.getAttr(rev)


    def duplicateMeshes(self, meshes):
        #pm.dgeval('meshDShape.testAttr')
        for mesh in meshes:
            if not pm.objExists(mesh):
                print("Mesh " + mesh + " not found. Skipped")
                continue
            self.forceDGEval(mesh)
            # now duplicate
            dupe = pm.duplicate(mesh)[0]
            # add to mesh group
            pm.parent(dupe, self.meshGroup)
