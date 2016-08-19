from nose.tools import *
import pymel.core as pm

from boxGenerator import BoxGenerator


# E2E test for generating the bounding box and arrow

class TestBoxGenerator:

    def setUp(self):
        self.cube, self.cubeShape = pm.polyCube(
                h=20,
                d=10,
                w=5,
                n="srcCube"
                )
        self.gen = BoxGenerator(self.cube)

    def tearDown(self):
        pm.delete(self.cube)

    def testMakeCube(self):
        self.cube.translate.set((4,5,10))
        self.cube.scale.set((1.2, 1.2, 1.2))
        arrow, name = self.gen.makeCube()

        eq_(1.2, arrow.getAttr('scaleX'))

