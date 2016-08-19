from attributeStore import AttributeStore
from nose.tools import *
import pymel.core as pm


class testAttributeStore:

    def __init__(self):
        self.store = False
        self.cube = False

    def setUp(self):
        self.store = AttributeStore()
        self.cube = pm.polyCube()[0]

    def tearDown(self):
        if self.cube:
            pm.delete(self.cube)
        self.cube = False

    def testStoreChildren(self):
        children = ['a','b','c','d']
        self.store.storeChildren(self.cube, children)

        data = str(self.cube.getAttr("characterCrowdChildren"))
        eq_(data, '["a", "b", "c", "d"]')

    def testGetChildren(self):
        self.testStoreChildren()
        children = self.store.getChildren(self.cube)

        eq_(len(children), 4)
        eq_(children[0], "a")


    def testStoreCoreData(self):
        data = {
                "test":1,
            }
        self.store.storeCoreData(self.cube, data, 'testAttr')
        result = self.cube.getAttr('testAttr')
        eq_(result, '{"test": 1}')

    def testGetCoreData(self):
        self.testStoreCoreData()
        data = self.store.getCoreData(self.cube, "testAttr")
        eq_(data["test"], 1)

    def testProcessAttrName(self):
        a = self.store.processAttrName("*.& _ aB C")
        eq_(a, "aBC")
        bV = "eee" + "".join(["a" for i in range(70)])
        b = self.store.processAttrName(bV)
        eq_(len(b), 55)
        eq_(b[0], "a")

    def storeAnimationAttrs(self):

        name = str(self.cube.name())
        atr = name + ".translateX"
        pm.setKeyframe(
                atr,
                t=1,
                v=10
                )
        pm.setKeyframe(
                atr,
                t=5,
                v=5
                )

        self.store.animationAttrs(
                [atr],
                self.cube
                )
        return name

    def testAnimationAttrs(self):
        name = self.storeAnimationAttrs()

        keys = pm.keyframe(
                name + "." + name + "translateX"
                , q=1,kc=1
                )
        keys2 = pm.keyframe(
                name + ".translateX"
                , q=1,kc=1
                )

        eq_(keys,2)
        eq_(keys2,2)
        data = self.cube.getAttr('animationAttrs')
        eq_(data, '{"' + name + 'translateX": "' +name + '.translateX"}')

    def testLoadStoredKeys(self):
        name = self.storeAnimationAttrs()
        # clear keyframes on the cube
        pm.cutKey(self.cube,at="translateX", cl=1)
        self.store.loadStoredKeys(self.cube)
        keys = pm.keyframe(name + ".translateX", q=1, kc=1)
        eq_(keys,2)

    def testClearAnimationAttrs(self):
        ""
