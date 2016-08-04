import pymel.core as pm
import json
import re
from dataTypes import DataTypes
dt = DataTypes()

class AttributeStore:
    """
    Manages the get/set of data
    on objects
    """
    def __init__(self):
        self.attrName = 'characterCrowdChildren'
        self.childAttrName = 'characterCrowd'
        self.animationAttrName = 'animationAttrs'

    def getChildren(self, parentObject):
        """
        Returns a list of children
        stored in custom attribute
        """
        # check whether attribute exists
        if not self.attrExists(parentObject, self.attrName):
            return []

        data = parentObject.getAttr(self.attrName)

        # return json_decoded data
        itemNames = json.loads(data)
        return itemNames

    def storeChildren(self, parentObject, children):
        """
        Stores the list of children in the parent
        """
        self.checkAndCreate(parentObject, self.attrName)

        names = []

        for child in children:
            if isinstance(child, str) or isinstance(child, unicode):
                names.append(str(child))
            else:
                names.append(str(child.name()))

        parentObject.setAttr(self.attrName, json.dumps(names), type="string")

    def storeCoreData(self, item, data, attrOverride=False):
        attrName = attrOverride if attrOverride else self.childAttrName
        self.checkAndCreate(item, attrName)
        item.setAttr(attrName, json.dumps(data), type="string")

    def getCoreData(self, item, attrOverride=False):
        attr = attrOverride if attrOverride else self.childAttrName
        if not self.attrExists(item, attr):
            return False
        data = json.loads(item.getAttr(attr))
        return data

    def checkAndCreate(self, obj, attr):
        if not self.attrExists(obj, attr):
            # create the attribute
            pm.addAttr(
                    obj.name(),
                    ln=attr,
                    dt="string"
                    )

    def attrExists(self, obj, attr):
        return (
            len(obj.listAttr(st=attr)) > 0
        )

    def transferAnimationAttrs(self, src, dest):
        """
        When duplicating a standin, transfer across
        keyed attributes to the new standin
        """
        # get animation cache
        animationKeys = self.getCoreData(
                src,
                self.animationAttrName
                )
        # iterate through cache
        # and copy and paste over keys
        for newName, attr in animationKeys.iteritems():
            pm.copyKey(src, at=newName)
            pm.pasteKey(dest, at=newName)


    def animationAttrs(self, keyedAttrs, node):
        """
        Clears existing animation attrs (on Standin)
        then writes keys currently on souce
        mesh controls to standIn
        """
        self.clearAnimationAttrs(node)
        animationAttrs = {}

        for attr in keyedAttrs:
            # santize the name
            newName = self.processAttrName(attr)
            # get the attribute type
            # from the original
            attrType = str(pm.getAttr(attr, typ=1))
            attrVal = pm.getAttr(attr)
            # create new attribute
            if dt.isAt(str(attrType)):
                node.addAttr(newName, at=attrType, k=1)
            else:
                node.addAttr(newName, dt=attrType, k=1)

            # add to data map
            animationAttrs[newName] = attr

            # copy keys from original to new attribute
            elms = attr.split(".")
            copyRes = pm.copyKey(elms[0], at=elms[1])
            pm.pasteKey(node,at=newName)

        # write the dict to object
        self.storeCoreData(
                node,
                animationAttrs,
                self.animationAttrName
                )

    def loadStoredKeys(self, node):
        """
        Takes all the stored animation keys
        on a standIn node and transfers them
        to the source mesh controls
        """
        # get animation cache
        animationKeys = self.getCoreData(
                node,
                self.animationAttrName
                )

        for newName, attr in animationKeys.iteritems():
            pm.copyKey(node, at=newName)
            elms = attr.split(".")
            pm.pasteKey(elms[0], at=elms[1])


    def processAttrName(self, attr):
        name = re.sub("[^a-zA-Z0-9]+","", attr)
        length = len(name)
        if length > 60:
            name = name[(length - 60 + 5):]
        return name


    def clearAnimationAttrs(self, node):
        """
        Clears animation attributes from a node
        """

        if not self.attrExists(node, self.animationAttrName):
            return

        animationAttrs = json.loads(
                node.getAttr(self.animationAttrName)
            )
        # delete all attributes
        for attr, oldName in animationAttrs.iteritems():
            node.deleteAttr(attr)

