"""
Plugin for manually animating
large numbers of rigs given a small number of source rigs

See README for installation instructions and usage
"""
from pymel.api.plugins import Command
import maya.OpenMayaMPx as OpenMayaMPx

from src.characterCrowd import gui, preRender, postRender

class characterCrowdGui(Command):
    def doIt(self, *args):
        print("loading gui...")
        gui()

class ccPreRenderFrame(Command):
    def doIt(self, *args):
        preRender()

class ccPostRenderFrame(Command):
    def doIt(self, *args):
        postRender()


## initialize the script plug-in
def initializePlugin(mobject):
    mplugin = OpenMayaMPx.MFnPlugin( mobject, "CampbellMorgan", "0.01" )
    characterCrowdGui.register()
    ccPreRenderFrame.register()
    ccPostRenderFrame.register()
    print("Loaded CharacterCrowd")

# uninitialize the script plug-in
def uninitializePlugin(mobject):
    mplugin = OpenMayaMPx.MFnPlugin( mobject )
    characterCrowdGui.deregister()
    ccPreRenderFrame.deregister()
    ccPostRenderFrame.deregister()
    print("Unloaded CharacterCrowd")
