import pymel.core as pm
from attributeStore import AttributeStore
from boxGenerator import BoxGenerator
from cache import Cache
from source import Source

"""
Abstraction of an individual stand-in
to streamline reading/writing data
and creation / deletion
"""

class StandIn:

    def __init__(
            self,
            coreNode=False, # root class
            source=False, # parent class
            node=False, # arrow node
            prefix="standInCtrl"
            ):
        self.coreNode = coreNode
        self.source = source
        self.node = node
        if node:
            self.name = str(node.name())

        self.store = AttributeStore()
        self.prefix = prefix
        axes = ["X","Y","Z"]
        attrs = ["translate","rotate","scale"]
        self.coreAttrs = []
        self.snapshotName = "snapshotData"
        for axis in axes:
            for attr in attrs:
                self.coreAttrs.append(
                        attr + axis
                        )
        # check if the source has been
        # defined, if not load from metadata
        if not source or not prefix:
            self.loadSourceFromMeta()

    def loadSourceFromMeta(self):
        """
        Loads the source from the
        node's metadata
        """
        meta = self.store.getCoreData(self.node)
        if not meta:
            raise Exception(
                    "Unable to load meta data:" +
                    "check that parent node exists"
                    )
        self.prefix = meta["prefix"]
        # save the current selection
        currentSelection = pm.ls(sl=1)
        # select the source
        pm.select(meta["source"])
        if len(pm.ls(sl=1)) is 0:
            raise Exception(
                "Source node not found"
                    )
        # load the current source
        # from the selection
        self.source = Source(selection=True)
        # load the old selection
        pm.select(currentSelection)

    def create(self):
        """
        Generates the physical box
        """
        generator = BoxGenerator(self.source.node)
        self.node, self.name = generator.makeCube(
                self.prefix + "_standInCtrl"
                )
        # register with source
        self.source.addChild(self.name)
        # register with core node
        self.coreNode.addChild(self.name)

        # save data
        self.storeMeta()
        # write attribute information
        # for key transforms
        self.sourceKeyTransforms()

        # now save it
        self.save()

        pm.select(self.node)
        return self.node

    def duplicate(self):
        """
        Creates a copy of itself that can be
        manipulated

        return new instance of StandIn
        """
        dupe = pm.duplicate(self.node)[0]
        newName = dupe.name()
        self.source.addChild(newName)
        self.coreNode.addChild(newName)
        newStandin = StandIn(
                coreNode=self.coreNode,
                source=self.source,
                node=dupe,
                prefix=self.prefix
                )
        self.store.transferAnimationAttrs(
                self.node,
                dupe
                )

        newStandin.storeMeta()
        newStandin.sourceKeyTransforms()
        pm.select(dupe)
        return newStandin

    def delete(self):
        """
        Deletes the stand-in
        and deregisters itself from
        core and parent
        """
        self.source.removeChild(self.name)
        self.coreNode.removeChild(self.name)
        pm.delete(self.node)


    def storeMeta(self):
        """
        Stores the core metadata:
        - what object source is
        - all attributes
        """
        coreData = self.source.coreData()

        meta = {
            "prefix":coreData["prefix"],
            "meshes":coreData["meshes"],
            "source":self.source.node.name(),
        }

        self.store.storeCoreData(self.node, meta)


    def save(self):
        """
        Saves the snapshot information
        for mesh as is and any keyed animation
        """
        self.store.animationAttrs(
                self.source.getKeys(),
                self.node
                )
        snapshot = self.source.getSnapshot()
        self.sourceKeyTransforms()
        self.store.storeCoreData(
                self.node,
                snapshot,
                self.snapshotName
        )

    def sourceKeyTransforms(self):
        """
        Set rotate, translate and scale
        from the parent on the standIn
        """
        for attr in self.coreAttrs:
            val = self.source.node.getAttr(attr)
            self.node.setAttr(attr, val)

    def parentKeyTransforms(self):
        """
        Set rotate, translate and scale
        from the standIn on the parent
        """
        for attr in self.coreAttrs:
            val = self.node.getAttr(attr)
            self.source.node.setAttr(attr, val)


    def confirm(self, message):
        """
        Pops up a confirm dialog
        returns true | false
        (abstracted for testing)
        """
        result = pm.confirmDialog(
                t="Sure?",
                m=message
                )
        return result is "Confirm"


    def focus(self):
        """
        Focuses the source mesh to the position
        of this standin
        """

        #if not self.confirm(
        #    "Focussing this stand-in will replace " +
        #    "all unsaved key/location on the source mesh. " +
        #    "Are you sure?"
        #    ):
        #    return
        # first set snapshot
        snapshot = self.store.getCoreData(
                self.node,
                self.snapshotName
                )

        # set snapshot
        self.source.loadSnapshot(snapshot)
        # transfer core transforms
        self.parentKeyTransforms()
        # clear key data on the source
        self.source.cleanKeyed()
        # load the stored animation data
        # from the keys
        self.store.loadStoredKeys(self.node)

    def cache(self):
        """
        Iterates through each frame in the
        frame range and saves the state to
        a cache file on the hard drive
        """
        cacher = Cache(
                self.source.prefix,
                self.name
                )

        startFrame = int(pm.playbackOptions(q=1,ast=1))
        endFrame = int(pm.playbackOptions(q=1,aet=1))
        for frame in range(startFrame, endFrame + 1):
            # go to current frame
            pm.currentTime(frame)
            # get the snapshot for this frame
            snapshot = self.source.getSnapshot()
            cacher.store(frame, snapshot)

        return True

