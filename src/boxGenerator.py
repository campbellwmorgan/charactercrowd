import pymel.core as pm

class BoxGenerator:

    def __init__(self, obj):
        self.obj = obj
        self.displayLayerName = 'boundingBoxesLayer'

    def makeCube(self, nameOverride = 'newProxy'):
        currentScale = self.obj.scale.get()
        currentTrans = self.obj.translate.get()
        currentRotate = self.obj.rotate.get()
        # set object transforms to init
        self.obj.scale.set((1,1,1))
        self.obj.rotate.set((0,0,0))
        self.obj.translate.set((0,0,0))

        boundingBox = pm.exactWorldBoundingBox(self.obj)

        # return object to where it was
        self.obj.scale.set(currentScale)
        self.obj.rotate.set(currentRotate)
        self.obj.translate.set(currentTrans)

        height = (boundingBox[4]-boundingBox[1])
        cube = pm.polyCube(width=(boundingBox[3]-boundingBox[0]),
                            height=height,
                            depth=(boundingBox[5]-boundingBox[2]),
                            name=nameOverride + '_box'
                            )[0]

        cube.translate.set(0,height / 2, 0)
        # freeze cube transforms
        pm.makeIdentity(cube, a=1, t=1)

        # create an arrow showing the direction of
        # front rotation
        arrow = pm.curve(
                d=1,
                p=[
                    (-2, 0, 0),
                    (-2, 0, 6),
                    (-4, 0, 6),
                    (0, 0, 10),
                    (4, 0, 6),
                    (2, 0, 6),
                    (2, 0, 0)
                ],
                k=[0,1,2,3,4,5,6],
                n=nameOverride
        )
        pm.parent(cube, arrow)
        # add the cube to display layer
        self.addToDisplayLayer(cube)

        arrow.rotate.set(currentRotate)
        arrow.scale.set(currentScale)
        arrow.translate.set(currentTrans)

        # parent the cube to the arrow

        return (arrow, arrow.name())


    def addToDisplayLayer(self, elem):
        """
        Adds the new box to a display layer
        called 'boundingBoxes' if it exists
        else create it
        """
        if not pm.objExists(self.displayLayerName):
            displayLayer = self.createDisplayLayer()
        else:
            displayLayer = pm.ls(self.displayLayerName)[0]

        displayLayer.addMembers(elem)

        return displayLayer


    def createDisplayLayer(self):
        """
        Create display layer and set it to wireframe mode
        """
        layer = pm.createDisplayLayer(n=self.displayLayerName)
        # set display type to wireframe only
        layer.setAttr('displayType', 1)
        return layer





