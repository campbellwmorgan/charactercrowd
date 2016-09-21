import pymel.core as pm
from attributeStore import AttributeStore

class Source:
    """
    Represents the source mesh control
    and can be instantiated with
    data or from a selection
    """

    def __init__(
            self,
            selection=False,
            meshes=[],
            keyable=[],
            prefix="",
            parentVis="",# string of parent visibility node
            node=False
            ):
        """
        """
        self.store = AttributeStore()

        if selection:
            self.fromSelection()
        else:
            self.meshes = self.toStrings(meshes)
            self.keyable = keyable
            self.prefix = prefix
            self.node = node
            self.parentVis = parentVis
            self.children = []
            self.save()

    def node(self):
        return self.node

    def fromSelection(self):
        """
        Gets all the prefix variables
        from a selected node
        """
        sel = pm.ls(sl=1)
        if not len(sel) is 1:
            raise Exception(
                    "Must have a node selected"
                    )
        node = sel[0]
        self.node = node
        data = self.store.getCoreData(node)
        children = self.store.getChildren(node)
        if not data:
            raise Exception(
                    "No data found on node"
                    )

        self.meshes = data['meshes']
        self.keyable = data['keyable']
        self.prefix = data['prefix']
        self.parentVis = data['parentVis']
        self.children = children


    def save(self):
        """
        Saves current data on class
        to attributes
        """
        if not self.node:
            raise Exception(
                    "Must provide valid source node"
                    )
        self.store.storeCoreData(self.node, self.coreData())
        self.store.storeChildren(self.node, self.children)

    def coreData(self):
        return {
            "meshes":self.meshes,
            "keyable":self.keyable,
            "prefix":str(self.prefix),
            "parentVis":str(self.parentVis),
            "source":str(self.node.name()),
        }

    def addChild(self, standinName):
        self.children.append(standinName)
        self.store.storeChildren(self.node, self.children)

    def removeChild(self, standinName):
        """
        Removes the child from the active list
        and deletes it from the scene
        """
        self.children.remove(standinName)
        self.store.storeChildren(self.node, self.children)

    def toStrings(self, lst):
        """
        Converts list of nodes to strings
        """
        return [node.name() for node in lst]

    def getSnapshot(self, openMaya=False):
        """
        Gets the data from every keyable attribute
        returns it as nested dict
        """
        snapshot = {}
        for attr in self.keyable:
            val = pm.getAttr(attr)
            # convert vectors into raw type
            # if possible
            if getattr(val, 'get', None):
                val = val.get()
            snapshot[attr] = {
                "value": val,
            }

        return snapshot

    def addKeyableAttrs(self, attrs):
        """
        Adds to list of keyable
        attributes
        """
        # iterate through current new attrs
        # check whether already included
        # and then add them if not
        for attr in attrs:
            if attr in self.keyable:
                continue
            self.keyable.append(attr)
        self.save()

    def loadSnapshot(self, attrHash):
        """
        Loads from a dict object where
        "<attributename>":"<attributeValue>"
        """
        if not attrHash:
            raise Exception(
                    "No saved data for this standin"
                    )
        for attr, data in attrHash.iteritems():
            pm.setAttr(attr, data["value"])

    def getKeys(self):
        """
        Searches through all keyable attributes
        for keyed node
        """
        keys = []
        for attr in self.keyable:
            if pm.keyframe(attr, q=1,kc=1) > 0:
                keys.append(attr)

        return keys

    def cleanKeyed(self):
        """
        Iterates through each keyable
        on the parent object and remove keys
        """
        for attr in self.keyable:
            pm.cutKey(attr, cl=1)
