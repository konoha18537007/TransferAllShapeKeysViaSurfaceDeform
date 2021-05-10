# TransferAllShapeKeysViaSurfaceDeform
Blender Script.

## Description
This simple script "transfers" all of the shape keys of the active object to the non-active selected objects via surface deform modifier.
![screen](screen.gif 'screen')

I tested this only on blender 2.92. Use this script at your own risk.

## Usage
1. Set surface deform modifier to the target object/objects to be transferred, and bind it/them to the source object. You can use any of the options of surface deform modifier such as veterx group.

2. Select the target object/objects and source object. The source object must be active.

3. Run this script by "Object" on tool bar > "Transfer All Shape Keys Via Surface Deform".

## Installation
Edit > Preferences > Add-ons > Install... and select transfer_all_shape_keys_via_surface_deform.py

## Notice
* If a shape key with the same name as the source object's already exists on the target object, a shape key with the name like 'foo.001' will be added (not over written).
* I don't suppose multiple surface deform modifiers on single target object. This script will just run "Save as Shape Key" on the first modifier.

