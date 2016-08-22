"""
Plugin for manually animating
large numbers of rigs given a small number of source rigs

See README for installation instructions and usage
"""
from pymel.api.plugins import Command
import maya.OpenMayaMPx as OpenMayaMPx

from characterCrowdSrc.characterCrowd import *

class characterCrowdGui(Command):
    def doIt(self, args):
        print("loading gui...")
        gui()

class ccPreRenderFrame(Command):
    def doIt(self, args):
        preRender()

class ccPostRenderFrame(Command):
    def doIt(self, args):
        postRender()

class ccGenerate(Command):
    def doIt(self, args):
        generateStandin()

class ccDuplicate(Command):
    def doIt(self, args):
        duplicateStandin()

class ccSave(Command):
    def doIt(self, args):
        saveStandin()

class ccEdit(Command):
    def doIt(self, args):
        editStandin()

class ccCache(Command):
    def doIt(self, *args):
        cacheStandin()

## initialize the script plug-in
def initializePlugin(mobject):
    mplugin = OpenMayaMPx.MFnPlugin( mobject, "CampbellMorgan", "0.01" )
    characterCrowdGui.register()
    ccPreRenderFrame.register()
    ccPostRenderFrame.register()
    ccGenerate.register()
    ccDuplicate.register()
    ccSave.register()
    ccEdit.register()
    ccCache.register()
    ccSelectAll.register()
    print("Loaded CharacterCrowd")

# uninitialize the script plug-in
def uninitializePlugin(mobject):
    mplugin = OpenMayaMPx.MFnPlugin( mobject )
    characterCrowdGui.deregister()
    ccPreRenderFrame.deregister()
    ccPostRenderFrame.deregister()
    ccGenerate.deregister()
    ccDuplicate.deregister()
    ccSave.deregister()
    ccEdit.deregister()
    ccCache.deregister()
    ccSelectAll.deregister()
    print("Unloaded CharacterCrowd")
