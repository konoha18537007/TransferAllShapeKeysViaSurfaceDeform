#-*- coding: utf-8 -*-

# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####


bl_info={
    "name" : "Transfer All Shape Keys Via Surface Deform",
    "author" : "konoha18537007",
    "version" : (1, 0),
    "blender": (2, 80, 0),
    "category": "Object"
}

import bpy
    

class TransferAllShapeKeysViaSurfaceDeform(bpy.types.Operator):
    u'''Transfer all shape keys from active object to selected objects via sufrace deform modifier'''
    bl_idname = "object.transfer_all_shape_keys_via_surface_deform"
    bl_label = "Transfer All Shape Keys Via Surface Deform"
    bl_options = {'REGISTER', 'UNDO'}

    DEBUG = False

    def invoke(self, context, event):
        return self.execute(context)

    def execute(self, context):
        ret = self.__transfer_shape_keys(context)
        if ret:
            self.report({"INFO"},"Finished transfer all shape keys via surface deform")
        else:
            self.report({"ERROR"},"Error on transfer all shape keys via surface deform")
        return {'FINISHED'}

    def __transfer_shape_keys(self, context):
        ret = True

        # get objects' references
        obj_src = context.active_object
        obj_tgts = [x for x in bpy.context.selected_objects if x != obj_src]

        # objects not selected (error return)
        if obj_src is None or len(obj_tgts) == 0:
            self.report({'ERROR'}, "select objects (active : src, selected : tgt)")
            ret = False
            return ret

        self.__debug("num shape keys : {0}".format(len(obj_src.data.shape_keys.key_blocks)))


        # memorize all shape keys' values and set them to 0
        sk_vals = []
        for kb in obj_src.data.shape_keys.key_blocks:
            sk_vals.append(kb.value)
            kb.value = 0

        # loop over target objects
        for o in obj_tgts:
            self.__debug("target object: {0}".format(o.name))

            # get surface deform modifier's ref 
            # (if multiple surface deforms exist (that's unexpected), get first)
            mod = None
            for m in o.modifiers:
                if m.type == 'SURFACE_DEFORM':
                    mod = m
                    break
            if mod is None:
                self.report({'ERROR'}, 'Surface Deform modifier dosen\'t exist on Object {0}'.format(o.name))
                ret = False
                break # skip to next object

            self.__debug("modifier name: {0}".format(mod.name))

            # transfer loop
            for i,kb in enumerate(obj_src.data.shape_keys.key_blocks):
                # skip the first shape key
                if i==0:
                    self.__debug("shape key: {0} (skipped as this is the 1st key)".format(kb.name))
                    continue

                self.__debug("shape key: {0}".format(kb.name))

                kb.value = 1

                # save as shape key
                bpy.context.view_layer.objects.active = o # set target object acitive 
                apply_ret = bpy.ops.object.modifier_apply_as_shapekey(keep_modifier=True, modifier=mod.name, report=True)

                if 'FINISHED' not in apply_ret:
                    self.report({'ERROR'}, "Error on pplying modifier, Object: {0}, ShapeKey: {1}, apply modifier: {2}".format(o.name, kb.name, apply_ret))
                    ret = False
                else:
                    o.data.shape_keys.key_blocks[-1].name = kb.name # rename

                kb.value=0

        # restore shape keys' values
        for i,kb in enumerate(obj_src.data.shape_keys.key_blocks):
            kb.value = sk_vals[i]

        return ret

    def __debug(self,msg):
        if self.DEBUG:
            self.report({"INFO"},msg)
        return


def menu_func(self, context):
    self.layout.operator(TransferAllShapeKeysViaSurfaceDeform.bl_idname)

classes = [
    TransferAllShapeKeysViaSurfaceDeform,
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.VIEW3D_MT_object.append(menu_func)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    bpy.types.VIEW3D_MT_object.remove(menu_func)

if __name__ == "__main__":
    register()
