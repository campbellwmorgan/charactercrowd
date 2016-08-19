from nose.tools import *
import pymel.core as pm

from standIn import StandIn

class MockExtra:
    def name(self):
        return "testName"

class NodeMock:

    children = []

    snapshot = {}

    coreD = {}

    node = MockExtra()

    def addChild(self, child):
        self.children.append(child)
    def removeChild(self, child):
        self.children.remove(child)

    def getSnapshot(self):
        return self.snapshot
    def coreData(self):
        return self.coreD



class testStandIn:

    def setUp(self):
        self.parentNode, self.parentNodeName = pm.polyCube()
        self.coreNode = NodeMock()
        self.source = NodeMock()
        self.standIn = StandIn(
                coreNode=self.coreNode,
                source=self.source,
                )

    def tearDown(self):
        pm.delete(self.parentNode)

    def testDelete(self):
        self.standIn.name = 'test'
        self.coreNode.children = ['test']
        self.source.children = ['test']
        self.standIn.node, nodeName = pm.polyCube()
        self.standIn.delete()
        eq_(len(self.coreNode.children),0)
        eq_(len(self.source.children),0)
        eq_(pm.objExists(nodeName), False)

    def testStoreMeta(self):
        self.standIn.node, nodeName = pm.polyCube()
        self.source.coreD = {
                "prefix":"testPrefix",
                "meshes":"testKeyable",
                }

        self.standIn.storeMeta()

        data = self.standIn.node.getAttr("characterCrowd")
        eq_(
            '{"source": "testName", "prefix": "testPrefix", "meshes": "testKeyable"}',
                data)
        pm.delete(nodeName)



