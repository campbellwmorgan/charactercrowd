import pymel.core as pm
def empty(*args):
    print(args)

class Gui:

    def __init__(
            self,
            setup=empty,
            load=empty,
            generate=empty,
            delete=empty,
            editCurrent=empty,
            saveCurrent=empty,
            selectChildren=empty,
            cacheSelected=empty,
            ):
        # executes the setup of a given controller
        # takes params: item, meshes=[], keyable=[], prefix=''
        self.setupFunc = setup
        # load data from the selected item
        self.loadFunc = load
        # generates an instance of the current item
        self.generateFunc = generate
        # deletes the selected instance of the current item
        self.deleteFunc = delete
        # moves the mesh to the location
        # of the current instance and updates mesh's data
        # according to cache
        self.editCurrentFunc = editCurrent
        # saves data to standin
        self.saveCurrentFunc = saveCurrent
        # selects all children of current parent mesh
        self.selectChildrenFunc = selectChildren
        # caches selected item for current active time frame
        self.cacheSelectedFunc = cacheSelected

        self.parentItem = False
        self.parentVisItem = False
        self.meshes = False
        self.keyable = False
        self.prefix = False

        # set init states
        self.createUI()

    def selectParent(self, *args):
        # get selected
        sel = pm.ls(sl=1)
        if len(sel) is not 1:
            raise Exception("Parent must be a single item")
        self.parentItem = sel[0]
        self.mainCharacter.setLabel(str(self.parentItem.name()))

    def selectParentVis(self, *args):
        # get selected
        sel = pm.ls(sl=1)
        if len(sel) is not 1:
            raise Exception("Parent Vis must be a single item")
        self.parentVisItem = sel[0]
        self.parentVis.setLabel(str(self.parentVisItem.name()))

    def selectKeyable(self, *args):
        # get keyable nodes in hiearchy
        keyable = pm.ls(sl=1)
        stringed = self.nameSamples(keyable)
        self.selectedKeyable.setLabel(stringed)
        self.keyable = self.allKeyableAttrs(keyable)


    def allKeyableAttrs(self, keyable):
        """
        returns a list with all keyable attributes
        """
        keyableAttrs = []

        for node in keyable:
            attrs = pm.listAttr(node, k=1, u=1)
            for attr in attrs:
                keyableAttrs.append(str(node.name()) + "." + str(attr))

        return keyableAttrs

    def nameSamples(self, iterable):
        total = len(iterable)
        upper = min(total,1)
        return str(total) + " (" + ", ".join(
            [obj.name() for obj in iterable[0:upper]]
        ) + "...)"

    def selectMeshes(self, *args):
        self.meshes = pm.ls(sl=1)
        stringed = self.nameSamples(self.meshes)
        self.selectedMeshes.setLabel(stringed)

    def storePrefix(self, *args):
        self.prefix = self.uniquePrefixField.getText()
        self.setupGui.setCollapse(True)
        if self.meshes and self.keyable and self.parentItem and self.prefix and self.parentVisItem:
            self.setupFunc(
                item=self.parentItem,
                parentVis=self.parentVisItem.name(), # only send string
                meshes=self.meshes,
                keyable=self.keyable,
                prefix=self.prefix
            )
        else:
            pm.promptDialog(
                    title="Setup Incomplete",
                    message="Please Fill all sections first",
                    button=["OK"]
                    )

    def loadFromSelected(self, *args):
        # collapse the setup tab
        self.setupGui.setCollapse(True)
        # execute the load function
        self.loadFunc()

    def setupUI(self, parent, width):
        """
        Creates the UI for setting up a mesh
        """
        setupContainer = pm.frameLayout(p=parent,l="Init",cll=1, cl=1)
        setupManual = pm.frameLayout(p=setupContainer,l="a) Setup New Mesh",cll=1, cl=1,mw=10,mh=20)
        # reference text items to show when something selected
        self.mainCharacter = pm.text(label="No Character Selected", p=setupManual, al="left", w=width)
        self.parentVis = pm.text(label="No Visibility Node Selected", p=setupManual, al="left", w=width)
        pm.separator(p=setupManual,h=10,w=width,st="single",hr=1)
        self.selectedKeyable = pm.text(label="No Keyables Selected", p=setupManual, al="left", w=width)
        pm.separator(p=setupManual,h=10,w=width,st="single",hr=1)
        self.selectedMeshes = pm.text(label="No Meshes Selected", p=setupManual, al="left", w=width)
        pm.separator(p=setupManual,h=10,w=width,st="single",hr=1)

        self.parentButton = pm.button(label="Select Parent Node", p=setupManual,command=self.selectParent)
        pm.separator(p=setupManual,h=10,w=width,st="single",hr=1)
        self.parentButton = pm.button(label="Select Parent Visibility Node", p=setupManual,command=self.selectParentVis)
        pm.separator(p=setupManual,h=10,w=width,st="single",hr=1)
        self.keyableButton = pm.button(label="Select Keyable Nodes", p=setupManual, command=self.selectKeyable)
        pm.separator(p=setupManual,h=10,w=width,st="single",hr=1)
        self.meshesButton = pm.button(label="Select Meshes", p=setupManual, command=self.selectMeshes)
        pm.separator(p=setupManual,h=50,w=width,st="single",hr=1)

        pm.text(label="Create Unique Prefix:", p=setupManual)
        self.uniquePrefixField = pm.textField(p=setupManual,w=width,h=20)
        pm.separator(p=setupManual,h=20,w=width,st="single",hr=1)
        pm.button(label="Store",p=setupManual,command=self.storePrefix)

        load = pm.frameLayout(
                p=setupContainer,
                l="b) Load Existing",
                cll=1,
                cl=1,
                mw=10,
                mh=20
                )

        pm.button(label="Load from Selected",p=load,command=self.loadFromSelected)

        setupContainer.setCollapse(True)
        return setupContainer

    def createUI(self):
        width =200
        self.win = pm.window(title="Character Crowd")
        parentLayout = pm.columnLayout(rs=10, w=width)

        # create the setup gui
        self.setupGui = self.setupUI(parentLayout, width)

        # create main buttons
        pm.button(l="Generate Stand-in",p=parentLayout,h=20,w=width,command=self.generateFunc)
        # deletes the current standin
        pm.button(l="Delete Stand-in",p=parentLayout,h=20,w=width,command=self.deleteFunc)

        pm.button(l="Edit Selected Stand-in", p=parentLayout,h=20,w=width, command=self.editCurrentFunc)
        pm.button(l="Save Selected Stand-in", p=parentLayout,h=20,w=width, command=self.saveCurrentFunc)
        pm.button(l="Select All Stan-ins ", p=parentLayout,h=20,w=width, command=self.selectChildrenFunc)
        pm.button(l="Cache Selected", p=parentLayout,h=20,w=width, command=self.cacheSelectedFunc)

        self.win.setWidth(width)

        self.win.show()
