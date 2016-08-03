#Character Crowd

Animate and render large number of complex rigs
without overloading your GPU

##Why

If you already have finished rigs and do not want to have
to re-rig them to fit the constraints of one of the few popular
crowd simulation systems and you would like to manually tweak
your rig for each character, *CharacterCrowd* was made for you.

Importantly:
* you won't need to animate your rig in a separate scene file
* you won't need to export gigantic mesh caches for each frame
* you don't have to do anything special to your rig
* you don't have to load heavy blendshapes/skinning information into memory more than once


##How

1. Start with a referenced rig

2. Tell *CharacterCrowd* what is the parent controller, what are the controllers with keyable/animatable
attributes and what are the base meshes that are needed for the final render

3. Pose and animate your referenced rig as needed for the character

4. Press "Generate Standin" then "Save standin"

5. Repeat 3 & 4 until all standins have been generated. To edit a stand-in or preview animation on that stand-in,
select the standin node (arrow) then click "Edit Stand-in" and the reference rig will be positioned and keyed as the stand-in

6. Cache each standin - click on the stand-in controller and then "Cache Standin"

7. Ensure that the preRenderFrameMEL and postRenderFrameMel have been set

8. Render away and the standins will be replaced with the mesh animated


##Installation

Copy / Git clone this repo to your maya plugins folder

Open Plugins Manager and if `characterCrowd.py` not visible
scroll to bottom and Browse to find file

Open Gui with `characterCrowdGui()` in MEL script repl

Add `ccPreRenderFrame` to PostRenderFrameMEL
and `ccPostRenderFrame` to PostRenderFrameMEL in your file's
render settings

##Running the unit tests

`easy-install nose`

`<MAYA PYTHON PATH> ./src/runTests.py`

##LICENSE

Copyright 2016, Campbell Morgan

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

