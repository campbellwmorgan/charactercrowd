from gui import Gui
from nose.tools import *
import pymel.core as pm

class LabelMock:
    def setLabel(self, text):
        self.text = text

class TestGui(Gui):

    def __init__(self):
        ""

def test_selectKeyable():

    g = TestGui()

    g.parentItem = pm.polyCube()[0]
    firstCube = pm.polyCube()[0]
    secondCube = pm.polyCube()[0]
    g.selectedKeyable = LabelMock()
    pm.select(firstCube, secondCube)

    sel = pm.ls(sl=1)
    l = len(sel)
    eq_(l,2)
    g.selectKeyable()

    eq_("3 (pCube2...)", g.selectedKeyable.text)

    keyableAttrs = g.keyable

    eq_(len(keyableAttrs), 30)

    eq_(str(keyableAttrs[0]), 'pCube2.visibility')

    pm.delete(firstCube, secondCube, g.parentItem)
